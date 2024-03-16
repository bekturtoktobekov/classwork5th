from django.contrib import admin
from django.urls import path, include
from product import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/test/', views.test),
    path('api/v1/product_list/', views.product_list_view),
    path('api/v1/product_list/<int:id>/', views.product_detail_view),
    path('api/v1/login/', views.authorization),
    path('api/v1/register/', views.registration),
    path('api/v1/user/reviews/', views.user_reviews),
    path('api/v1/cbv/', include('class_based_views.urls')),
]
