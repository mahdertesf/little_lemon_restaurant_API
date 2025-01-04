from django.urls import path
from . import views
urlpatterns = [
    path('menu-items/',views.MenuItemView.as_view(),name='menu-items'),
    path('menu-items/<int:pk>/',views.MenuItemDetailView.as_view(),name='menu-item-detail'),
    path('groups/manager/users/',views.managers,name='managers'),
    path('groups/manager/users/<int:pk>/',views.managerdetail,name='managers'),
    path('cart/menu-items/', views.cartitems, name='cart-items'),
]