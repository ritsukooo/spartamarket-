from django.urls import path
from . import views

app_name = "products"

urlpatterns = [
    path("", views.products, name="products"),
    path("create/", views.create, name="create"),
    path("<int:pk>/", views.products_detail, name="products_detail"),
    
    
    path("<int:pk>/delete/", views.delete, name="delete"),
    path("<int:pk>/update/", views.update, name="update"),
    
    path('<int:pk>/like/', views.like, name='like'),
    
]
