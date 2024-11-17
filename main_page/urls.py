from django.urls import path
from .views import main_page, initial_user

urlpatterns = [
    path('', main_page, name="home"),
    path('initial-user', initial_user),
]
