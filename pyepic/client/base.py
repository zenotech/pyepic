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

import epiccore


class Client(object):
    """Base client class for API wrappers

    :param connection_token: Your EPIC API authentication token
    :type connection_token: str
    :param connection_url: The API URL for EPIC, defaults to "https://epic.zenotech.com/api/v2"
    :type connection_url: str, optional

    """

    def __init__(
        self, connection_token, connection_url="https://epic.zenotech.com/api/v2"
    ):
        """Constructor method"""
        self.LIMIT = 10
        self.configuration = epiccore.Configuration(
            host=connection_url,
            api_key={"Bearer": "Bearer {}".format(connection_token)},
        )

    def set_limt(self, limit):
        self.LIMIT = limit


class EPICClient(object):
    """A wrapper class around the epiccore API.

    :param connection_token: Your EPIC API authentication token
    :type connection_token: str
    :param connection_url: The API URL for EPIC, defaults to "https://epic.zenotech.com/api/v2"
    :type connection_url: str, optional

    :var job: API to Job functions
    :vartype job: :class:`JobClient`
    :var catalog: API to Catalog functions
    :vartype catalog: :class:`CatalogClient`
    :var desktops: API to Desktops functions
    :vartype desktops: :class:`DesktopClient`
    :var projects: API to Projects functions
    :vartype projects: :class:`ProjectClient`
    :var teams: API to Teams functions
    :vartype teams: :class:`TeamsClient`
    """

    def __init__(
        self, connection_token, connection_url="https://epic.zenotech.com/api/v2"
    ):
        """Constructor method"""
        from .job import JobClient
        from .catalog import CatalogClient
        from .desktop import DesktopClient
        from .projects import ProjectClient
        from .teams import TeamsClient
        from .data import DataClient

        self.job = JobClient(connection_token, connection_url=connection_url)
        self.catalog = CatalogClient(connection_token, connection_url=connection_url)
        self.desktops = DesktopClient(connection_token, connection_url=connection_url)
        self.projects = ProjectClient(connection_token, connection_url=connection_url)
        self.teams = TeamsClient(connection_token, connection_url=connection_url)
        self.data = DataClient(connection_token, connection_url=connection_url)
