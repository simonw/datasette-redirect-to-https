from datasette import hookimpl
from functools import wraps


def _check_headers(scope, if_headers):
    headers = {k.lower(): v for k, v in scope["headers"]}
    for key, value in if_headers.items():
        if headers.get(key.encode("utf-8")) == value.encode("utf-8"):
            return True


@hookimpl
def asgi_wrapper(datasette):
    config = datasette.plugin_config("datasette-redirect-to-https") or {}
    if_headers = config.get("if_headers") or {}
    check = lambda scope: scope["scheme"] == "http"
    if if_headers:
        check = lambda scope: _check_headers(scope, if_headers)

    def wrap_with_redirect_to_https(app):
        @wraps(app)
        async def redirect_to_https(scope, receive, send):
            if scope.get("type") != "http" or "scheme" not in scope:
                return await app(scope, receive, send)
            if check(scope):
                url = b"https://" + dict(scope["headers"])[b"host"]
                if scope.get("raw_path"):
                    url += scope["raw_path"]
                else:
                    url += scope["path"].decode("utf-8")
                if scope["query_string"]:
                    url += b"?" + scope["query_string"]
                if scope["method"] != "GET":
                    await send(
                        {
                            "type": "http.response.start",
                            "status": 405,
                            "headers": [["content-type", "text/html"]],
                        }
                    )
                    await send(
                        {
                            "type": "http.response.body",
                            "body": (
                                "<h1>Bad method: {}</h1>\n".format(
                                    scope["method"]
                                ).encode("utf-8")
                                + b"<p>You should talk to the <code>https</code> endpoint instead.</p>"
                            ),
                        }
                    )
                    return
                await send(
                    {
                        "type": "http.response.start",
                        "status": 301,
                        "headers": [["location", url]],
                    }
                )
                await send({"type": "http.response.body", "body": b""})
            else:
                await app(scope, receive, send)

        return redirect_to_https

    return wrap_with_redirect_to_https
