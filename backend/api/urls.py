from django.urls import path
from .views import SignupView, GetTokenView, ProfileView

app_name = 'api'

urlpatterns = [
    path('auth/signup/', SignupView.as_view(), name='signup'),
    path('auth/token/', GetTokenView.as_view(), name='get_token'),
    path('profile/', ProfileView.as_view(), name='get_profile'),
]