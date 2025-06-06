from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.order import Order
from ...stateset_types import Response


def _get_kwargs(*, json_body: Order) -> Dict[str, Any]:
    """Build keyword arguments for the request."""

    json_json_body = json_body.to_dict()

    return {
        "method": "post",
        "url": "/orders",
        "json": json_json_body,
    }


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Any]:
    if response.status_code == HTTPStatus.CREATED:
        return None
    if response.status_code == HTTPStatus.BAD_REQUEST:
        return None
    if response.status_code == HTTPStatus.METHOD_NOT_ALLOWED:
        return None
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Response[Any]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(*, client: AuthenticatedClient, json_body: Order) -> Response[Any]:
    """Create a new order"""

    kwargs = _get_kwargs(json_body=json_body)

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(*, client: AuthenticatedClient, json_body: Order) -> Optional[Any]:
    """Create a new order"""

    return sync_detailed(
        client=client,
        json_body=json_body,
    ).parsed


async def asyncio_detailed(*, client: AuthenticatedClient, json_body: Order) -> Response[Any]:
    """Create a new order"""

    kwargs = _get_kwargs(json_body=json_body)

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(*, client: AuthenticatedClient, json_body: Order) -> Optional[Any]:
    """Create a new order"""

    return (
        await asyncio_detailed(
            client=client,
            json_body=json_body,
        )
    ).parsed
