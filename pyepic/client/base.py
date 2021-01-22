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
