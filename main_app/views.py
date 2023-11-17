from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Game, Review
from .serializers import UserSerializer, GroupSerializer, GameSerializer, ReviewSerializer

class UserViewSet(viewsets.ReadOnlyModelViewSet): #will display the whole model and even edit data from an 
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated] # if not authenticated we can't consume API

class GroupViewSet(viewsets.ReadOnlyModelViewSet): 
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class GameViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [permissions.IsAuthenticated]

class ReviewViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

#USER
class CreateUserAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message':'user created ok', 'user_data':serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)