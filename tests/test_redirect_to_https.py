from asgi_lifespan import LifespanManager
from datasette.app import Datasette
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
