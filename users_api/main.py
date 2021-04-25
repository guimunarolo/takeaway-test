import logging

from aiohttp import web

from .routes import init_routes


async def init_app():
    logging.basicConfig(level=logging.DEBUG)
    app = web.Application()
    init_routes(app)

    return app
