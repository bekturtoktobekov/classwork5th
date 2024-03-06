from django.contrib import admin
from django.urls import path
from product import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/product_list/', views.product_list_view),
    path('api/v1/product_list/<int:id>/', views.product_detail_view),
]
