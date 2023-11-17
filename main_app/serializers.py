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

# GROUP
class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']

# GAME
class GameSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    class Meta:
        model = Game
        fields = ['id', 'title', 'genre', 'description', 'release_date', 'cover_url', 'user']

# REVIEW
class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    game = serializers.PrimaryKeyRelatedField(queryset=Game.objects.all())
    class Meta:
        model = Review
        fields = ['id', 'score', 'review','date_submitted', 'user', 'game']

