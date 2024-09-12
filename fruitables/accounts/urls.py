from django.urls import path, include
from .views import custom_logout_view,EditProfileView, UserLoginView ,UserRegisterView, ProfileDetailView



urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('profile/', ProfileDetailView.as_view(), name='profile_detail'),
    path('profile/edit/', EditProfileView.as_view(), name='edit_profile'),
    path('logout/', custom_logout_view, name='logout'),
    path('', include('allauth.urls')),
    
]
