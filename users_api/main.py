import logging

from aiohttp import web


async def init_app():
    logging.basicConfig(level=logging.DEBUG)
    app = web.Application()

    return app
