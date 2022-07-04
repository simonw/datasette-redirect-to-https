from asgi_lifespan import LifespanManager
from datasette.app import Datasette
from datasette.utils import PrefixedUrlString
import httpx
import pytest


@pytest.mark.asyncio
@pytest.mark.parametrize("path", ["/", "/-/versions", "/-/versions.json"])
async def test_http_get_redirects_to_https(path):
    datasette = Datasette([], memory=True)
    response = await datasette.client.get(path)
    assert response.status_code == 301
    assert response.headers["location"] == "https://localhost{}".format(path)
    assert response.text == ""


@pytest.mark.asyncio
@pytest.mark.parametrize("path", ["/", "/-/versions", "/-/versions.json"])
async def test_https_get_does_not_redirect(path):
    datasette = Datasette([], memory=True)
    async with LifespanManager(datasette.app()):
        async with httpx.AsyncClient(app=datasette.app()) as client:
            response = await client.get("https://localhost{}".format(path))
    assert response.status_code == 200
    assert response.text


@pytest.mark.asyncio
@pytest.mark.parametrize("method", ("post", "options", "put"))
async def test_other_methods_return_405(method):
    datasette = Datasette([], memory=True)
    response = await getattr(datasette.client, method)("/")
    assert response.status_code == 405
    assert response.text == (
        "<h1>Bad method: {}</h1>\n".format(method.upper())
        + "<p>You should talk to the <code>https</code> endpoint instead.</p>"
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "if_headers,scope_scheme,request_headers,should_redirect",
    (
        (None, "http", {}, True),
        (None, "https", {}, False),
        ({"x-forwarded-proto": "http"}, "http", {"x-forwarded-proto": "http"}, True),
        ({"x-forwarded-proto": "http"}, "http", {"x-forwarded-proto": "https"}, False),
        ({"x-forwarded-proto": "http", "x-y-z": "xyz"}, "http", {}, False),
        ({"x-forwarded-proto": "http"}, "http", {"x-forwarded-proto": "https"}, False),
        ({"x-forwarded-proto": "http", "x-y-z": "xyz"}, "http", {"x-y-z": "xyz"}, True),
        ({"x-forwarded-proto": "http", "x-y-z": "xyz"}, "http", {}, False),
    ),
)
async def test_if_headers_config(
    if_headers, scope_scheme, request_headers, should_redirect
):
    datasette = Datasette(
        metadata={
            "plugins": {
                "datasette-redirect-to-https": {
                    "if_headers": if_headers,
                }
            }
        }
    )
    response = await datasette.client.get(
        PrefixedUrlString("{}://localhost/".format(scope_scheme)),
        headers=request_headers,
    )
    if should_redirect:
        assert response.status_code == 301
    else:
        assert response.status_code == 200
