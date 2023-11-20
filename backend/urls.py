from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from main_app import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'games', views.GameViewSet)
router.register(r'reviews', views.ReviewViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('new-user/', views.CreateUserAPIView.as_view()),
    path('new-game/', views.CreateGameAPIView.as_view()),
    path('games/<int:game_id>/new-review', views.CreateReviewAPIView.as_view()),
    path('games/<int:game_id>/reviews/<int:review_id>', views.ReviewAPIView.as_view()),
    path('games/<int:game_id>/edit', views.EditGameAPIView.as_view()),
    path('api/login', views.LoginAndTokenView.as_view()),
    path('api/logout', views.LogoutView.as_view()),
    path('get-csrf-token/', views.csrf_token_view)
]
