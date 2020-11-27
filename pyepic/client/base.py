import epiccore


class APIListResponse(object):
    """An abstract representation of the response from an EPIC API list request
    """

    @property
    def count(self):
        """
        :return: Number of results returned
        :rtype: int
        """
        pass

    @property
    def next():
        """
        :return next: The uri to get the next set of responses
        :rtype: str
        """
        pass

    @property
    def previous():
        """
        :return next: The uri to get the previous set of responses
        :rtype: str
        """
        pass

    @property
    def results():
        """
        :return: A list of the repsonse objects for request
        :rtype: list
        """
        pass


class Client(object):
    """Base client class for API wrappers

            :param connection_token: Your EPIC API authentication token
            :type connection_token: str
            :param connection_url: The API URL for EPIC, defaults to "https://epic.zenotech.com/api/v2"
            :type connection_url: str, optional

        """

    def __init__(self, connection_token, connection_url="https://epic.zenotech.com/api/v2"):
        """Constructor method
        """
        self.configuration = epiccore.Configuration(
            host=connection_url,
            api_key={
                'Bearer': 'Bearer {}'.format(connection_token)
            }
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
            :var desktop: API to Desktops functions
            :vartype desktop: :class:`DesktopClient`
        """

    def __init__(self, connection_token, connection_url="https://epic.zenotech.com/api/v2"):
        """Constructor method
        """
        from .job import JobClient
        from .catalog import CatalogClient
        from .desktop import DesktopClient

        self.job = JobClient(connection_token, connection_url=connection_url)
        self.catalog = CatalogClient(connection_token, connection_url=connection_url)
        self.desktop = DesktopClient(connection_token, connection_url=connection_url)
