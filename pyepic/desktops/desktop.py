from enum import Enum

from epiccore.models import (
    DesktopNodeQuote,
    DesktopNodeLaunchSpec,
    DataSpec

)

class MountType (Enum):
    """ How should the data folder be mounted to the desktop. Offline takes a copy of the data and will not be automatically synced back to the data store.	
    """
    ONLINE = 'online'
    OFFLINE = 'offline'


class Desktop(object):
    """ An EPIC Desktop Definition

            :param data_path: The path to the data to be loaded on the Desktop, formed as an epic url (e.g. "epic://path_to/data")
            :type path: str
            :param application_version: The ID of the Desktop Application Version to launch
            :type application_version: int
            :param node_type: The ID of the Desktop Node Type to launch
            :type node_type: int
            :param connection_type: The ID of the Desktop Connection Type to use
            :type connection_type: int

            :var runtime: The runtime for the Desktop in hours
            :vartype runtime: int
            :var mount_type: How should the data folder be mounted to the desktop. Offline takes a copy of the data and will not be automatically synced back to the data store.	
            :vartype mount_type: :class:`MountType`
            :var secure_ip: Should we restrict which IPs can connect to this node? (defaults to False)
            :vartype secure_ip: bool, optional
            :var ip_address: If secure_ip is True, which IP should connections be restricted to?
            :vartype ip_address: str, optional
            :var invoice_reference: Reference string for this desktop to appear on invoices.
            :vartype invoice_reference: str, optional
            :var project_id: ID of the EPIC project to run this job in
            :vartype project_id: int, optional
    """

    def __init__(self, data_path, application_version = 1, node_type = 1 , connection_type = 1):
        self.application_version = application_version
        self.node_type = node_type
        self.connection_type = connection_type
        self.data_path = data_path
        self.runtime = 1
        self.mount_type = MountType.ONLINE
        self.secure_ip = False
        self.ip_address = None
        self.invoice_reference = None
        self.project_id = None

    def get_quote_spec(self):
        """Get a Specification for this desktop for quotes

            :return: Desktop Quote Specification
            :rtype: class:`epiccore.models.DesktopNodeQuote`
        """
        quote = DesktopNodeQuote(
            application_version=self.application_version,
            node_type=self.node_type,
            connection_type=self.connection_type,
            runtime=self.runtime
        )
        return quote

    def get_launch_spec(self):
        """Get a Specification for this desktop for launching it

            :return: Desktop Specification
            :rtype: class:`epiccore.models.DesktopNodeLaunchSpec`
        """
        spec = DesktopNodeLaunchSpec(
            application_version=self.application_version,
            node_type=self.node_type, 
            connection_type=self.connection_type,
            runtime=self.runtime,
            secure_ip=self.secure_ip,
            ip_address=self.ip_address,
            invoice_reference=self.invoice_reference,
            data_path=DataSpec(
                path=self.data_path,
            ),
            mount_type=self.mount_type.value,
            project=self.project_id
        )
        return spec

