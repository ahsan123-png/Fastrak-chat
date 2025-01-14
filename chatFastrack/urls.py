from django.contrib import admin
from django.urls import path,include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include("userChat.urls")),
    path('', include("fastrakGPT.urls")),
    path('', include("guestTokenSessions.urls")),
    path('', include("guestUser.urls")),
    path('', include("openaiTuning.urls")),
    path('', include("pricePlain.urls")),
]
