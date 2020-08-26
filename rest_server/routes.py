from aiohttp import web
import aiohttp_cors
import youtube


###############################################################################
# URL Routes for rest server
###############################################################################
def setup_routes(app):
    app.add_routes((
        web.view('/youtube/storedvideos',
                 youtube.StoredVideos),
        web.view('/youtube/search',
                 youtube.SearchVideos)
    ))

    cors = aiohttp_cors.setup(app, defaults={
        '*': aiohttp_cors.ResourceOptions(
         allow_credentials=True,
         expose_headers='*',
         allow_headers='*')
        }
    )

    for route in list(app.router.routes()):
        cors.add(route, webview=True)
