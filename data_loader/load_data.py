#!/usr/bin/python3
import aiohttp
import asyncio
import copy
from libraries import AsyncObject, PlatformDB
import os
import ujson
import uvloop


###############################################################################
# Data Loader
###############################################################################
class DataLoader(AsyncObject):
    '''
    Module to load videos data into database
    '''
    async def __init__(self):
        # Read config file - check if exist
        if not os.path.exists('config.json'):
            print('===== Unable to fetch configuration file =====')
            return
        else:
            try:
                config = ujson.loads(open('config.json', 'r'))
            except Exception as e:
                print('===== Error reading configuration file =====')
                print(e)
                return

        # Assumption is that if config file is present, It is in valid format
        #   and contains required data
        self.db_config = config['db_config']
        self.api_keys = config['api_keys']
        self.search_config = config['search_config']
        self.api_url = config['api_url']
        self.sleep_interval = config['sleep_interval']

        # API Key index
        self.api_key_index = 0
        self.max_key_index = len(self.api_keys)

        # Initialize database
        # self.platformdb = await PlatformDB(config=db_config)

        # Intiialize HTTP client
        self.session = aiohttp.ClientSession(json_serialize=ujson.dumps)

        # Start loading data
        await self.load_data()

    ###########################################################################
    # Load data - Starts loading data from youtube to DB
    ###########################################################################
    async def load_data(self):
        api_key = self.api_keys[self.api_key_index]
        data = copy.deepcopy(self.search_config)
        data['token'] = api_key

        response = await self.fetch_data(
            url=self.api_url,
            data=data)
        print(await response.json())

    ###########################################################################
    # Fetch data - Makes an HTTP GET request and fetches data
    ###########################################################################
    async def fetch_data(self, url, data):
        response = await self.session.get(
            url=self.api_url,
            data=ujson.dumps(data))
        print(response.status)
        return response


# Obtain event loop and Start data loader
loop = asyncio.get_event_loop()
loop.create_task(DataLoader())
loop.run_forever()
