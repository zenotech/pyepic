# BSD 3 - Clause License

# Copyright(c) 2020, Zenotech
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# 1. Redistributions of source code must retain the above copyright notice, this
# list of conditions and the following disclaimer.

# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and / or other materials provided with the distribution.

# 3. Neither the name of the copyright holder nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
#         SERVICES
#         LOSS OF USE, DATA, OR PROFITS
#         OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import boto3
from botocore.credentials import RefreshableCredentials
from botocore.exceptions import ClientError
from botocore.session import get_session
import epiccore
import errno
import os
from pathlib import Path
from queue import Queue, Empty
import sys
import threading

from .base import Client


class DataThread(threading.Thread):
    """
    Thread class used internally by pyepic for managaing upload/download functions
    """

    def __init__(
        self,
        s3_client,
        bucket_name,
        s3_prefix,
        local_path,
        file_queue,
        cancel_event=None,
        dryrun=False,
        callback=None,
        download_thread=True,
        overwrite_existing=False,
        meta_data={},
    ):
        threading.Thread.__init__(self)
        self.__s3_client = s3_client
        self.__bucket_name = bucket_name
        self.__s3_prefix = s3_prefix
        self.__file_q = file_queue
        self.__cancelled = cancel_event
        self.__local_path = local_path
        self.__overwrite_existing = overwrite_existing
        self.__download_thread = download_thread
        self.__callback = callback
        self.__dryrun = dryrun
        self.__meta_data = meta_data

    def __validate_s3_key_as_dir_name(self, s3_key_name):

        ERROR_INVALID_NAME = 123

        try:
            for pathname_part in s3_key_name.split("/"):
                try:
                    os.lstat("/" + pathname_part)
                    # If an OS-specific exception is raised, its error code
                    # indicates whether this pathname is valid or not. Unless this
                    # is the case, this exception implies an ignorable kernel or
                    # filesystem complaint (e.g., path not found or inaccessible).
                    #
                    # Only the following exceptions indicate invalid pathnames:
                    #
                    # * Instances of the Windows-specific "WindowsError" class
                    #   defining the "winerror" attribute whose value is
                    #   "ERROR_INVALID_NAME". Under Windows, "winerror" is more
                    #   fine-grained and hence useful than the generic "errno"
                    #   attribute. When a too-long pathname is passed, for example,
                    #   "errno" is "ENOENT" (i.e., no such file or directory) rather
                    #   than "ENAMETOOLONG" (i.e., file name too long).
                    # * Instances of the cross-platform "OSError" class defining the
                    #   generic "errno" attribute whose value is either:
                    #   * Under most POSIX-compatible OSes, "ENAMETOOLONG".
                    #   * Under some edge-case OSes (e.g., SunOS, *BSD), "ERANGE".
                except OSError as exc:
                    if hasattr(exc, "winerror"):
                        if exc.winerror == ERROR_INVALID_NAME:
                            return False
                    elif exc.errno in {errno.ENAMETOOLONG, errno.ERANGE}:
                        return False
        # If a "TypeError" exception was raised, it almost certainly has the
        # error message "embedded NUL character" indicating an invalid pathname.
        except TypeError as exc:
            return False
        except ValueError as exc:
            return False
        else:
            return True

    def run(self):
        while not self.__cancelled.is_set():
            try:
                item = self.__file_q.get(True, 5)
                if self.__download_thread:
                    source_path, target_path, status = self.download_key(item)
                    source_path = "epic://" + source_path.split("/", 1)[1]
                else:
                    source_path, target_path, status = self.upload_file(item)
                    target_path = "epic://" + target_path.split("/", 1)[1]
                if self.__callback is not None:
                    self.__callback(source_path, target_path, status, self.__dryrun)
            except Empty:
                break
            except Exception as e:
                raise e
        return

    def download_key(self, key_name):
        file_path = os.path.sep.join(key_name.split(self.__s3_prefix)[1].split("/"))
        full_file_path = os.path.join(self.__local_path, file_path)

        if not self.__validate_s3_key_as_dir_name(key_name):
            raise ValueError("Invalid key name: %s" % str(key_name))

        if full_file_path.endswith("/"):
            if not os.path.isdir(full_file_path) and not self.__dryrun:
                try:
                    os.makedirs(full_file_path)
                except FileExistsError:
                    # Directory created on another thread
                    pass
            return (key_name, full_file_path, False)
        if os.path.exists(full_file_path):
            if not self.__overwrite_existing:
                return (key_name, full_file_path, False)
            local_modified = os.path.getmtime(full_file_path)
            s3_modified = self.__s3_client.head_object(
                Bucket=self.__bucket_name, Key=key_name
            )["LastModified"]
            if s3_modified.timestamp() < local_modified:
                return (key_name, full_file_path, False)
            os.remove(full_file_path)
        file_dir = os.path.dirname(full_file_path)
        if not os.path.isdir(file_dir) and not self.__dryrun:
            try:
                os.makedirs(file_dir)
            except FileExistsError:
                # Directory created on another thread
                pass
        if self.__dryrun:
            return (key_name, full_file_path, False)
        else:
            self.__s3_client.download_file(self.__bucket_name, key_name, full_file_path)
            return (key_name, full_file_path, True)

    def upload_file(self, file_full_path):
        last_modified = os.path.getmtime(file_full_path)
        key_name = os.path.relpath(file_full_path, self.__local_path)
        if key_name.startswith("/"):
            key_name = key_name[1:]
        s3_key_name = self.__s3_prefix + key_name
        upload = False
        try:
            s3_head = self.__s3_client.head_object(
                Bucket=self.__bucket_name, Key=s3_key_name
            )
            if self.__overwrite_existing:
                s3_modified = s3_head["LastModified"].timestamp()
                if last_modified > s3_modified:
                    upload = True
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                upload = True
            else:
                raise e
        if upload and not self.__dryrun:
            self.__s3_client.upload_file(
                file_full_path,
                self.__bucket_name,
                s3_key_name,
                ExtraArgs={"Metadata": self.__meta_data},
            )
            return (file_full_path, s3_key_name, True)
        return (file_full_path, s3_key_name, False)


