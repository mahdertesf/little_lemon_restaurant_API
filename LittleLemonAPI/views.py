from django.shortcuts import render
from .models import Category, MenuItems, Cart, Order, OrderItem
from rest_framework import generics
from .serializers import MenuItemSerializer ,UserSerializer , CartSerializer , OrderSerializer, OrderItemSerializer
from rest_framework.permissions import BasePermission 
from rest_framework.response import Response
from rest_framework.decorators import api_view , permission_classes
from django.contrib.auth.models import User, Group
from rest_framework import status
from django.db import IntegrityError

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
        try:
            deserialized_data=CartSerializer(data=request.data, context={'request':request})
            deserialized_data.is_valid(raise_exception=True)
            deserialized_data.save()
        except IntegrityError:
            return Response({'message':'Item already exists in cart'}, status.HTTP_400_BAD_REQUEST)
        return Response(deserialized_data.data, status.HTTP_201_CREATED)
    if request.method=='DELETE':
        cartitem=Cart.objects.filter(user=request.user)
        cartitem.delete()
        return Response({'message':'Cart items deleted'}, status.HTTP_200_OK)
        
#Order Management endpoints
@api_view(['GET','POST'])
def orders(request):
        if request.user.groups.filter(name='Manager').exists():
            if request.method=='GET':
                orderitems=Order.objects.all()
                serialized_orders=OrderSerializer(orderitems, many=True)
                return Response(serialized_orders.data, status.HTTP_200_OK)
            if request.method=='POST':
                deserialized_orders=OrderSerializer(data=request.data)
                deserialized_orders.is_valid(rasie_exception=True)
                deserialized_orders.save()
                return Response(deserialized_orders.data, status.HTTP_201_CREATED)
        elif request.user.groups.filter(name='Delivery Crew').exists():
            pass
        else:
            if request.method=='POST':
                deserialized_orders=OrderSerializer(data=request.data)
                deserialized_orders.is_valid(raise_exception=True)
                deserialized_orders.save()
                Cart.objects.filter(user=request.user).delete()
                return Response(deserialized_orders.data, status.HTTP_201_CREATED)
            if request.method=='GET':
                items=Order.Objects.filter(user=request.user)
                serialized_orders=OrderSerializer(items,many=True)
                return Response(serialized_orders.data, status.HTTP_200_OK)