import asyncio
from aiohttp import web
import os
from routes import setup_routes
from startup import setup_modules
import uvloop

# Set uvloop as default loop for asyncio
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

# Set debug
loop = asyncio.get_event_loop()
loop.set_debug(True)

# AIO Web App
app = web.Application()


# Perform one time setup of requirements on every startup event
app.on_startup.append(setup_modules)

# Pass the web app to setup routes
setup_routes(app)

# Run the app
web.run_app(app, host='localhost', port='4001')
