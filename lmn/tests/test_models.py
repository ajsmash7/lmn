from django.test import TestCase
from lmn.models import Artist, Venue, Show, Note
from django.contrib.auth.models import User
from django.db import IntegrityError
# Create your tests here.


class TestUser(TestCase):

    def test_create_user_duplicate_username_fails(self):

        user = User(username='bob', email='bob@bob.com', first_name='bob', last_name='bob')
        user.save()

        user2 = User(username='bob', email='another_bob@bob.com', first_name='bob', last_name='bob')
        with self.assertRaises(IntegrityError):
            user2.save()


    def test_create_user_duplicate_username_case_insensitive_fails(self):

        user = User(username='bob', email='bob@bob.com', first_name='bob', last_name='bob')
        user.save()

        user2 = User(username='Bob', email='another_bob@bob.com', first_name='bob', last_name='bob')
        with self.assertRaises(IntegrityError):
            user2.save()


    def test_create_user_duplicate_email_fails(self):
        user = User(username='bob', email='bob@bob.com', first_name='bob', last_name='bob')
        user.save()

        user2 = User(username='bob', email='bob@bob.com', first_name='bob', last_name='bob')
        with self.assertRaises(IntegrityError):
            user2.save()


    def test_create_user_duplicate_email_case_insensitive_fails(self):
        user = User(username='bob', email='bob@bob.com', first_name='bob', last_name='bob')
        user.save()

        user2 = User(username='another_bob', email='Bob@bob.com', first_name='bob', last_name='bob')
        with self.assertRaises(IntegrityError):
            user2.save()

class TestArtist(TestCase):

    def test_can_add_Artist(self):
        artist = Artist(name='Tom Petty')
        artist.save()
        self.assertEquals(artist, 'Tom Petty')

    def test_add_Artist_duplicate_fails(self):
        artist = Artist(name='Tom Petty')
        artist.save()
        artist2 = Artist(name='Tom Petty')
        with self.assertRaises(IntegrityError):
            artist2.save()


class TestVenue(TestCase):

    def test_can_add_venue(self):
        venue = Venue(name='First Avenue', city='Minneapolis', state='MN')
        venue.save()
        data = {'name': 'First Avenue', 'city': 'Minneapolis', 'state': 'MN'}
        self.assertEquals(venue, data)

    def test_fails_for_duplicate_venue_name(self):
        venue = Venue(name='First Avenue', city='Minneapolis', state='MN')
        venue.save()
        venue2 = Venue(name='First Avenue', city='Minneapolis', state='MN')
        with self.assertRaises(IntegrityError):
            venue2.save()

class TestShow(TestCase):

    def test_can_add_show(self):
        # add a venue, then an artist, then create a show. compare to dictionary data
        venue = Venue(name='First Avenue', city='Minneapolis', state='MN')
        venue.save()
        artist = Artist(name='Tom Petty')
        artist.save()
        show = Show(show_id=1, show_date='2017-01-21 07:00 PM', artist=artist, venue=venue)
        data = {'show_id': 1, 'show_date': '2017-01-21 07:00 PM', 'artist' : {'name': 'Tom Petty'}, 'venue': {'name': 'First Avenue', 'city': 'Minneapolis', 'state': 'MN'}}
        self.assertEquals(show, data)



