from aiohttp import web
from aiohttp_cors import CorsViewMixin
import ujson
from webargs import fields
from webargs.aiohttpparser import parser


# Parameter validation
handler_args = {
                    # query (string) - query string to search
                    'query': fields.Str(required=True),
                    'maxresults': fields.Int(missing=10)
                }


###############################################################################
# GET Search videos
###############################################################################
class SearchVideos(web.View, CorsViewMixin):
    '''
    GET Search videos
    '''
    async def get(self):
        # Parse request data
        args = await parser.parse(handler_args, self.request)

        query_string = args['query']
        max_results = args['maxresults']

        # Get search results from database
        results = await self.request.app['platformdb']\
            .search_videos(
                query_string=query_string,
                limit=max_results)
        if results is None:
            results = []

        return_data = {
            'search_results': results
        }
        return web.json_response(
            status=200,
            data=return_data,
            dumps=ujson.dumps)
