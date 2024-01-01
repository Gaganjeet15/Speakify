from django.contrib import admin
from django.urls import path
from Text_to_speech.views import generate_and_play_audio  # Update the import statement
from Text_to_speech import views
from .views import extract_text
 
urlpatterns = [
    path('', views.speakify, name='speakify'),
    path('generate_audio/', views.generate_and_play_audio, name='generate_and_play_audio'),
    path('extract-text/', views.extract_text, name='extract_text'),

   

]
