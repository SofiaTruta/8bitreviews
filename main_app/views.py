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
    

#GAME
class CreateGameAPIView(APIView):
    def post(self, request):
        serializer = GameSerializer(data=request.data)
        if serializer.is_valid():
            game = serializer.save()
            return Response({'message':'game created ok', 'user_data':serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class EditGameAPIView(APIView):
    def put(self, request, game_id):
        try:
            game = Game.objects.get(pk=game_id)
        except (Game.DoesNotExist):
            return Response({"error": "Game not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if game:
            serializer = GameSerializer(game, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
# REVIEW
class CreateReviewAPIView(APIView):
    def post(self, request, game_id):
        try:
            game = Game.objects.get(pk=game_id)
        except Game.DoesNotExist:
            return Response({'error': 'Game not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(game=game, user=request.user)
            return Response({"message": "Review created ok", 'review_data':serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ReviewAPIView(APIView):
    def delete(self, request, game_id, review_id):
        try:
            game = Game.objects.get(pk=game_id)
            review = Review.objects.get(pk=review_id, game=game)
        except (Game.DoesNotExist, Review.DoesNotExist):
            return Response({"error": "Review or Game not found"}, status=status.HTTP_404_NOT_FOUND)
        review.delete()
        return Response({"message": "Review deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    
    def put(self, request, game_id, review_id):
        try:
            game = Game.objects.get(pk=game_id)
            review = Review.objects.get(pk=review_id, game=game)
        except (Game.DoesNotExist, Review.DoesNotExist):
            return Response({"error": "Review or Game not found"}, status=status.HTTP_404_NOT_FOUND)
        
        if review:
            serializer = ReviewSerializer(review, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)