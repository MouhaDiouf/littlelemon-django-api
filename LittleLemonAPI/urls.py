from django.urls import path

from . import views

urlpatterns = [
    path('menu-items/', views.menu_items),
    path('menu/', views.menu),
    path('menu-items/<int:pk>', views.single_item),
    path('category/<int:pk>',views.category_detail, name='category-detail'),
]