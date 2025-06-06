# stateset-client
A client library for accessing Stateset

## Usage
First, create a client:

```python
from stateset_client import Client

client = Client(base_url="https://api.stateset.com")
```

If the endpoints you're going to hit require authentication, use `AuthenticatedClient` instead:

```python
from stateset_client import AuthenticatedClient

client = AuthenticatedClient(base_url="https://api.stateset.com", token="SuperSecretToken")
```

Now call your endpoint and use your models:

```python
from stateset_client.models import MyDataModel
from stateset_client.api.my_tag import get_my_data_model
from stateset_client.stateset_types import Response

with client as client:
    my_data: MyDataModel = get_my_data_model.sync(client=client)
    # or if you need more info (e.g. status_code)
    response: Response[MyDataModel] = get_my_data_model.sync_detailed(client=client)
```

Or do the same thing with an async version:

```python
from stateset_client.models import MyDataModel
from stateset_client.api.my_tag import get_my_data_model
from stateset_client.stateset_types import Response

async with client as client:
    my_data: MyDataModel = await get_my_data_model.asyncio(client=client)
    response: Response[MyDataModel] = await get_my_data_model.asyncio_detailed(client=client)
```

### Using the high level `Stateset` client

The package exposes a convenience :class:`Stateset` class which reads the API key
from the ``STATESET_API_KEY`` environment variable and optionally ``STATESET_BASE_URL``.
Additional environment variables allow further configuration:

- ``STATESET_TIMEOUT`` – request timeout in seconds (default ``30``).
- ``STATESET_FOLLOW_REDIRECTS`` – set to ``false`` to disable following redirects.
- ``STATESET_VERIFY_SSL`` – set to ``false`` to disable SSL verification or provide a path to a certificate bundle.
- ``STATESET_HTTPX_PROXIES`` – proxy URL passed to ``httpx``.

```python
from stateset import Stateset

# configuration taken from the environment
client = Stateset()

# You can pass extra httpx options if needed
# client = Stateset(httpx_args={"timeout": 10.0})

# When not using a context manager, close the client explicitly
client.close()
```

Once you have a client instance you can access customer service APIs like
case tickets:

```python
async with client:
    tickets = await client.case_tickets.list()
    # Create a new order
    order = await client.orders.create({
        "customer_id": "cust_123",
        "status": "pending",
        "items": [{"product_id": "prod_456", "quantity": 1, "price": 10.0}],
        "total_amount": 10.0,
    })

    # Automatically generate a shipping label for the order
    label = await client.orders.create_shipping_label(
        order.id,
        {
            "carrier": "UPS",
            "service": "ground",
            "ship_from": {"postal_code": "94107"},
        },
    )
```

The SDK automatically sets a ``User-Agent`` header on all requests in the form
``stateset-python/<version>`` so that your integration can be identified by the
Stateset API.

By default, when you're calling an HTTPS API it will attempt to verify that SSL is working correctly. Using certificate verification is highly recommended most of the time, but sometimes you may need to authenticate to a server (especially an internal server) using a custom certificate bundle.

```python
client = AuthenticatedClient(
    base_url="https://internal_api.stateset.com", 
    token="SuperSecretToken",
    verify_ssl="/path/to/certificate_bundle.pem",
)
```

You can also disable certificate validation altogether, but beware that **this is a security risk**.

```python
client = AuthenticatedClient(
    base_url="https://internal_api.stateset.com", 
    token="SuperSecretToken", 
    verify_ssl=False
)
```

Things to know:
1. Every path/method combo becomes a Python module with four functions:
    1. `sync`: Blocking request that returns parsed data (if successful) or `None`
    1. `sync_detailed`: Blocking request that always returns a `Request`, optionally with `parsed` set if the request was successful.
    1. `asyncio`: Like `sync` but async instead of blocking
    1. `asyncio_detailed`: Like `sync_detailed` but async instead of blocking

1. All path/query params, and bodies become method arguments.
1. If your endpoint had any tags on it, the first tag will be used as a module name for the function (my_tag above)
1. Any endpoint which did not have a tag will be in `stateset_client.api.default`
1. Every resource class includes an `iter_all` method to iterate through all
   pages of results, and a `list_all` helper that returns a full list.

## Advanced customizations

There are more settings on the generated `Client` class which let you control more runtime behavior, check out the docstring on that class for more info. You can also customize the underlying `httpx.Client` or `httpx.AsyncClient` (depending on your use-case):

```python
from stateset_client import Client

def log_request(request):
    print(f"Request event hook: {request.method} {request.url} - Waiting for response")

def log_response(response):
    request = response.request
    print(f"Response event hook: {request.method} {request.url} - Status {response.status_code}")

client = Client(
    base_url="https://api.stateset.com",
    httpx_args={"event_hooks": {"request": [log_request], "response": [log_response]}},
)

# Or get the underlying httpx client to modify directly with client.get_httpx_client() or client.get_async_httpx_client()
```

You can even set the httpx client directly, but beware that this will override any existing settings (e.g., base_url):

```python
import httpx
from stateset_client import Client

client = Client(
    base_url="https://api.stateset.com",
)
# Note that base_url needs to be re-set, as would any shared cookies, headers, etc.
client.set_httpx_client(httpx.Client(base_url="https://api.stateset.com", proxies="http://localhost:8030"))
async_client = httpx.AsyncClient(base_url="https://api.stateset.com", proxies="http://localhost:8030")
client.set_async_httpx_client(async_client)
```

## Building / publishing this package
This project uses [Poetry](https://python-poetry.org/) to manage dependencies  and packaging.  Here are the basics:
1. Update the metadata in pyproject.toml (e.g. authors, version)
1. If you're using a private repository, configure it with Poetry
    1. `poetry config repositories.<your-repository-name> <url-to-your-repository>`
    1. `poetry config http-basic.<your-repository-name> <username> <password>`
1. Publish the client with `poetry publish --build -r <your-repository-name>` or, if for public PyPI, just `poetry publish --build`

If you want to install this client into another project without publishing it (e.g. for development) then:
1. If that project **is using Poetry**, you can simply do `poetry add <path-to-this-client>` from that project
1. If that project is not using Poetry:
    1. Build a wheel with `poetry build -f wheel`
    1. Install that wheel from the other project `pip install <path-to-wheel>`
