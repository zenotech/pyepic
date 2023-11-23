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

import time
import epiccore

from .base import Client


class JobClient(Client):
    """A wrapper class around the epiccore Job API.

    :param connection_token: Your EPIC API authentication token
    :type connection_token: str
    :param connection_url: The API URL for EPIC, defaults to "https://epic.zenotech.com/api/v2"
    :type connection_url: str, optional

    """

    def get_quote(self, job_spec):
        """Get a Quote for running a series of tasks on EPIC.

        :param job_spec: The EPIC job specification
        :type job_spec: class:`epiccore.models.JobSpec`
        :return: A quote giving the price for the job on the available HPC queues
        :rtype: class:`epiccore.models.JobQuote`
        """
        with epiccore.ApiClient(self.configuration) as api_client:
            instance = epiccore.JobApi(api_client)
            return instance.job_quote(job_spec)

    def submit(self, job_array_spec):
        """Submit new job in EPIC as described by job_array_spec.

        :param job_array_spec: The EPIC job specification
        :type job_array_spec: class:`epiccore.models.JobArraySpec`
        :return: The newly created job instance
        :rtype: class:`epiccore.models.Job`
        """
        with epiccore.ApiClient(self.configuration) as api_client:
            instance = epiccore.JobApi(api_client)
            return instance.job_create(job_array_spec)

    def list(self, job_array=None, limit=10):
        """List all of the jobs in EPIC.

        :param job_array: Filter by job array ID (optional)
        :type job_array: int
        :param limit: Maximum number of jobs to list
        :type limit: int
        :return: Iterable collection of Jobs
        :rtype: collections.Iterable[:class:`epiccore.models.Job`]
        """
        with epiccore.ApiClient(self.configuration) as api_client:
            offset = 0
            count = 0
            get_batch_size = 20
            if limit < get_batch_size:
                get_batch_size = limit
            instance = epiccore.JobApi(api_client)
            if job_array:
                results = instance.job_list(job_array=str(job_array), limit=get_batch_size, offset=offset)
            else:
                results = instance.job_list(limit=get_batch_size, offset=offset)
            for result in results.results:
                count += 1
                yield result
            if count < limit:
                while results.next is not None:
                    offset += get_batch_size
                    if offset >= limit:
                        return
                    results = instance.job_list(limit=get_batch_size, offset=offset)
                    for result in results.results:
                        if count >= limit:
                            return
                        count += 1
                        yield result

    def list_steps(self, parent_job=None):
        """List all of the job steps in EPIC.

        :param parent_job: The ID of the parent job to list the steps for
        :type parent_job: int, optional

        :return: Iterable collection of Job Steps
        :rtype: collections.Iterable[:class:`epiccore.models.JobStep`]
        """
        with epiccore.ApiClient(self.configuration) as api_client:
            limit = self.LIMIT
            offset = 0
            instance = epiccore.JobstepApi(api_client)
            results = instance.jobstep_list(
                limit=limit, offset=offset, parent_job=parent_job
            )
            for result in results.results:
                yield result
            while results.next is not None:
                offset += limit
                results = instance.job_list(limit=limit, offset=offset)
                for result in results.results:
                    yield result

    def get_details(self, job_id):
        """Get details of job with ID job_id

        :param job_id: The ID of the job to fetch details on
        :type job_id: int
        :return: A Job instance
        :rtype: class:`epiccore.models.Job`
        """
        with epiccore.ApiClient(self.configuration) as api_client:
            instance = epiccore.JobApi(api_client)
            return instance.job_read(job_id)

    def get_step_details(self, step_id):
        """Get the details of the step ID step_id

        :param step_id: The ID of the job step to fetch
        :type step_id: int
        :return: A Job Step instance
        :rtype: class:`epiccore.models.JobStep`
        """
        with epiccore.ApiClient(self.configuration) as api_client:
            instance = epiccore.JobstepApi(api_client)
            return instance.jobstep_read(step_id)

    def get_step_logs(self, step_id, refresh=True, refresh_timeout=10):
        """Get the step logs for step with id step_id

        :param step_id: The ID of the step to fetch the logs for
        :type step_id: int
        :param dryrun: If refresh is True then the request will attempt to refresh the logs before returning the latest update
        :type dryrun: bool, optional
        :param dryrun: How many seconds should we wait for a refresh before giving up, default 10 seconds
        :type dryrun: int, optional

        :return: A Job Log instance
        :rtype: class:`epiccore.models.JobLog`
        """
        if refresh:
            with epiccore.ApiClient(self.configuration) as api_client:
                try:
                    instance = epiccore.JobrefreshApi(api_client)
                    refresh_obj = instance.jobrefresh_create({"job_step": step_id})
                    count = 0
                    while (
                        count < refresh_timeout
                    ) and not refresh_obj.response_recieved:
                        time.sleep(1)
                        count += 1
                        refresh_obj = instance.jobrefresh_create({"job_step": step_id})
                except epiccore.exceptions.ApiException as e:
                    if e.status != 400:
                        raise (e)
        with epiccore.ApiClient(self.configuration) as api_client:
            instance = epiccore.JobstepApi(api_client)
            return instance.jobstep_logs_read(step_id)

    def cancel(self, job_id):
        """Cancel job with ID job_id

        :param job_id: The ID of the job to cancel
        :type job_id: int
        """
        with epiccore.ApiClient(self.configuration) as api_client:
            instance = epiccore.JobApi(api_client)
            return instance.job_cancel(job_id, {})

    def get_job_residual_names(self, job_id):
        """Get the names of the residual variables available forjob with id job_id

        :param job_id: The ID of the job to get the residual list for
        :type job_id: int

        :return: A list of variable names
        :rtype: List[str]
        """
        with epiccore.ApiClient(self.configuration) as api_client:
            instance = epiccore.JobApi(api_client)
            return instance.job_residuals_read(job_id, variables=None).variables

    def get_job_residual_values(self, job_id, variable_list):
        """Get the names of the residual variables available forjob with id job_id

        :param job_id: The ID of the job to get the variables for
        :type job_id: int
        :param variable_names: A list of the variables to return
        :type variable_names: List[str]

        :return: A JobResidualData object
        :rtype: class:`epiccore.models.JobResidualData`
        """
        with epiccore.ApiClient(self.configuration) as api_client:
            instance = epiccore.JobApi(api_client)
            return instance.job_residuals_read(
                job_id, variables=variable_list
            ).residual_values
