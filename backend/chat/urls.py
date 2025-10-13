from django.urls import path
from . import views


urlpatterns = [
    path("chat", views.ChatAPI.as_view(), name="chat"),
]