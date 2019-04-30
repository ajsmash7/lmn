from django.shortcuts import render
from search_app.API.eventful_events import get_event
from search_app.API.db_config import add_record
from django.db.models import Q
# Create your views here.
def searchResult(request):
    query = None
    if 'q' in request.GET:
        query = request.GET.get('q')
        # print(query)
        # q='first avenue'
        res = get_event(query)
        print (res)
        events_data = []
        for event in res:
            if event.get('performers') is not None:
                events = {'show_id': event['id'],
                          # 'show' : event['title'],
                          'artist': event['performers']['performer']['name'],
                          'venue': event['venue_name'],
                          'city': event['city_name'],
                          'state': event['region_abbr'],
                          'date': event['start_time']
                          }
                events_data.append(events)
    print(events_data)
    load_data(events_data)
    return render(request, 'search.html', {'query': query, 'events_data': events_data})

def load_data(data):
    for event in data:
        add_record(artist=event['artist'], venue_name=event['venue'],
                   city=event['city'],state=event['state'],show_id=event['show_id'], show_date=['showdate'])