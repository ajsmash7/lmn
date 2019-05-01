from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Artist, Venue, Show, Note


class ArtistSerializer(serializers.ModelSerializer):

    class Meta:
        model = Artist
        fields = '__all__'


class VenueSerializer(serializers.ModelSerializer):


    class Meta:
        model = Venue
        fields = '__all__'



class ShowSerializer(serializers.ModelSerializer):
    artist = ArtistSerializer()
    venue = VenueSerializer()

    def create(self, validated_data):
        venue = Venue(name=validated_data['venue']['name'], city=validated_data['venue']['city'], state=validated_data['venue']['state'])
        artist = Artist(name=validated_data['artist']['name'])
        show = Show(show_id=validated_data['show_id'], show_date=validated_data['show_date'], artist=artist, venue=venue)
        return show

    class Meta:
        model = Show
        fields = '__all__'

