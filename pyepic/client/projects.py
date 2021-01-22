import epiccore

from .base import Client


class ProjectClient(Client):
    """A wrapper class around the epiccore Projects API.

    :param connection_token: Your EPIC API authentication token
    :type connection_token: str
    :param connection_url: The API URL for EPIC, defaults to "https://epic.zenotech.com/api/v2"
    :type connection_url: str, optional

    """

    def list(self):
        """List all of the projects you have access to on EPIC.

        :return: An interable list of Projects
        :rtype: collections.Iterable[:class:`epiccore.models.Project`]
        """
        with epiccore.ApiClient(self.configuration) as api_client:
            limit = 10
            offset = 0
            instance = epiccore.ProjectsApi(api_client)
            results = instance.projects_list(limit=limit, offset=offset)
            for result in results.results:
                yield result
            while results.next is not None:
                offset += limit
                results = instance.projects_list(limit=limit, offset=offset)
                for result in results.results:
                    yield result

    def get_details(self, id: int):
        """Get the details for project with ID id

        :return: The Project
        :rtype: :class:`epiccore.models.ProjectDetails`
        """
        with epiccore.ApiClient(self.configuration) as api_client:
            instance = epiccore.ProjectsApi(api_client)
            return instance.projects_read(id=id)
