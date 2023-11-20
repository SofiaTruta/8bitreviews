from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.core.cache import cache
from django.middleware.csrf import get_token

from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authentication import TokenAuthentication

from .models import Game, Review
from .serializers import UserSerializer, GroupSerializer, GameSerializer, ReviewSerializer


# just grabbing information
class UserViewSet(viewsets.ReadOnlyModelViewSet): #will display the whole model and even edit data from an 
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated] # if not authenticated we can't consume API
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        user_serializer = self.get_serializer(instance)
        games_serializer = GameSerializer(instance.game_set.all(), many=True)
        reviews_serializer = ReviewSerializer(instance.reviews.all(), many=True)

        response_data = {
            'user': user_serializer.data,
            'games': games_serializer.data,
            'reviews': reviews_serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)


class GroupViewSet(viewsets.ReadOnlyModelViewSet): 
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]

class GameViewSet(viewsets.ModelViewSet):
    queryset = Game.objects.all()
    serializer_class = GameSerializer
    permission_classes = [permissions.IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        game_serializer = self.get_serializer(instance)
        reviews_serializer = ReviewSerializer(instance.reviews.all(), many=True)

        response_data = {
            'game': game_serializer.data,
            'reviews': reviews_serializer.data
        }
        return Response(response_data, status=status.HTTP_200_OK)

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

# class UserDetailView(APIView):
#     def get(self, request, pk):
#         try:
#             user = User.objects.get(pk=pk)
#             print(user)
#             user_serializer = UserSerializer(user)
#             games_serializer = GameSerializer(user.game_set.all(), many=True)
#             reviews_serializer = ReviewSerializer(user.reviews.all(), many=True)

#             response_data ={
#                 'user': user_serializer.data,
#                 'games': games_serializer.data,
#                 'reviews': reviews_serializer.data
#             }
#             return Response(response_data, status=status.HTTP_200_OK)
#         except User.DoesNotExist:
#             return Response({'error': 'user does not exist'}, status=status.HTTP_404_NOT_FOUND)


#USER
class CreateUserAPIView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            user = serializer.save()
            return Response({'message':'user created ok', 'user_data':serializer.data}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

# ORIGINAL LOGIN VIEW
class LoginAndTokenView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)
        # print(user)
        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)

            user_id=user.id
            username = user.username
            print('username', username)

            return JsonResponse({'message': 'Login successful',
                                 'user_id': user_id,
                                 'username': username,
                                 'refresh': str(refresh),
                                 'access': str(refresh.access_token)
                                 })
        else:
            return JsonResponse({'message': 'Invalid credentials'}, status=401)


class LogoutView(APIView):
    def post(self, request):
        token = request.data.get('token')
        cache.set(token, 'logged_out', timeout=None)
        return JsonResponse({'message': 'logged out successfully'})

#GAME
class CreateGameAPIView(APIView):
    # authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
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


# CSRF EXPOSURE
def csrf_token_view(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrf_token': csrf_token})