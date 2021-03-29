from datasette import hookimpl
from functools import wraps


@hookimpl
def asgi_wrapper(datasette):
    def wrap_with_cache_header(app):
        @wraps(app)
        async def add_cache_header(scope, recieve, send):
            async def wrapped_send(event):
                if not event["type"] == "http.response.start":
                    await send(event)
                    return

                original_headers = event.get("headers") or []
                new_headers = [
                    [key, value]
                    for key, value in original_headers
                    if key.lower() != b"cache-control"
                ]
                new_headers.append(
                    [b"cache-control", b"max-age=86400"]
                )  # Later use 604800 one week
                await send({**event, **{"headers": new_headers}})

            await app(scope, recieve, wrapped_send)

        return add_cache_header

    return wrap_with_cache_header
