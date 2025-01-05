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
            pass
        elif request.user.groups.filter(name='Delivery Crew').exists():
            pass
        else:
            if request.method=='POST':
                carts=Cart.objects.filter(user=request.user)
                if not carts:
                    return Response({'message':'Cart is empty'}, status.HTTP_400_BAD_REQUEST)
                for item in carts:
                    deserialized_item=OrderItemSerializer(data={
                        'menuitem': item.menuitem.id, 
                        'quantity': item.quantity,
                        'unit_price': item.unit_price, 
                        'price': item.price},
                        context={'request': request})
                    
                    deserialized_item.is_valid(raise_exception=True)    
                  
                    deserialized_item.save()
    
                Cart.objects.filter(user_id=request.user.id).delete()
                return Response({'message':'All Order placed'}, status.HTTP_201_CREATED)
              
                        
                return Response({'message':'Order placed'}, status.HTTP_201_CREATED)
            if request.method=='GET':
                items=OrderItem.objects.filter(order__id=request.user.id)
                serialized_orders=OrderItemSerializer(items,many=True)
                return Response(serialized_orders.data, status.HTTP_200_OK)
            
@api_view(['GET', 'DELETE', 'PUT', 'PATCH'])
def orderdetail(request, pk):
    try:
        orderitem= OrderItem.objects.get(order=request.user, pk=pk)
    except OrderItem.DoesNotExist:
        return Response({'error': 'Order not found'}, status=status.HTTP_404_NOT_FOUND)


    if request.user.groups.filter(name='Manager').exists():
        # Add logic for Manager
        pass
    elif request.user.groups.filter(name='Delivery Crew').exists():
        # Add logic for Delivery Crew
        pass
    else:
        if request.method == 'GET':
            serialized_order = OrderItemSerializer(orderitem,context={'request': request})
            return Response(serialized_order.data, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            order.delete()
            return Response({'message': 'Order deleted'}, status=status.HTTP_200_OK)
        elif request.method in ['PUT', 'PATCH']:
            deserialized_order = OrderSerializer(request.data)
            deserialized_order.is_valid(raise_exception=True)
            deserialized_order.save()
            return Response(deserialized_order.data, status=status.HTTP_200_OK)
    
    return Response({'error': 'Unauthorized access'}, status=status.HTTP_403_FORBIDDEN)