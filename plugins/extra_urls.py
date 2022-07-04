from datasette import hookimpl

# from datasette.utils.asgi import asgi_send
# from functools import wraps
from datasette.utils.asgi import Response


robots_text = """User-agent: *
Disallow: /
Allow: /$
Allow: /politics
Allow: /about
Allow: /fora
"""


async def robots():
    return Response.text(robots_text)


@hookimpl
def register_routes():
    return [(r"^/robots.txt$", robots)]