class DataObject(object):
    """Class representing a file or folder

    :param name: Name of the file/folder
    :type name: str
    :param obj_path: Path of the file/folder
    :type obj_path: str
    :param folder: Is the object a folder?
    :type folder: bool
    :param name: Size of the object if available
    :type name: int
    :param last_modified: Last modified time if available. Datetime in ISO 8601 format, UTC timezone.
    :type last_modified: str
    """

    def __init__(self, name, obj_path, folder=False, size=None, last_modified=None):
        """Constructor method"""
        self.name = name
        self.obj_path = obj_path
        self.folder = folder
        self.size = size
        self.last_modified = last_modified


class DataClient(Client):
    """A wrapper class around the epiccore Data API.

    :param connection_token: Your EPIC API authentication token
    :type connection_token: str
    :param connection_url: The API URL for EPIC, defaults to "https://epic.zenotech.com/api/v2"
    :type connection_url: str, optional

    """

    _s3_prefix = None
    _s3_bucket = None
    _s3_client = None

    meta_source = "SDK"

    def _fetch_profile_details_from_epic(self):
        with epiccore.ApiClient(self.configuration) as api_client:
            instance = epiccore.ProfileApi(api_client)
            return instance.profile_settings_list()

    def _fetch_session_details_from_epic(self):
        with epiccore.ApiClient(self.configuration) as api_client:
            instance = epiccore.DataApi(api_client)
            return instance.data_session_list()

    def _refresh_credentials(self):
        "Refresh AWS access credentials"
        session_details = self._fetch_session_details_from_epic()
        credentials = {
            "access_key": session_details.session_token.aws_key_id,
            "secret_key": session_details.session_token.aws_secret_key,
            "token": session_details.session_token.aws_session_token,
            "expiry_time": session_details.session_token.expiration.isoformat(),
            "region": session_details.aws_region,
            "s3_obj_key": session_details.s3_obj_key,
            "s3_location": session_details.s3_location,
        }
        return credentials

    def _connect(self):
        if self._s3_client is None:
            session_details = self._refresh_credentials()
            session_credentials = RefreshableCredentials.create_from_metadata(
                metadata=session_details,
                refresh_using=self._refresh_credentials,
                method="sts-assume-role",
            )
            session = get_session()
            session._credentials = session_credentials
            session.set_config_variable("region", session_details["region"])
            autorefresh_session = boto3.Session(botocore_session=session)
            self._s3_client = autorefresh_session.client("s3")
            self._s3_prefix = session_details["s3_obj_key"]
            self._s3_bucket = session_details["s3_location"]
            profile_details = self._fetch_profile_details_from_epic()
            self._meta_data = {
                "Source": self.meta_source,
                "User-Profile": str(profile_details.id),
            }

    def _epic_path_to_s3(self, epic_path):
        self._connect()
        if epic_path[:7] != "epic://":
            raise ValueError("Path specification must start with epic://")
        raw_path = epic_path[7:]
        s3_path = "{}{}".format(self._s3_prefix, raw_path)
        return s3_path

    def _s3_to_epic_path(self, s3_key):
        self._connect()
        path = s3_key.split("/", 1)[1]
        return "epic://{}".format(path)

    def _page_keys(self, s3_prefix, delimeter=""):
        paginator = self._s3_client.get_paginator("list_objects_v2")
        pages = paginator.paginate(
            Bucket=self._s3_bucket, Prefix=s3_prefix, Delimiter=delimeter
        )
        return pages

    def _list_contents(self, s3_prefix, delimeter=""):
        response_pages = self._page_keys(s3_prefix, delimeter=delimeter)
        for response in response_pages:
            if response["KeyCount"] == 0:
                raise ValueError("EPIC Path not found")
            for s3_obj in response["Contents"]:
                yield s3_obj["Key"]

    def ls(self, epic_path):
        """
        List the files and folders at the given path
            :param epic_path: Path in the form epic://[<folder>]/
            :type epic_path: str

            :return: Iterable collection of DataObject
            :rtype: collections.Iterable[:class:`pyepic.client.data.DataObject`]
        """
        self._connect()
        if not epic_path.endswith("/"):
            epic_path = epic_path + "/"
        prefix = self._epic_path_to_s3(epic_path)
        response_pages = self._page_keys(prefix, delimeter="/")
        for response in response_pages:
            if response["KeyCount"] == 0:
                raise ValueError("Path not found")
            if "CommonPrefixes" in response:
                for item in response["CommonPrefixes"]:
                    folder = DataObject(
                        item["Prefix"].split("/")[-2],
                        self._s3_to_epic_path(item["Prefix"]),
                        folder=True,
                    )
                    yield folder
            if "Contents" in response:
                for item in response["Contents"]:
                    file = DataObject(
                        item["Key"].split("/")[-1],
                        self._s3_to_epic_path(item["Key"]),
                        folder=False,
                        size=item["Size"],
                        last_modified=item["LastModified"].isoformat(),
                    )
                    yield file

    def get_file_meta_data(self, epic_path):
        """
        Get the meta-data for the file at epic_path
            :param epic_path: Path of a file in the form epic://[<folder>]/<file>
            :type epic_path: str

            :return: Dictionary of file meta-data
            :rtype: dict
        """
        self._connect()
        if epic_path.endswith("/"):
            raise ValueError("Invalid file epic path")
        s3_path = self._epic_path_to_s3(epic_path)
        # bytes_buffer = io.BytesIO()
        print(s3_path)
        head = self._s3_client.head_object(Bucket=self._s3_bucket, Key=s3_path)
        return head["Metadata"]

    def download_file(self, epic_path, destination):
        """
        Download the contents of epic_path
            :param epic_path: Path of a file in the form epic://[<folder>]/<file>
            :type epic_path: str
            :param destination: Location to download file to, can be a string or a writable file-like object
            :type destination: str
        """
        self._connect()
        if epic_path.endswith("/"):
            raise ValueError("Invalid file epic path")
        s3_path = self._epic_path_to_s3(epic_path)
        if destination.endswith(os.path.sep):
            if not os.path.isdir(destination):
                os.makedirs(destination)
        if os.path.isdir(destination):
            destination = os.path.join(destination, epic_path.split("/")[-1])
        if type(destination) == str:
            self._s3_client.download_file(self._s3_bucket, s3_path, destination)
        else:
            self._s3_client.download_fileobj(self._s3_bucket, s3_path, destination)

    def upload_file(self, file, epic_path):
        """
        Upload the contents of file to epic_path
            :param destination: Location of the file to upload OR a readable file-like object
            :type destination: str
            :param epic_path: Destination path of a file in the form epic://[<folder>]/<file>
            :type epic_path: str
        """
        self._connect()
        if type(file) == str:
            if epic_path.endswith("/"):
                file_name = os.path.basename(file)
                epic_path += file_name
            s3_path = self._epic_path_to_s3(epic_path)
            self._s3_client.upload_file(
                file, self._s3_bucket, s3_path, ExtraArgs={"Metadata": self._meta_data}
            )
        else:
            if epic_path.endswith("/"):
                raise ValueError("Invalid file epic path")
            s3_path = self._epic_path_to_s3(epic_path)
            self._s3_client.upload_fileobj(
                file, self._s3_bucket, s3_path, ExtraArgs={"Metadata": self._meta_data}
            )

    def delete(self, epic_path, dryrun=False):
        """
        Delete the file of folder at epic_path
            :param epic_path: Path of a file or folder to delete in the form epic://[<folder>]/<file>
            :type epic_path: str
            :param dryrun: If dryrun is True then return a list of files that would be deleted without actually deleting them
            :type dryrun: bool

            :return: List of the files deleted
            :rtype: List[str]
        """
        self._connect()
        deleted = []
        if not epic_path.endswith("/"):
            key = self._epic_path_to_s3(epic_path)
            deleted.append(epic_path)
            if not dryrun:
                response = self._s3_client.delete_object(
                    Bucket=self._s3_bucket, Key=key
                )
            return deleted
        else:
            objects = []
            prefix = self._epic_path_to_s3(epic_path)
            key_list = self._list_contents(prefix)
            for item in key_list:
                deleted.append(self._s3_to_epic_path(item))
                objects.append({"Key": item})
            if not dryrun:
                response = self._s3_client.delete_objects(
                    Bucket=self._s3_bucket,
                    Delete={"Objects": objects},
                )
                if "Errors" in response:
                    # TODO, remove any error files for deleted list
                    pass
            return deleted

    def sync(
        self,
        source_path,
        target_path,
        dryrun=False,
        overwrite_existing=False,
        callback=None,
        threads=3,
        cancel_event=None,
    ):
        """
        Synchronize the data from one directory to another, source_path or target_path can be a remote folder or a local folder.
            :param source_path: Source folder to syncronise from. For remote folders use form epic://[<folder>]/<file>.
            :type source_path: str
            :param target_path: Target folder to syncronise to. For remote folders use form epic://[<folder>]/<file>.
            :type target_path: str
            :param dryrun: If dryrun == True then no actual copy will take place but the callback will be called with the generated source and target paths. This can be useful for checking before starting a large upload/download.
            :type dryrun: bool, optional
            :param overwrite_existing: If overwrite_existing == True then files with newer modification timestamps in source_path will replace existing files in target_path
            :type overwrite_existing: bool, optional
            :param callback: A callback method that accepts four parameters. These are source, destination, a boolean indicating if a copy has taken place and a boolean to indicate if the copy was a dryrun. The callback is called after each file is processed.
            :type callback: method, optional
            :param threads: Number of threads to use for sync
            :type threads: int, optional
            :param cancel_event: An instance of threading.Event that can be set to cancel the sync.
            :type cancel_event: :class:`threading.Event`
        """
        if source_path.startswith("epic://"):
            if target_path.startswith("epic://"):
                raise ValueError("Both source_path and target_path are EPIC paths")
            if not source_path.endswith("/"):
                source_path = source_path + "/"
            target_path = os.path.expanduser(target_path)
            Path(target_path).mkdir(parents=True, exist_ok=True)
            prefix = self._epic_path_to_s3(source_path)
            self._download(
                prefix,
                target_path,
                dryrun=dryrun,
                callback=callback,
                overwrite_existing=overwrite_existing,
                cancel_event=cancel_event,
            )
        elif target_path.startswith("epic://"):
            if source_path.startswith("epic://"):
                raise ValueError("Both source_path and target_path are EPIC paths")
            if not target_path.endswith("/"):
                target_path = target_path + "/"
            source_path = os.path.expanduser(source_path)
            if not os.path.isdir(source_path):
                raise ValueError("source_path does not exist")
            prefix = self._epic_path_to_s3(target_path)
            self._upload(
                source_path,
                prefix,
                dryrun=dryrun,
                callback=callback,
                overwrite_existing=overwrite_existing,
                cancel_event=cancel_event,
            )
        else:
            raise ValueError("At least one epic:// path must be specified")

    def _download(
        self,
        s3_prefix,
        local_destination,
        dryrun=False,
        callback=None,
        threads=3,
        overwrite_existing=False,
        cancel_event=None,
    ):
        file_queue = Queue()
        if cancel_event is None:
            cancel_event = threading.Event()
        thread_pool = []
        for i in range(threads):
            t = DataThread(
                self._s3_client,
                self._s3_bucket,
                s3_prefix,
                local_destination,
                file_queue,
                cancel_event=cancel_event,
                dryrun=dryrun,
                callback=callback,
                download_thread=True,
                overwrite_existing=overwrite_existing,
            )
            t.daemon = True
            t.start()
            thread_pool.append(t)
        file_count = 0
        keys = self._list_contents(s3_prefix)
        for key in keys:
            file_count += 1
            file_queue.put(key)
        for i in range(threads):
            while thread_pool[i].is_alive():
                thread_pool[i].join(1)

    def _upload(
        self,
        local_source,
        s3_prefix,
        threads=1,
        dryrun=False,
        callback=None,
        overwrite_existing=False,
        cancel_event=None,
    ):
        file_queue = Queue()
        if cancel_event is None:
            cancel_event = threading.Event()
        thread_pool = []
        for i in range(threads):
            t = DataThread(
                self._s3_client,
                self._s3_bucket,
                s3_prefix,
                local_source,
                file_queue,
                cancel_event=cancel_event,
                dryrun=dryrun,
                callback=callback,
                download_thread=False,
                overwrite_existing=overwrite_existing,
                meta_data=self._meta_data,
            )
            t.daemon = True
            t.start()
            thread_pool.append(t)
        file_count = 0
        for dirname, _, filenames in os.walk(local_source):
            for filename in filenames:
                full_path = os.path.join(dirname, filename)
                file_count += 1
                file_queue.put(full_path)
        for i in range(threads):
            while thread_pool[i].is_alive():
                thread_pool[i].join(1)
