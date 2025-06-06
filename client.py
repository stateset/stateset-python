import os
from typing import Any, Dict, Mapping, Optional

import httpx
from attrs import define, field
from httpx import Timeout

from . import __version__
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
        httpx_args: Optional[Dict[str, Any]] = None,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.headers = dict(headers or {})
        self.headers.setdefault("User-Agent", f"stateset-python/{__version__}")
        self.timeout = (
            timeout if isinstance(timeout, Timeout) else Timeout(timeout or 5.0)
        )
        self.follow_redirects = follow_redirects
        self.verify_ssl = verify_ssl
        self.raise_on_unexpected_status = raise_on_unexpected_status
        self.httpx_args = dict(httpx_args or {})
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
                **self.httpx_args,
            )
        return self._client

    def set_httpx_client(self, client: httpx.Client) -> None:
        """Use a custom :class:`httpx.Client` instance."""
        # Close any previously created client
        if self._client is not None and not self._client.is_closed:
            self._client.close()
        self._client = client
        # Keep configuration in sync with the new client
        self.base_url = str(client.base_url).rstrip("/")
        self.headers = dict(client.headers)
        self.timeout = client.timeout
        self.follow_redirects = client.follow_redirects
        self.verify_ssl = client.verify

    # Async httpx client -------------------------------------------------------
    def get_async_httpx_client(self) -> httpx.AsyncClient:
        if self._async_client is None:
            self._async_client = httpx.AsyncClient(
                base_url=self.base_url,
                headers=self.headers,
                timeout=self.timeout,
                follow_redirects=self.follow_redirects,
                verify=self.verify_ssl,
                **self.httpx_args,
            )
        return self._async_client

    def set_async_httpx_client(self, client: httpx.AsyncClient) -> None:
        """Use a custom :class:`httpx.AsyncClient` instance."""
        if self._async_client is not None and not self._async_client.is_closed:
            try:
                import asyncio

                asyncio.get_event_loop().run_until_complete(self._async_client.aclose())
            except Exception:
                pass
        self._async_client = client
        self.base_url = str(client.base_url).rstrip("/")
        self.headers = dict(client.headers)
        self.timeout = client.timeout
        self.follow_redirects = client.follow_redirects
        self.verify_ssl = client.verify

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

    def __exit__(
        self, *args: Any, **kwargs: Any
    ) -> None:  # pragma: no cover - simple close
        if self._client:
            self._client.close()

    async def __aenter__(self) -> "Client":
        self.get_async_httpx_client()
        return self

    async def __aexit__(
        self, *args: Any, **kwargs: Any
    ) -> None:  # pragma: no cover - simple close
        if self._async_client:
            await self._async_client.aclose()

    def close(self) -> None:
        """Close any underlying HTTP clients."""
        if self._client is not None and not self._client.is_closed:
            self._client.close()
        if self._async_client is not None and not self._async_client.is_closed:
            try:
                import asyncio

                asyncio.run(self._async_client.aclose())
            except RuntimeError:
                pass


class AuthenticatedClient(Client):
    """Adds bearer token authentication to :class:`Client`."""

    def __init__(
        self,
        *,
        token: str,
        base_url: str,
        httpx_args: Optional[Dict[str, Any]] = None,
        **kwargs: Any,
    ) -> None:
        headers = dict(kwargs.pop("headers", {}))
        headers.setdefault("Authorization", f"Bearer {token}")
        super().__init__(
            base_url=base_url, headers=headers, httpx_args=httpx_args, **kwargs
        )
        self.token = token


