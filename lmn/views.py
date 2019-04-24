from django.shortcuts import render
import eventful
from .models import Show, Artist, Venue

def homepage(request):

    api = eventful.API('S3Zr3tsQKMVtCMGk')

    # If you need to log in:
    # api.login('username', 'password')

    events = api.call('/events/search', q='music', l='Minneapolis')
    for event in events['events']['event']:
        # Venue(event['venue_name'], event['city_name'], event['region_abbr'])
        performers = event['performers']['performer']
        for performer in performers['performers']['performer']:
            # Artist(performer['name'])
            Show(event['id'], event['start_time'], Venue(event['venue_name'], event['city_name'], event['region_abbr']), Artist(performer['name']))
    return render(request, 'lmn/home.html')
