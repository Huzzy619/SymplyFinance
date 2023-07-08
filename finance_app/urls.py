from django.urls import path
from . import views



urlpatterns = [
    path("", views.AIView.as_view(), name="AI")
    
]
