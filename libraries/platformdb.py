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

    ###########################################################################
    # Get vidoes - ordered by time
    ###########################################################################
    async def get_videos(self, limit):
        return await self.videos.order_by(self.db.desc('timestamp'))\
            .limit(limit).run(self.conn)

    ###########################################################################
    # Get count of stored videos
    ###########################################################################
    async def get_videos_count(self):
        return await self.videos.count().run(self.conn)

    ###########################################################################
    # Search videos
    ###########################################################################
    async def search_videos(self, query_string, limit):
        query_string = '.*%s.*' % query_string.strip().lower()
        return await self.videos.filter(
            lambda video:
                video['title'].downcase().match(query_string) |
                video['description'].downcase().match(query_string))\
            .limit(limit).order_by(self.db.desc('timestamp')).run(self.conn)
