# YouTube Videos Loader and Search

### How to run
- Clone this repository `git clone https://github.com/madhukar01/fampay_ytsearch`
- Edit the configuration file `config.json` for loading data from youtube
    - Replace `api_keyX` placeholder with actual API keys for Youtube data API
    (supports multiple keys, switches keys when quota is exhausted)
    - For other options, scroll down to editing config file section
- Build the docker image
    - `cd fampay_ytsearch`
    - `docker build . --tag platform-base`
- Start docker containers `docker-compose -f docker-compose.yaml up`
- You can see the status in docker log
- This will run a REST API on http://localhost:4001

### API Spec
- Stored data with pagination `/youtube/storedvideos`
    - Request Type: GET
    - Parameter:
        - `pagenumber` - Integer, Defaults to 1 if missing
    - Page size is set to 10
    - Sample request `http://localhost:4001/youtube/storedvideos?pagenumber=1`
    - Sample response:
        ```
        {
            "available_pages": x,       # Number of available pages,
            "page_number": x,           # Current page number,
            "data_in_current_page": x,  # Number of videos in current page,
            "videos": [x, y, z]         # Array of video elements sorted in descending order of publish timestamp
        }
        ```
    - Videos array will be empty if there are no videos in current page

- Search videos `/youtube/search`
    - Request Type: GET
    - Parameters:
        - `query` - String, Required, String to search
        - `maxresults` - Integer, Defaults to 10 if missing
    - Sample request `http://localhost:4001/youtube/search?query=miracle&maxresults=5`
    - Sample response:
        ```
        {
            'search_results': [x, y, z] # Array of video elements
        }
        ```
    - Search results will be empty if there are no videos with matching Title / Prescription found in database  
    (Strongly coupled search - Regex based, in the order of words in query)


### Assumptions
- Data loader assumes that if the above mentioned config file `config.json` is present,
It is in valid format and contains required data.  
Validation of the config is not done, Please edit with your own risk :)

### Editing Configuration file
- Minimum requirement to run the project is to replace `api_keyX` in config
- `search_config: maxResults` - Number of results to fetch with each API call (0-50)
- `search_config: order` - Sorting order of results from youtube data API
- `search_config: publishedAfter` - Fetch videos that are published after this timestamp
- `search_config: q` - Query string to search for loading data
- `sleep_interval` - Interval to sleep (in seconds) between subsequent API call
- `max_data_to_fetch` - Total count of videos to fetch (Each API key allows count of 10000 per day, Please use this accordingly to control usgae quota)