import epiccore


from .base import Client

class DesktopClient(Client):
    """A wrapper class around the epiccore Desktop API.

            :param connection_token: Your EPIC API authentication token
            :type connection_token: str
            :param connection_url: The API URL for EPIC, defaults to "https://epic.zenotech.com/api/v2"
            :type connection_url: str, optional

    """

    def get_quote(self, desktop_spec):
        """Get a Quote for launching the desktop on EPIC

            :param desktop_spec: The EPIC Desktop Quote specification
            :type desktop_spec: class:`epiccore.models.DesktopNodeQuote`
            :return: A quote giving the price for the job on the available HPC queues
            :rtype: class:`epiccore.models.PriceQuote`
        """
        with epiccore.ApiClient(self.configuration) as api_client:
            instance = epiccore.DesktopApi(api_client)
            return instance.desktop_quote(desktop_spec)

    def launch(self, desktop_spec):
        """Launch the Desktop described by desktop_spec in EPIC

            :param desktop_spec: The EPIC Desktop Launch specification
            :type desktop_spec: class:`epiccore.models.DesktopNodeQuote`
            :return: A quote giving the price for the job on the available HPC queues
            :rtype: class:`epiccore.models.DesktopInstance`
        """
        with epiccore.ApiClient(self.configuration) as api_client:
            instance = epiccore.DesktopApi(api_client)
            return instance.desktop_create(desktop_spec)

    def list(self, limit=10, offset=0):
        """List all of your Desktops in EPIC. 

            :param limit: Number of results to return per request, defaults to 10
            :type limit: int
            :param offset: The initial index from which to return the results, defaults to 0
            :type offset: int
            :return: Response with results of returned :class:`epiccore.models.Job` objects
            :rtype: class:`APIListResponse`
        """
        with epiccore.ApiClient(self.configuration) as api_client:
            instance = epiccore.DesktopApi(api_client)
            return instance.desktop_list(limit=limit, offset=offset)

    def get_details(self, id):
        """Get details of desktop with ID id

            :param id: The ID of the desktop to fetch details on
            :type id: int
            :return: A desktop instance
            :rtype: class:`epiccore.models.DesktopInstance`
        """
        with epiccore.ApiClient(self.configuration) as api_client:
            instance = epiccore.DesktopApi(api_client)
            return instance.desktop_read(id)

    def terminate(self, id):
        """Terminate Desktop job with ID id

            :param id: The ID of the Desktop to terminate
            :type id: int
        """
        with epiccore.ApiClient(self.configuration) as api_client:
            instance = epiccore.DesktopApi(api_client)
            return instance.desktop_terminate(id, {})
