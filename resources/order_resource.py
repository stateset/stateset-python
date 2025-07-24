"""
Enhanced Orders resource implementation with advanced operations and better developer experience.
"""

from datetime import datetime
from typing import Any, Dict, List, Optional, Union

from attrs import define

from ..client import AuthenticatedClient
from ..base_resource import BaseResource, FilterParams, RequestOptions, FilterOperator
from ..models.order import Order
from ..models.shipping_label import ShippingLabel
from ..errors import StatesetValidationError, StatesetInvalidRequestError


@define
class OrderFilters(FilterParams):
    """Enhanced filters specific to orders."""
    
    customer_id: Optional[str] = None
    total_amount_min: Optional[float] = None
    total_amount_max: Optional[float] = None
    order_date_from: Optional[str] = None
    order_date_to: Optional[str] = None
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert order filters to API parameters."""
        params = super().to_dict()
        
        if self.customer_id:
            params["customer_id"] = self.customer_id
        if self.total_amount_min is not None:
            params["total_amount[gte]"] = self.total_amount_min
        if self.total_amount_max is not None:
            params["total_amount[lte]"] = self.total_amount_max
        if self.order_date_from:
            params["order_date[gte]"] = self.order_date_from
        if self.order_date_to:
            params["order_date[lte]"] = self.order_date_to
            
        return params


class Orders(BaseResource[Order]):
    """Enhanced operations on Stateset Orders with advanced features."""

    def __init__(self, client: AuthenticatedClient) -> None:
        super().__init__(
            client, 
            Order, 
            "/orders",
            enable_caching=True  # Enable caching for orders
        )

    async def cancel(
        self, 
        id: str, 
        reason: Optional[str] = None,
        options: Optional[RequestOptions] = None
    ) -> Order:
        """
        Cancel an order with enhanced error handling.
        
        Args:
            id: Order ID to cancel
            reason: Optional cancellation reason
            options: Request options
            
        Returns:
            The cancelled order
            
        Raises:
            StatesetValidationError: If the order cannot be cancelled
        """
        if not id:
            raise StatesetInvalidRequestError("Order ID is required")
        
        data = {"reason": reason} if reason else {}
        request_kwargs = options.to_kwargs() if options else {}
        
        try:
            response = await self.client.post(
                f"{self.base_path}/{id}/cancel", 
                json=data,
                **request_kwargs
            )
            result = Order(**response)
            
            # Invalidate caches
            self._invalidate_resource_caches(id)
            
            return result
        except Exception as e:
            raise StatesetValidationError(
                f"Failed to cancel order {id}",
                detail=str(e)
            ) from e

    async def mark_as_shipped(
        self,
        id: str,
        tracking_number: str,
        carrier: str,
        shipped_at: Optional[Union[datetime, str]] = None,
        options: Optional[RequestOptions] = None,
    ) -> Order:
        """
        Mark an order as shipped with validation.
        
        Args:
            id: Order ID
            tracking_number: Tracking number from carrier
            carrier: Shipping carrier name
            shipped_at: When the order was shipped (defaults to now)
            options: Request options
            
        Returns:
            The updated order
        """
        if not id:
            raise StatesetInvalidRequestError("Order ID is required")
        if not tracking_number:
            raise StatesetInvalidRequestError("Tracking number is required")
        if not carrier:
            raise StatesetInvalidRequestError("Carrier is required")
        
        shipped_time = shipped_at
        if isinstance(shipped_at, datetime):
            shipped_time = shipped_at.isoformat()
        elif shipped_at is None:
            shipped_time = datetime.now().isoformat()
        
        data = {
            "tracking_number": tracking_number,
            "carrier": carrier,
            "shipped_at": shipped_time,
        }
        
        request_kwargs = options.to_kwargs() if options else {}
        
        try:
            response = await self.client.post(
                f"{self.base_path}/{id}/ship", 
                json=data,
                **request_kwargs
            )
            result = Order(**response)
            
            # Invalidate caches
            self._invalidate_resource_caches(id)
            
            return result
        except Exception as e:
            raise StatesetValidationError(
                f"Failed to mark order {id} as shipped",
                detail=str(e)
            ) from e

    async def add_items(
        self, 
        id: str, 
        items: List[Dict[str, Any]],
        options: Optional[RequestOptions] = None
    ) -> Order:
        """
        Add items to an existing order with validation.
        
        Args:
            id: Order ID
            items: List of items to add
            options: Request options
            
        Returns:
            The updated order
        """
        if not id:
            raise StatesetInvalidRequestError("Order ID is required")
        if not items:
            raise StatesetInvalidRequestError("Items list cannot be empty")
        
        # Validate item structure
        for i, item in enumerate(items):
            if "product_id" not in item:
                raise StatesetValidationError(
                    f"Item at index {i} missing required field: product_id"
                )
            if "quantity" not in item:
                raise StatesetValidationError(
                    f"Item at index {i} missing required field: quantity"
                )
        
        request_kwargs = options.to_kwargs() if options else {}
        
        try:
            response = await self.client.post(
                f"{self.base_path}/{id}/items", 
                json={"items": items},
                **request_kwargs
            )
            result = Order(**response)
            
            # Invalidate caches
            self._invalidate_resource_caches(id)
            
            return result
        except Exception as e:
            raise StatesetValidationError(
                f"Failed to add items to order {id}",
                detail=str(e)
            ) from e

    async def remove_items(
        self, 
        id: str, 
        item_ids: List[str],
        options: Optional[RequestOptions] = None
    ) -> Order:
        """
        Remove items from an existing order.
        
        Args:
            id: Order ID
            item_ids: List of item IDs to remove
            options: Request options
            
        Returns:
            The updated order
        """
        if not id:
            raise StatesetInvalidRequestError("Order ID is required")
        if not item_ids:
            raise StatesetInvalidRequestError("Item IDs list cannot be empty")
        
        request_kwargs = options.to_kwargs() if options else {}
        
        try:
            response = await self.client.delete(
                f"{self.base_path}/{id}/items",
                json={"item_ids": item_ids},
                **request_kwargs
            )
            result = Order(**response)
            
            # Invalidate caches
            self._invalidate_resource_caches(id)
            
            return result
        except Exception as e:
            raise StatesetValidationError(
                f"Failed to remove items from order {id}",
                detail=str(e)
            ) from e

    async def create_shipping_label(
        self, 
        id: str, 
        label_data: Dict[str, Any],
        options: Optional[RequestOptions] = None
    ) -> ShippingLabel:
        """
        Create a shipping label for this order with validation.
        
        Args:
            id: Order ID
            label_data: Shipping label configuration
            options: Request options
            
        Returns:
            The created shipping label
        """
        if not id:
            raise StatesetInvalidRequestError("Order ID is required")
        if not label_data:
            raise StatesetInvalidRequestError("Label data is required")
        
        request_kwargs = options.to_kwargs() if options else {}
        
        try:
            response = await self.client.post(
                f"{self.base_path}/{id}/shipping_label",
                json=label_data,
                **request_kwargs
            )
            return ShippingLabel(**response)
        except Exception as e:
            raise StatesetValidationError(
                f"Failed to create shipping label for order {id}",
                detail=str(e)
            ) from e

    async def get_shipping_status(
        self, 
        id: str,
        options: Optional[RequestOptions] = None
    ) -> Dict[str, Any]:
        """
        Get shipping status and tracking information for an order.
        
        Args:
            id: Order ID
            options: Request options
            
        Returns:
            Shipping status information
        """
        if not id:
            raise StatesetInvalidRequestError("Order ID is required")
        
        request_kwargs = options.to_kwargs() if options else {}
        
        try:
            return await self.client.get(
                f"{self.base_path}/{id}/shipping_status",
                **request_kwargs
            )
        except Exception as e:
            raise StatesetValidationError(
                f"Failed to get shipping status for order {id}",
                detail=str(e)
            ) from e

    async def refund(
        self,
        id: str,
        amount: Optional[float] = None,
        reason: Optional[str] = None,
        options: Optional[RequestOptions] = None
    ) -> Dict[str, Any]:
        """
        Issue a refund for an order.
        
        Args:
            id: Order ID
            amount: Refund amount (None for full refund)
            reason: Refund reason
            options: Request options
            
        Returns:
            Refund information
        """
        if not id:
            raise StatesetInvalidRequestError("Order ID is required")
        
        data = {}
        if amount is not None:
            if amount <= 0:
                raise StatesetValidationError("Refund amount must be positive")
            data["amount"] = amount
        if reason:
            data["reason"] = reason
        
        request_kwargs = options.to_kwargs() if options else {}
        
        try:
            response = await self.client.post(
                f"{self.base_path}/{id}/refund",
                json=data,
                **request_kwargs
            )
            
            # Invalidate caches
            self._invalidate_resource_caches(id)
            
            return response
        except Exception as e:
            raise StatesetValidationError(
                f"Failed to process refund for order {id}",
                detail=str(e)
            ) from e

    # Enhanced query methods using the new base resource features

    def for_customer(self, customer_id: str):
        """Get orders for a specific customer."""
        return self.query().where(customer_id=customer_id)

    def pending(self):
        """Get pending orders."""
        return self.query().status("pending")

    def completed(self):
        """Get completed orders."""
        return self.query().status("completed")

    def with_total_range(self, min_amount: float, max_amount: float):
        """Get orders within a total amount range."""
        return (self.query()
                .filter("total_amount", FilterOperator.GREATER_THAN_EQUAL, min_amount)
                .filter("total_amount", FilterOperator.LESS_THAN_EQUAL, max_amount))

    def recent(self, days: int = 7):
        """Get recent orders."""
        from datetime import datetime, timedelta
        cutoff_date = (datetime.now() - timedelta(days=days)).isoformat()
        return self.query().created_after(cutoff_date)

    def high_value(self, threshold: float = 1000.0):
        """Get high-value orders."""
        return self.query().filter("total_amount", FilterOperator.GREATER_THAN_EQUAL, threshold)

    async def get_daily_stats(
        self, 
        date: Union[str, datetime],
        options: Optional[RequestOptions] = None
    ) -> Dict[str, Any]:
        """
        Get order statistics for a specific date.
        
        Args:
            date: Date to get stats for
            options: Request options
            
        Returns:
            Daily order statistics
        """
        if isinstance(date, datetime):
            date_str = date.strftime("%Y-%m-%d")
        else:
            date_str = date
        
        request_kwargs = options.to_kwargs() if options else {}
        
        try:
            return await self.client.get(
                f"{self.base_path}/stats/daily",
                params={"date": date_str},
                **request_kwargs
            )
        except Exception as e:
            raise StatesetValidationError(
                f"Failed to get daily stats for {date_str}",
                detail=str(e)
            ) from e

    async def search_by_product(
        self, 
        product_id: str,
        options: Optional[RequestOptions] = None
    ) -> List[Order]:
        """
        Search orders containing a specific product.
        
        Args:
            product_id: Product ID to search for
            options: Request options
            
        Returns:
            List of orders containing the product
        """
        if not product_id:
            raise StatesetInvalidRequestError("Product ID is required")
        
        return await (self.query()
                     .search(f"product:{product_id}")
                     .all())

    async def bulk_update_status(
        self,
        order_ids: List[str],
        status: str,
        options: Optional[RequestOptions] = None
    ) -> Dict[str, Any]:
        """
        Update status for multiple orders in bulk.
        
        Args:
            order_ids: List of order IDs
            status: New status
            options: Request options
            
        Returns:
            Bulk operation result
        """
        if not order_ids:
            raise StatesetInvalidRequestError("Order IDs list cannot be empty")
        if not status:
            raise StatesetInvalidRequestError("Status is required")
        
        request_kwargs = options.to_kwargs() if options else {}
        
        try:
            response = await self.client.post(
                f"{self.base_path}/bulk_update_status",
                json={"order_ids": order_ids, "status": status},
                **request_kwargs
            )
            
            # Invalidate caches for all affected orders
            for order_id in order_ids:
                self._invalidate_resource_caches(order_id)
            
            return response
        except Exception as e:
            raise StatesetValidationError(
                "Failed to bulk update order statuses",
                detail=str(e)
            ) from e
