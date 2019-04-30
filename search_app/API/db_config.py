import os
import psycopg2
from dataclasses import dataclass

DATABASE_URL = "postgres://gvrspwekjkerog:c00096be3f966f639c2e28716123f1d10745aea81b0bc9fff250bc0b021cc6b2@ec2-50-19-127-115.compute-1.amazonaws.com:5432/d1mqvenhan49li"

## I do not know in what format you pull data from the api. Likely you will use a for loop for each line in the dictionary. The parameters in these paranthesis you need to get from the api
@dataclass
class Venue:
    name: str
    city: str
    state: str

artist_insert = "INSERT INTO Artist (name) VALUES (%s);"
venue_insert = "INSERT INTO Venue (name, city, state) VALUES (%s, %s, %s);"
show_insert = "INSERT INTO Show (show_id, show_date, artist, venue) VALUES (%s, %s, %s, %s);"

def add_record(artist, venue_name, city, state, show_id, show_date):
    show_artist = add_artist(artist)
    show_venue = add_venue(venue_name, city, state)
    add_show(show_id, show_date, show_artist, show_venue)

def add_artist(artist):
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute(artist_insert, artist)

        return artist

        conn.close()
    except psycopg2.IntegrityError:
        return artist
    except psycopg2.Error as e:
        raise EventError("Not a duplicate, but cannot add artist to database") from e

def add_venue(name, city, state):
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute(venue_insert, (name, city, state))

        venue = Venue(name, city, state)
        return venue
        conn.close()
    except psycopg2.IntegrityError:
        return Venue (name, city, state)
    except psycopg2.Error as e:
        raise EventError("Not a duplicate, but cannot add venue to database") from e

def add_show(id, date, artist, venue):

    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode='require')
        cur = conn.cursor()
        cur.execute(show_insert, (id, date, artist, venue))
        conn.close()

    except psycopg2.IntegrityError:
            print("Show already exists!")
    except psycopg2.Error as e:
            raise EventError("Not a duplicate, but cannot add show to database") from e
class EventError(Exception):
    #for raising errors
    pass
