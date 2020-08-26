from aiohttp import web
from aiohttp_cors import CorsViewMixin
import math
import ujson
from webargs import fields
from webargs.aiohttpparser import parser


# Parameter validation
handler_args = {
                    # pagenumber (integer) - pagenumber
                    'pagenumber': fields.Int(missing=1),
                }


###############################################################################
# GET Stored videos
###############################################################################
class StoredVideos(web.View, CorsViewMixin):
    '''
    GET Stored Videos
    '''
    async def get(self):
        # Parse request data
        args = await parser.parse(handler_args, self.request)

        # Static page size 10
        page_size = 10
        page_number = args['pagenumber']

        if page_number < 1:
            page_number = 1

        # Fetch data from DB
        limit = page_size * page_number
        videos = await self.request.app['platformdb']\
            .get_videos(limit)
        if videos is None:
            videos = []

        # Remove data from previous page
        slice_index = (page_number - 1) * page_size
        if len(videos) < slice_index:
            videos = []
        else:
            videos = videos[slice_index:]

        # Fetch available videos count from DB
        available_data = await self.request.app['platformdb']\
            .get_videos_count()
        available_pages = math.ceil(available_data / page_size)

        return_data = {
            'available_pages': available_pages,
            'page_number': page_number,
            'data_in_current_page': len(videos),
            'videos': videos
        }
        return web.json_response(
            status=200,
            data=return_data,
            dumps=ujson.dumps)
