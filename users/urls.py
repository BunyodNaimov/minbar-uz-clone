from django.urls import path

from users.views import UserRegisterView, UserLoginView, UserProfileAPIView

app_name = 'users'

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='user-register'),
    path('login/', UserLoginView.as_view(), name='user-login'),
    path('profile/', UserProfileAPIView.as_view(), name='user-profile'),
]
