from libraries import PlatformDB


###############################################################################
# Setup any modules required for rest server - called during startup
###############################################################################
async def setup_modules(app):
    # Initialize modules
    app['platformdb'] = await PlatformDB()
