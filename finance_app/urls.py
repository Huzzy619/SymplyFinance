from django.urls import path
from . import views



urlpatterns = [
    path("search/", views.AIView.as_view(), name="AI")
    
]
