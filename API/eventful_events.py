import requests
import os
import json

# import requests_cache

# requests_cache.install_cache()

def get_event(keyword):
    key = os.environ.get('EVENTS_KEY')

    try:
        query = {'q':keyword, 'l':'minneapolis', 'date':'all', 'app_key': key}
        url = 'http://api.eventful.com/json/events/search?'

        data = requests.get(url, params=query).json()
        res= data['events']['event']

        # print(res)
        # for ev in res:
        #     if ev.get('performers')is not None:
        #         artist = ev['performers']['performer']['name']
        #         venue_name = ev['venue_name']
        #         city =ev['city_name']
        #         state =ev['region_name']
        #         show_id =ev['id']
        #         show_date =ev['start_time']
        #         print(venue_name,artist)



    except requests.exceptions.HTTPError as http_error:
        print("There's a Http Error", http_error)
    except requests.exceptions.ConnectionError as conn:
        print("There's a connection error", conn)
    except requests.exceptions.Timeout as timeout:
        print("There is a timeout Error", timeout)
    except requests.exceptions.RequestException as error:
        print("Something went wrong", error)

    return res

# get_event('first avenue')