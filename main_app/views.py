from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.core.cache import cache
from django.middleware.csrf import get_token
from django.shortcuts import get_object_or_404

from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authentication import TokenAuthentication

from .models import Game, Review
from .serializers import UserSerializer, GroupSerializer, GameSerializer, ReviewSerializer


# just grabbing information
class UserViewSet(viewsets.ReadOnlyModelViewSet): 
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated] # if not authenticated we can't consume API
    def retrieve(self, request, *args, **kwargs): #override the built in one
        instance = self.get_object() #fetches the specific user object based on request
        user_serializer = self.get_serializer(instance)#grabs the serializer for this user
        games_serializer = GameSerializer(instance.game_set.all(), many=True)#creates a specific serializer for all games connected to this user
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

    def retrieve(self, request, *args, **kwargs): #same thing as above but just for a single game, grabs all data from that game + game specific reviews
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



class UserForReviewView(RetrieveAPIView): #used to fetch user details for a specific review, from their id. get requests only
     def get(self, request, user_id): #customize the get request
        print(f"Received user ID from URL path: {user_id}")
        user = get_object_or_404(User, pk=user_id) #django magic shortcut
        serialized_user = UserSerializer(user, context={'request': request}) #it required the context but it's magic, no obvious reason why it would need more than the id
        return Response(serialized_user.data)

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

        user = authenticate(request, username=username, password=password) #built in django method. returns a user object if successful, else returns None
    
        if user is not None:
            login(request, user) #also built in
            refresh = RefreshToken.for_user(user) #this is django-rest-framework magic

            user_id=user.id
            username = user.username

            return JsonResponse({'message': 'Login successful', #used JsonResponse because Response was not very happy with a longer message
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
        cache.set(token, 'logged_out', timeout=None) #kind of blacklisting? lives there forever now
        return JsonResponse({'message': 'logged out successfully'})

#GAME
class CreateGameAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated] #passed superuser credent
    def post(self, request):
        serializer = GameSerializer(data=request.data)
        if serializer.is_valid():
            game = serializer.save() #saves in db 
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
class CreateReviewAPIView(APIView): #ended up not using this figured out how to user the ReviewViewSet
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