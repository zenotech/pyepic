import epiccore

from .base import Client


class CatalogClient(Client):
    """A wrapper class around the epiccore Catalog API.

            :param connection_token: Your EPIC API authentication token
            :type connection_token: str
            :param connection_url: The API URL for EPIC, defaults to "https://epic.zenotech.com/api/v2"
            :type connection_url: str, optional

        """

    def list_clusters(self, limit=10, offset=0, cluster_name=None, application_id=None):
        """List the clusters available in EPIC

            :param limit: Number of results to return per request, defaults to 10
            :type limit: int
            :param offset: The initial index from which to return the results, defaults to 0
            :type offset: int
            :param cluster_name: Filter clusters by cluster name.
            :type cluster_name: str, optional
            :param application_id: Filter clusters by those with application application_id available.
            :type application_id: int, optional
            :return: Response with results of returned :class:`epiccore.models.BatchQueueDetails` objects
            :rtype: class:`APIListResponse`
        """
        with epiccore.ApiClient(self.configuration) as api_client:
            instance = epiccore.CatalogApi(api_client)
            return instance.catalog_clusters_list(limit=limit, offset=offset, cluster_name=cluster_name, allowed_apps=application_id)

    def list_applications(self, limit=10, offset=0, product_name=None):
        """List the applications available in EPIC

            :param limit: Number of results to return per request, defaults to 10
            :type limit: int
            :param offset: The initial index from which to return the results, defaults to 0
            :type offset: int
            :param product_name: Filter clusters by application name. 
            :type product_name: str, optional
            :return: Response with results of returned :class:`epiccore.models.BatchApplicationDetails` objects
            :rtype: class:`APIListResponse`
        """
        with epiccore.ApiClient(self.configuration) as api_client:
            instance = epiccore.catalog_api.CatalogApi(api_client)
            return instance.catalog_applications_list(limit=limit, offset=offset, product_name=product_name)

    def list_desktops(self, limit=10, offset=0):
        """List the available Desktops in EPIC

            :param limit: Number of results to return per request, defaults to 10
            :type limit: int
            :param offset: The initial index from which to return the results, defaults to 0
            :type offset: int
            :return: Response with results of returned :class:`epiccore.models.BatchApplicationDetails` objects
            :rtype: class:`APIListResponse`
        """
        with epiccore.ApiClient(self.configuration) as api_client:
            instance = epiccore.CatalogApi(api_client)
            return instance.catalog_desktop_list(limit=limit, offset=offset)
