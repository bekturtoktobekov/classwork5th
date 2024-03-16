from django.urls import path
from . import views
from product.models import Review

urlpatterns = [
    path('reviews/', views.ReviewListApiView.as_view()),
    path('reviews/<int:id>', views.RetrieveUpdateDestroyAPIView.as_view()),
    path('register/', views.RegisterApiView.as_view()),
]