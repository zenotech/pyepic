import epiccore

from .base import Client


class CatalogClient(Client):
    """A wrapper class around the epiccore Catalog API.

    :param connection_token: Your EPIC API authentication token
    :type connection_token: str
    :param connection_url: The API URL for EPIC, defaults to "https://epic.zenotech.com/api/v2"
    :type connection_url: str, optional

    """

    def list_clusters(self, cluster_name=None, queue_name=None, application_id=None):
        """List the clusters available in EPIC

        :param cluster_name: Filter clusters by cluster name.
        :type cluster_name: str, optional
        :param queue_name: Filter clusters by queue name.
        :type queue_name: str, optional
        :param application_id: Filter clusters by those with application application_id available.
        :type application_id: int, optional

        :return: Iterable collection of BatchQueueDetails
        :rtype: collections.Iterable[:class:`epiccore.models.BatchQueueDetails`]
        """
        with epiccore.ApiClient(self.configuration) as api_client:
            limit = self.LIMIT
            offset = 0
            instance = epiccore.CatalogApi(api_client)
            results = instance.catalog_clusters_list(
                limit=limit,
                offset=offset,
                cluster_name=cluster_name,
                queue_name=queue_name,
                allowed_apps=application_id,
            )
            for result in results.results:
                yield result
            while results.next is not None:
                offset += limit
                results = instance.catalog_clusters_list(
                    limit=limit,
                    offset=offset,
                    cluster_name=cluster_name,
                    queue_name=queue_name,
                    allowed_apps=application_id,
                )
                for result in results.results:
                    yield result

    def list_applications(self, product_name=None):
        """List the applications available in EPIC

        :param product_name: Filter clusters by application name.
        :type product_name: str, optional

        :return: Iterable collection of BatchApplicationDetails
        :rtype: collections.Iterable[:class:`epiccore.models.BatchApplicationDetails`]
        """
        with epiccore.ApiClient(self.configuration) as api_client:
            limit = self.LIMIT
            offset = 0
            instance = epiccore.CatalogApi(api_client)
            results = instance.catalog_applications_list(
                limit=limit, offset=offset, product_name=product_name
            )
            for result in results.results:
                yield result
            while results.next is not None:
                offset += limit
                results = instance.catalog_applications_list(
                    limit=limit, offset=offset, product_name=product_name
                )
                for result in results.results:
                    yield result

    def list_desktops(self):
        """List the available Desktops in EPIC

        :return: Iterable collection of DesktopNodeApp
        :rtype: collections.Iterable[:class:`epiccore.models.DesktopNodeApp`]
        """
        with epiccore.ApiClient(self.configuration) as api_client:
            limit = self.LIMIT
            offset = 0
            instance = epiccore.CatalogApi(api_client)
            results = instance.catalog_desktop_list(limit=limit, offset=offset)
            for result in results.results:
                yield result
            while results.next is not None:
                offset += limit
                results = instance.catalog_desktop_list(limit=limit, offset=offset)
                for result in results.results:
                    yield result
