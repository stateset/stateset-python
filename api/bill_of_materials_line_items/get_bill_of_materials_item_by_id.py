from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.bill_of_materials_line_item import BillOfMaterialsLineItem
from ...stateset_types import UNSET, Response


def _get_kwargs(
    *,
    limit: float,
    offset: float,
    order_direction: str,
) -> Dict[str, Any]:
    pass

    params: Dict[str, Any] = {}
    params["limit"] = limit

    params["offset"] = offset

    params["order_direction"] = order_direction

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "get",
        "url": "/billofmaterialsitems",
        "params": params,
    }


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[Union[Any, BillOfMaterialsLineItem]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = BillOfMaterialsLineItem.from_dict(response.json())

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
) -> Response[Union[Any, BillOfMaterialsLineItem]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    limit: float,
    offset: float,
    order_direction: str,
) -> Response[Union[Any, BillOfMaterialsLineItem]]:
    """Get bill of materials item by id

     Some description of the operation.
    You can use `Markdown` here.

    Args:
        limit (float):
        offset (float):
        order_direction (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, BillOfMaterialsLineItem]]
    """

    kwargs = _get_kwargs(
        limit=limit,
        offset=offset,
        order_direction=order_direction,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    limit: float,
    offset: float,
    order_direction: str,
) -> Optional[Union[Any, BillOfMaterialsLineItem]]:
    """Get bill of materials item by id

     Some description of the operation.
    You can use `Markdown` here.

    Args:
        limit (float):
        offset (float):
        order_direction (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, BillOfMaterialsLineItem]
    """

    return sync_detailed(
        client=client,
        limit=limit,
        offset=offset,
        order_direction=order_direction,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    limit: float,
    offset: float,
    order_direction: str,
) -> Response[Union[Any, BillOfMaterialsLineItem]]:
    """Get bill of materials item by id

     Some description of the operation.
    You can use `Markdown` here.

    Args:
        limit (float):
        offset (float):
        order_direction (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, BillOfMaterialsLineItem]]
    """

    kwargs = _get_kwargs(
        limit=limit,
        offset=offset,
        order_direction=order_direction,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    limit: float,
    offset: float,
    order_direction: str,
) -> Optional[Union[Any, BillOfMaterialsLineItem]]:
    """Get bill of materials item by id

     Some description of the operation.
    You can use `Markdown` here.

    Args:
        limit (float):
        offset (float):
        order_direction (str):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[Any, BillOfMaterialsLineItem]
    """

    return (
        await asyncio_detailed(
            client=client,
            limit=limit,
            offset=offset,
            order_direction=order_direction,
        )
    ).parsed
