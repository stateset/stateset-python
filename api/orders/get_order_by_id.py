from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.order import Order
from ...stateset_types import Response


def _get_kwargs(id: str) -> Dict[str, Any]:
    """Build keyword arguments for get_order_by_id request."""

    return {
        "method": "get",
        "url": f"/orders/{id}",
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, Order]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = Order.from_dict(response.json())
        return response_200
    if response.status_code == HTTPStatus.FORBIDDEN:
        response_403 = cast(Any, None)
        return response_403
    if response.status_code == HTTPStatus.NOT_FOUND:
        response_404 = cast(Any, None)
        return response_404
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[Union[Any, Order]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(id: str, *, client: AuthenticatedClient) -> Response[Union[Any, Order]]:
    """Get order by id"""

    kwargs = _get_kwargs(id)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(id: str, *, client: AuthenticatedClient) -> Optional[Union[Any, Order]]:
    """Get order by id"""

    return sync_detailed(id=id, client=client).parsed


async def asyncio_detailed(id: str, *, client: AuthenticatedClient) -> Response[Union[Any, Order]]:
    """Get order by id"""

    kwargs = _get_kwargs(id)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(id: str, *, client: AuthenticatedClient) -> Optional[Union[Any, Order]]:
    """Get order by id"""

    return (
        await asyncio_detailed(
            id=id,
            client=client,
        )
    ).parsed
