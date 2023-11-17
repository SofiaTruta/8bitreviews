from django.contrib.auth.models import User, Group
from .models import Game, Review
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['url', 'username', 'password', 'email', 'first_name', 'last_name']

    def create(self, data):
        user = User.objects.create_user(**data)
        return user


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

class GameSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Game
        fields = ['id', 'title', 'genre', 'description', 'release_date', 'cover_url', 'user']

class ReviewSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'score', 'date_submitted', 'user', 'game']

