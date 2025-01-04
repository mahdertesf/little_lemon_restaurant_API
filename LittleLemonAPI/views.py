from django.shortcuts import render
from .models import Category, MenuItems, Cart, Order, OrderItem
from rest_framework import generics
from .serializers import MenuItemSerializer 
from rest_framework.permissions import BasePermission


# Create your views here.

class IsManager(BasePermission):
    def has_permission(self,request,view):
        return request.user.groups.filter(name="Manager").exists()

class MenuItemView(generics.ListCreateAPIView):
    queryset=MenuItems.objects.all()
    serializer_class=MenuItemSerializer

    def get_permissions(self):
        if self.request.method=='GET':
            return []
        else:
            return [IsManager()]
    
   