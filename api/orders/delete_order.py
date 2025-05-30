from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...stateset_types import Response


def _get_kwargs(id: str) -> Dict[str, Any]:
    """Build keyword arguments for deleting an order."""

    return {
        "method": "delete",
        "url": f"/orders/{id}",
    }


def _parse_response(*, client: Union[AuthenticatedClient, Client], response: httpx.Response) -> Optional[Any]:
    if response.status_code == HTTPStatus.BAD_REQUEST:
        return None
    if response.status_code == HTTPStatus.NOT_FOUND:
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


def sync_detailed(id: str, *, client: AuthenticatedClient) -> Response[Any]:
    """Delete order"""

    kwargs = _get_kwargs(id)
    response = client.get_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


def sync(id: str, *, client: AuthenticatedClient) -> Optional[Any]:
    """Delete order"""

    return sync_detailed(
        id=id,
        client=client,
    ).parsed


async def asyncio_detailed(id: str, *, client: AuthenticatedClient) -> Response[Any]:
    """Delete order"""

    kwargs = _get_kwargs(id)
    response = await client.get_async_httpx_client().request(**kwargs)
    return _build_response(client=client, response=response)


async def asyncio(id: str, *, client: AuthenticatedClient) -> Optional[Any]:
    """Delete order"""

    return (
        await asyncio_detailed(
            id=id,
            client=client,
        )
    ).parsed
