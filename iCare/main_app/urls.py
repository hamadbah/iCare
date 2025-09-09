from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name = 'home'),
    path('about/', views.about, name = 'about'),
    path('accounts/signup/', views.signup, name='signup'),
    
    path('profile/', views.profile_view, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
]