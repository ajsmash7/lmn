from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Artist, Venue, Show, Note


class ArtistSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(required=True, allow_blank=False, max_length=200)

    class Meta:
        model = Artist

    def create(self, validated_data):
        """
        Create and return a new Artist instance with the validated data.
        """
        return Artist.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return current Artist instance with data, if existing.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.save()
        return instance


class VenueSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(max_length=200, allow_blank=False, required=True)
    city = serializers.CharField(max_length=200, allow_blank=False)
    state = serializers.CharField(max_length=2, allow_blank=False)

    class Meta:
        model = Venue

    def create(self, validated_data):
        """
        Create and return a new Venue instance with the validated data.
        """
        return Venue.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return current Venue instance with data, if existing.
        """
        instance.name = validated_data.get('name', instance.name)
        instance.city = validated_data.get('city', instance.city)
        instance.state = validated_data.get('state', instance.state)
        instance.save()
        return instance


class ShowSerializer(serializers.Serializer):
    show_id = serializers.CharField(max_length=200, allow_blank=False)
    show_date = serializers.DateTimeField()
    artist = serializers.PrimaryKeyRelatedField(many=True, queryset=Artist.name.all())
    venue = serializers.PrimaryKeyRelatedField(many=True, queryset=Venue.object.all())

    class Meta:
        model = Show


    def create(self, validated_data):
        """
        Create and return a new Venue instance with the validated data.
        """
        return Show.objects.create(**validated_data)

    def update(self, instance: Show, validated_data):
        """
        Update and return current Venue instance with data, if existing.
        :type instance: Show
        """
        instance.name = validated_data.get('name', instance.name)
        instance.city = validated_data.get('city', instance.city)
        instance.state = validated_data.get('state', instance.state)
        instance.save()
        return instance

 class UserSerializer(serializers.ModelSerializer):
    user_notes = serializers.PrimaryKeyRelatedField(many=True, queryset=Note.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'user_notes')

