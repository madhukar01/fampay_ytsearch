import asyncio
from .async_object import AsyncObject
from rethinkdb import RethinkDB


###############################################################################
# Database module
###############################################################################
class PlatformDB(AsyncObject):
    '''
    Platform database module
    '''
    async def __init__(self, config={}):
        # Fetch configuration from Redis server
        host = config.get('host', 'localhost')
        port = config.get('port', 28015)
        db_name = config.get('db_name', 'platform')

        # Connect to RethinkDB
        self.db = RethinkDB()
        self.db.set_loop_type(library='asyncio')
        self.conn = await self.db.connect(host=host,
                                          port=port,
                                          db=db_name)

        # Videos table
        self.videos = self.db.table('videos')

    ###########################################################################
    # Insert a video
    ###########################################################################
    async def insert_video(self, data):
        return await self.videos.insert(data).run(self.conn)
