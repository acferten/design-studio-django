from django.urls import path
from . import views


urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('home/', views.index, name='index'),
    path('profile/', views.profile, name='profile'),
]
