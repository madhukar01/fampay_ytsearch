#!/usr/bin/python3
import aiohttp
import asyncio
import copy
import datetime
from libraries import AsyncObject, PlatformDB
import os
from setup_database import setup_database
import ujson
from urllib.parse import urlencode
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
                config = ujson.load(open('config.json', 'r'))
            except Exception as e:
                print('===== Error reading configuration file =====')
                print(e)
                return

        # Assumption is that if config file is present, It is in valid format
        #   and contains required data
        self.api_keys = config['api_keys']
        self.search_config = config['search_config']
        self.api_url = config['api_url']
        self.sleep_interval = config['sleep_interval']
        self.max_data_to_fetch = config['max_data_to_fetch']

        # API Key index
        self.api_key_index = 0
        self.max_key_index = len(self.api_keys)
        self.fetched_data = 0

        if self.max_key_index < 1:
            print('No API keys found in config file',
                  'Please update the config and restart the container')

        # Initialize database
        db_config = config['db_config']
        self.platformdb = await PlatformDB(config=db_config)

        # Intiialize HTTP client
        self.session = aiohttp.ClientSession(json_serialize=ujson.dumps)

        try:
            # Start loading data
            await self.load_data()
        except Exception as e:
            print('An error occurred while loading data\n%s' % e)
        finally:
            # Close HTTP session
            await self.session.close()

    ###########################################################################
    # Load data - Starts loading data from youtube to DB
    ###########################################################################
    async def load_data(self):
        next_page_token = ''
        first_request = True

        # Keep fetching until there is no next page
        # Or max amount of data is fetched
        while next_page_token or first_request:
            response = await self.fetch_data(
                url=self.api_url,
                data=self.search_config,
                page_token=next_page_token)

            # Set first request to false
            first_request = False

            # If response status is not 200, Retry by changing keys
            while response.status != 200:
                print('Error fetching response with key: %s'
                      % self.api_key_index)
                print('Response status code: %s\n' % response.status)

                # Check if you have more keys available
                self.api_key_index += 1
                if self.api_key_index >= self.max_key_index:
                    print('Exhausted available keys')
                    print('==================================================')
                    return

                print('Retrying with key: ', self.api_key_index)
                response = await self.fetch_data(
                    url=self.api_url,
                    data=self.search_config,
                    page_token=next_page_token)

            # Decode available pages info
            response_data = await response.json()
            next_page_token = response_data.get('nextPageToken', None)
            await self.process_data(response_data)

            # Check if we have reached max data to fetch limit
            if self.fetched_data >= self.max_data_to_fetch:
                print('Data loading completed')
                print('Data loaded: ', self.max_data_to_fetch)
                print('=====================================================')
                return

            # Wait before sending next request
            print('Total data loaded: %s' % self.fetched_data)
            print('Sleeping for %d seconds' % self.sleep_interval)
            await asyncio.sleep(self.sleep_interval)

    ###########################################################################
    # Fetch data - Makes an HTTP GET request and fetches data
    ###########################################################################
    async def fetch_data(self, url, data, page_token):
        # Send request using current API key
        api_key = self.api_keys[self.api_key_index]
        data['key'] = api_key
        data['pageToken'] = page_token

        # Generate URL with query parameters
        final_url = '%s?%s' % (url, urlencode(data))

        response = await self.session.get(url=final_url)
        return response

    ###########################################################################
    # Process data - Process fetched data and insert to database
    ###########################################################################
    async def process_data(self, data):
        # Process video data elements and insert to DB
        video_elements = data.get('items', [])
        for element in video_elements:
            video_id = element.get('id', {}).get('videoId', None)
            title = element.get('snippet', {}).get('title', None)
            description = element.get('snippet', {}).get('description', None)
            thumbnails = element.get('snippet', {}).get('thumbnails', None)
            publish_time = element.get('snippet', {}).get('publishTime', None)

            # Check for validity of data
            if video_id is None\
               or title is None\
               or description is None\
               or thumbnails is None\
               or publish_time is None:
                print(video_id, title, description, thumbnails, publish_time)
                continue

            # Convert date string to timestamp
            timestamp = datetime.datetime.strptime(
                publish_time,
                '%Y-%m-%dT%H:%M:%SZ').timestamp() * 1000

            # Insert valid video to database
            await self.platformdb.insert_video(
                {
                    'video_id': video_id,
                    'title': title,
                    'description': description,
                    'thumbnails': thumbnails,
                    'timestamp': timestamp
                })
            self.fetched_data += 1


# Setup database
setup_database()

# Obtain event loop and Start data loader
loop = asyncio.get_event_loop()
loop.create_task(DataLoader())
loop.run_forever()
