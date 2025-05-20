from typing import Optional, Dict, Any, Mapping
import os
import httpx
from httpx import Timeout
from attrs import define, field

from .errors import raise_for_status_code


class Client:
    """HTTP client wrapper used by the generated endpoints."""

    def __init__(
        self,
        *,
        base_url: str,
        headers: Optional[Mapping[str, str]] = None,
        timeout: Timeout | float | None = None,
        follow_redirects: bool = True,
        verify_ssl: bool | str = True,
        raise_on_unexpected_status: bool = False,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.headers = dict(headers or {})
        self.timeout = timeout if isinstance(timeout, Timeout) else Timeout(timeout or 5.0)
        self.follow_redirects = follow_redirects
        self.verify_ssl = verify_ssl
        self.raise_on_unexpected_status = raise_on_unexpected_status
        self._client: Optional[httpx.Client] = None
        self._async_client: Optional[httpx.AsyncClient] = None

    # Synchronous httpx client -------------------------------------------------
    def get_httpx_client(self) -> httpx.Client:
        if self._client is None:
            self._client = httpx.Client(
                base_url=self.base_url,
                headers=self.headers,
                timeout=self.timeout,
                follow_redirects=self.follow_redirects,
                verify=self.verify_ssl,
            )
        return self._client

    # Async httpx client -------------------------------------------------------
    def get_async_httpx_client(self) -> httpx.AsyncClient:
        if self._async_client is None:
            self._async_client = httpx.AsyncClient(
                base_url=self.base_url,
                headers=self.headers,
                timeout=self.timeout,
                follow_redirects=self.follow_redirects,
                verify=self.verify_ssl,
            )
        return self._async_client

    # Convenience async request helpers ---------------------------------------
    async def get(self, path: str, **kwargs: Any) -> Dict[str, Any]:
        response = await self.get_async_httpx_client().get(path, **kwargs)
        raise_for_status_code(response.status_code, response.content)
        return response.json()

    async def post(self, path: str, **kwargs: Any) -> Dict[str, Any]:
        response = await self.get_async_httpx_client().post(path, **kwargs)
        raise_for_status_code(response.status_code, response.content)
        return response.json()

    async def put(self, path: str, **kwargs: Any) -> Dict[str, Any]:
        response = await self.get_async_httpx_client().put(path, **kwargs)
        raise_for_status_code(response.status_code, response.content)
        return response.json()

    async def delete(self, path: str, **kwargs: Any) -> None:
        response = await self.get_async_httpx_client().delete(path, **kwargs)
        raise_for_status_code(response.status_code, response.content)

    # Lifecycle management -----------------------------------------------------
    def __enter__(self) -> "Client":
        self.get_httpx_client()
        return self

    def __exit__(self, *args: Any, **kwargs: Any) -> None:  # pragma: no cover - simple close
        if self._client:
            self._client.close()

    async def __aenter__(self) -> "Client":
        self.get_async_httpx_client()
        return self

    async def __aexit__(self, *args: Any, **kwargs: Any) -> None:  # pragma: no cover - simple close
        if self._async_client:
            await self._async_client.aclose()


class AuthenticatedClient(Client):
    """Adds bearer token authentication to :class:`Client`."""

    def __init__(self, *, token: str, base_url: str, **kwargs: Any) -> None:
        headers = dict(kwargs.pop("headers", {}))
        headers.setdefault("Authorization", f"Bearer {token}")
        super().__init__(base_url=base_url, headers=headers, **kwargs)
        self.token = token
from .resources.return_resource import Returns
from .resources.warranty_resource import Warranties
from .resources.product_resource import Products
from .resources.order_resource import Orders
from .resources.shipment_resource import Shipments
from .resources.inventory_resource import Inventory
from .resources.customer_resource import Customers
from .resources.workorder_resource import WorkOrders
from .resources.bill_of_material_resource import BillOfMaterials
from .resources.purchase_order_resource import PurchaseOrders
from .resources.manufacture_order_resource import ManufactureOrders
from .resources.channel_resource import Channels
from .resources.message_resource import Messages
from .resources.agent_resource import Agents
from .resources.rule_resource import Rules
from .resources.attribute_resource import Attributes
from .resources.workflow_resource import Workflows
from .resources.user_resource import Users
from .resources.return_line_resource import ReturnLines
from .resources.warranty_line_resource import WarrantyLines
from .resources.order_line_resource import OrderLines
from .resources.shipment_line_resource import ShipmentLines
from .resources.workorder_line_resource import WorkOrderLines
from .resources.purchase_order_line_resource import PurchaseOrderLines
from .resources.manufacture_order_line_resource import ManufactureOrderLines
from .resources.settlement_resource import Settlements
from .resources.payout_resource import Payouts
from .resources.pick_resource import Picks
from .resources.cycle_count_resource import CycleCounts
from .resources.machine_resource import Machines
from .resources.waste_and_scrap_resource import WasteAndScrap
from .resources.supplier_resource import Suppliers
from .resources.location_resource import Locations
from .resources.vendor_resource import Vendors
from .resources.invoice_resource import Invoices
from .resources.invoice_line_resource import InvoiceLines
from .resources.compliance_resource import Compliance
from .resources.lead_resource import Leads
from .resources.asset_resource import Assets
from .resources.contract_resource import Contracts
from .resources.promotion_resource import Promotions
from .resources.schedule_resource import Schedule
from .resources.ship_to_resource import ShipTo
from .resources.log_resource import Logs

@define
class Stateset:
    """Main entry point for interacting with the Stateset API.

    The ``api_key`` and ``base_url`` parameters can be supplied directly or via
    the ``STATESET_API_KEY`` and ``STATESET_BASE_URL`` environment variables.
    """

    api_key: str = field(default_factory=lambda: os.getenv("STATESET_API_KEY", ""))
    base_url: str = field(
        default_factory=lambda: os.getenv(
            "STATESET_BASE_URL",
            "https://stateset-proxy-server.stateset.cloud.stateset.app/api",
        )
    )
    _client: Optional[AuthenticatedClient] = field(init=False, default=None)

    def __attrs_post_init__(self):
        if not self.api_key:
            raise ValueError(
                "API key is required. Provide it via the 'api_key' argument or the 'STATESET_API_KEY' environment variable."
            )

        self._client = AuthenticatedClient(
            base_url=self.base_url,
            token=self.api_key,
            timeout=Timeout(timeout=30.0),
            follow_redirects=True,
        )
        
        # Initialize all resource classes
        self.returns = Returns(self._client)
        self.return_items = ReturnLines(self._client)
        self.warranties = Warranties(self._client)
        self.warranty_items = WarrantyLines(self._client)
        self.products = Products(self._client)
        self.orders = Orders(self._client)
        self.order_items = OrderLines(self._client)
        self.shipments = Shipments(self._client)
        self.shipment_items = ShipmentLines(self._client)
        self.ship_to = ShipTo(self._client)
        self.inventory = Inventory(self._client)
        self.customers = Customers(self._client)
        self.workorders = WorkOrders(self._client)
        self.workorder_items = WorkOrderLines(self._client)
        self.bill_of_materials = BillOfMaterials(self._client)
        self.purchase_orders = PurchaseOrders(self._client)
        self.purchase_order_items = PurchaseOrderLines(self._client)
        self.manufacturer_orders = ManufactureOrders(self._client)
        self.manufacturer_order_items = ManufactureOrderLines(self._client)
        self.channels = Channels(self._client)
        self.messages = Messages(self._client)
        self.agents = Agents(self._client)
        self.rules = Rules(self._client)
        self.attributes = Attributes(self._client)
        self.workflows = Workflows(self._client)
        self.schedules = Schedule(self._client)
        self.users = Users(self._client)
        self.settlements = Settlements(self._client)
        self.payouts = Payouts(self._client)
        self.picks = Picks(self._client)
        self.cycle_counts = CycleCounts(self._client)
        self.machines = Machines(self._client)
        self.waste_and_scrap = WasteAndScrap(self._client)
        self.suppliers = Suppliers(self._client)
        self.locations = Locations(self._client)
        self.vendors = Vendors(self._client)
        self.invoices = Invoices(self._client)
        self.invoice_lines = InvoiceLines(self._client)
        self.compliance = Compliance(self._client)
        self.leads = Leads(self._client)
        self.assets = Assets(self._client)
        self.contracts = Contracts(self._client)
        self.promotions = Promotions(self._client)
        self.logs = Logs(self._client)

    async def request(self, method: str, path: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Make an authenticated request to the Stateset API.
        
        Args:
            method: HTTP method to use (GET, POST, PUT, DELETE, etc.)
            path: API endpoint path
            data: Optional request body data
            
        Returns:
            API response as a dictionary
        """
        client = self._client.get_async_httpx_client()
        
        try:
            response = await client.request(
                method=method,
                url=path,
                json=data
            )
            raise_for_status_code(response.status_code, response.content)
            return response.json()
            
        except Exception as e:
            print(f"Error in Stateset request: {str(e)}")
            raise

    async def __aenter__(self) -> "Stateset":
        await self._client.__aenter__()
        return self

    async def __aexit__(self, *args: Any, **kwargs: Any) -> None:
        await self._client.__aexit__(*args, **kwargs)

    def __enter__(self) -> "Stateset":
        self._client.__enter__()
        return self

    def __exit__(self, *args: Any, **kwargs: Any) -> None:
        self._client.__exit__(*args, **kwargs)
