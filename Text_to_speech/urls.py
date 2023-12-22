from django.contrib import admin
from django.urls import path
from Text_to_speech.views import generate_and_play_audio  # Update the import statement
from Text_to_speech import views
urlpatterns = [
    path('', views.todolist, name='todolist'),
    path('generate_audio/', generate_and_play_audio, name='generate_and_play_audio'),

]
