import requests
import os

import requests_cache

requests_cache.install_cache()

def get_event(keyword):
    key = os.environ.get('EVENTS_KEY')

    try:
        query = {'keywords':keyword, 'l':'minneapolis', 'date':'all', 'app_key': key}
        url = 'http://api.eventful.com/json/events/search?'

        data = requests.get(url, params=query).json()
        print(data)
    except requests.exceptions.HTTPError as http_error:
        print("There's a Http Error", http_error)
    except requests.exceptions.ConnectionError as conn:
        print("There's a connection error", conn)
    except requests.exceptions.Timeout as timeout:
        print("There is a timeout Error", timeout)
    except requests.exceptions.RequestException as error:
        print("Something went wrong", error)

    return data

# get_event('first avenue')