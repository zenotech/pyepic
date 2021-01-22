import epiccore

from .base import Client


class TeamsClient(Client):
    """A wrapper class around the epiccore Teams API.

    :param connection_token: Your EPIC API authentication token
    :type connection_token: str
    :param connection_url: The API URL for EPIC, defaults to "https://epic.zenotech.com/api/v2"
    :type connection_url: str, optional

    """

    def list(self):
        """List all of the teams you have access to on EPIC.

        :return: An interable list of Teams
        :rtype: collections.Iterable[:class:`epiccore.models.Team`]
        """
        with epiccore.ApiClient(self.configuration) as api_client:
            limit = 10
            offset = 0
            instance = epiccore.TeamsApi(api_client)
            results = instance.teams_list(limit=limit, offset=offset)
            for result in results.results:
                yield result
            while results.next is not None:
                offset += limit
                results = instance.teams_list(limit=limit, offset=offset)
                for result in results.results:
                    yield result

    def get_details(self, id: int):
        """Get the details for team with ID id

        :return: The Team details
        :rtype: :class:`epiccore.models.TeamDetails`
        """
        with epiccore.ApiClient(self.configuration) as api_client:
            instance = epiccore.TeamsApi(api_client)
            return instance.teams_read(id=id)
