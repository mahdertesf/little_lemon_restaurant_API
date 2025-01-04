from django.shortcuts import render
from .models import Category, MenuItems, Cart, Order, OrderItem
from rest_framework import generics
from .serializers import MenuItemSerializer ,UserSerializer , CartSerializer
from rest_framework.permissions import BasePermission 
from rest_framework.response import Response
from rest_framework.decorators import api_view , permission_classes
from django.contrib.auth.models import User, Group
from rest_framework import status


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
    
class MenuItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset=MenuItems.objects.all()
    serializer_class=MenuItemSerializer
    
    def get_permissions(self):
        if self.request.method=='GET':
            return []
        else:
            return [IsManager()]

@api_view(['GET','POST',]) 
@permission_classes([IsManager])  
def managers(request):
    if request.method=='POST':
        username=request.data['username']
        if username:
            user=User.objects.get(username=username)
            managers=Group.objects.get(name="Manager")
            managers.user_set.add(user)
            return Response({'message':'Manager added'})
        else:
            return Response({'message':'put username correctly'}, status.HTTP_400_BAD_REQUEST)
            
    if request.method=='GET':
        managers=User.objects.filter(groups__name="Manager")
        serialized_users=UserSerializer(managers,many=True)
        return Response(serialized_users.data, status.HTTP_200_OK)

@api_view(['GET','DELETE']) 
@permission_classes([IsManager])
def managerdetail(request,pk):   
    if request.method=='GET':
        user=User.objects.get(pk=pk)
        serialized_user=UserSerializer(user)
        return Response(serialized_user.data, status.HTTP_200_OK)
    if request.method=='DELETE':
        user=User.objects.get(pk=pk)
        managers=Group.objects.get(name="Manager")
        managers.user_set.remove(user)
        return Response({"message":f'Manager {user.username} removed'}, status.HTTP_200_OK)
    
    
@api_view(['GET','POST','DELETE'])
def cartitems(request):
    if request.method=='GET':
        cartitems=Cart.objects.filter(user=request.user)
        serialized_cartitems=CartSerializer(cartitems, many=True)
        return Response(serialized_cartitems.data, status.HTTP_200_OK)
    if request.method=='POST':
        deserialized_data=CartSerializer(data=request.data, context={'request':request})
        deserialized_data.is_valid(raise_exception=True)
        deserialized_data.save()
        return Response(deserialized_data.data, status.HTTP_201_CREATED)
        
        
        