from .resources.agent_resource import Agents
from .resources.asset_resource import Assets
from .resources.attribute_resource import Attributes
from .resources.bill_of_material_resource import BillOfMaterials
from .resources.case_ticket_resource import CaseTickets
from .resources.channel_resource import Channels
from .resources.compliance_resource import Compliance
from .resources.contract_resource import Contracts
from .resources.customer_resource import Customers
from .resources.cycle_count_resource import CycleCounts
from .resources.eval_resource import Evals
from .resources.inventory_resource import Inventory
from .resources.invoice_line_resource import InvoiceLines
from .resources.invoice_resource import Invoices
from .resources.knowledge_resource import KnowledgeBase
from .resources.lead_resource import Leads
from .resources.location_resource import Locations
from .resources.log_resource import Logs
from .resources.machine_resource import Machines
from .resources.manufacture_order_line_resource import ManufactureOrderLines
from .resources.manufacture_order_resource import ManufactureOrders
from .resources.message_resource import Messages
from .resources.note_resource import Notes
from .resources.order_line_resource import OrderLines
from .resources.order_resource import Orders
from .resources.fulfillment_order_resource import FulfillmentOrders
from .resources.item_receipt_resource import ItemReceipts
from .resources.cash_sale_resource import CashSales
from .resources.payment_resource import Payments
from .resources.payout_resource import Payouts
from .resources.pick_resource import Picks
from .resources.product_resource import Products
from .resources.promotion_resource import Promotions
from .resources.purchase_order_line_resource import PurchaseOrderLines
from .resources.purchase_order_resource import PurchaseOrders
from .resources.response_resource import Responses
from .resources.return_line_resource import ReturnLines
from .resources.return_resource import Returns
from .resources.rule_resource import Rules
from .resources.schedule_resource import Schedule
from .resources.settlement_resource import Settlements
from .resources.ship_to_resource import ShipTo
from .resources.shipment_line_resource import ShipmentLines
from .resources.shipment_resource import Shipments
from .resources.supplier_resource import Suppliers
from .resources.user_resource import Users
from .resources.vendor_resource import Vendors
from .resources.warranty_line_resource import WarrantyLines
from .resources.warranty_resource import Warranties
from .resources.waste_and_scrap_resource import WasteAndScrap
from .resources.workflow_resource import Workflows
from .resources.workorder_line_resource import WorkOrderLines
from .resources.workorder_resource import WorkOrders


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
    timeout: float = field(
        default_factory=lambda: float(os.getenv("STATESET_TIMEOUT", "30.0"))
    )
    follow_redirects: bool = field(
        default_factory=lambda: os.getenv("STATESET_FOLLOW_REDIRECTS", "true").lower() not in {"0", "false", "no"}
    )
    verify_ssl: bool | str = field(
        default_factory=lambda: (
            False
            if os.getenv("STATESET_VERIFY_SSL", "true").lower() in {"0", "false", "no"}
            else os.getenv("STATESET_VERIFY_SSL", "true")
        )
    )
    httpx_args: Dict[str, Any] = field(factory=dict)
    _client: Optional[AuthenticatedClient] = field(init=False, default=None)

    def __attrs_post_init__(self):
        if not self.api_key:
            raise ValueError(
                "API key is required. Provide it via the 'api_key' argument or the 'STATESET_API_KEY' environment variable."
            )

        proxy = os.getenv("STATESET_HTTPX_PROXIES")
        if proxy and "proxies" not in self.httpx_args:
            self.httpx_args["proxies"] = proxy

        self._client = AuthenticatedClient(
            base_url=self.base_url,
            token=self.api_key,
            timeout=Timeout(timeout=self.timeout),
            follow_redirects=self.follow_redirects,
            verify_ssl=self.verify_ssl,
            httpx_args=self.httpx_args,
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
        self.notes = Notes(self._client)
        self.case_tickets = CaseTickets(self._client)
        self.agents = Agents(self._client)
        self.rules = Rules(self._client)
        self.attributes = Attributes(self._client)
        self.responses = Responses(self._client)
        self.knowledge = KnowledgeBase(self._client)
        self.evals = Evals(self._client)
        self.workflows = Workflows(self._client)
        self.schedules = Schedule(self._client)
        self.users = Users(self._client)
        self.settlements = Settlements(self._client)
        self.payouts = Payouts(self._client)
        self.fulfillment_orders = FulfillmentOrders(self._client)
        self.item_receipts = ItemReceipts(self._client)
        self.cash_sales = CashSales(self._client)
        self.payments = Payments(self._client)
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

    async def request(
        self, method: str, path: str, data: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
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
            response = await client.request(method=method, url=path, json=data)
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

    def close(self) -> None:
        """Close the underlying HTTP client."""
        self._client.close()
