from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('speakify/', include('Text_to_speech.urls')),
]
