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
from rest_framework.exceptions import ValidationError
from decimal import Decimal
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
                orders=OrderItem.objects.all()
                serialized_orders=OrderItemSerilizer(orders,many=True)
                return Response(serialized_orders.data, status.HTTP_200_OK)
        elif request.user.groups.filter(name='Delivery Crew').exists():
            pass
        else:
            if request.method=='POST':
                carts=Cart.objects.filter(user=request.user)
                
                if not carts:
                    return Response({'message':'Cart is empty'}, status.HTTP_400_BAD_REQUEST)
                serialized_order=OrderSerializer(data={'user':request.user.id}, context={'request':request})
                serialized_order.is_valid(raise_exception=True)
                
                try:
                    order=serialized_order.save()
                    order_id=order.id
                except IntegrityError:
                    return Response({'message':'Order already exists'}, status.HTTP_400_BAD_REQUEST)
                for item in carts:
                    deserialized_item=OrderItemSerializer(data={
                        'order':order_id,                     
                        'menuitem_id': item.menuitem_id,
                        'menuitem': item.menuitem, 
                        'quantity': item.quantity,
                        'unit_price': item.unit_price, 
                        'price': item.price,},
                        context={'request': request})
                    
                    deserialized_item.is_valid(raise_exception=True)    
                  
                    try:
                        deserialized_item.save()
                    except IntegrityError as e:
                        return Response({'message':str(e)}, status.HTTP_400_BAD_REQUEST)
                        
                
                
                Cart.objects.filter(user_id=request.user.id).delete()
                
                        
                return Response({'message':'Order placed'}, status.HTTP_201_CREATED)
            if request.method=='GET':
                items=OrderItem.objects.filter(order__user=request.user)
                serialized_orders=OrderItemSerializer(items,many=True)
                return Response(serialized_orders.data, status.HTTP_200_OK)
            
@api_view(['GET', 'DELETE', 'PUT', 'PATCH'])
def orderdetail(request, pk):
    try:
        orderitem = OrderItem.objects.get(order=request.user, pk=pk)
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
            serialized_order = OrderItemSerializer(orderitem, context={'request': request})
            return Response(serialized_order.data, status=status.HTTP_200_OK)
        elif request.method == 'DELETE':
            orderitem.delete()
           
            return Response({'message': 'Order deleted'}, status=status.HTTP_200_OK)
        elif request.method in ['PUT', 'PATCH']:
            deserialized_order = OrderItemSerializer(
                orderitem,
                data=request.data,
                partial=(request.method == 'PATCH'),
                context={'request': request}
            )
            try:
                deserialized_order.is_valid(raise_exception=True)
                
                
                deserialized_order.save()
                update_orderitem_price(orderitem)
               
                
                
                return Response(deserialized_order.data, status=status.HTTP_200_OK)
            except ValidationError as e:
                return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    return Response({'error': 'Unauthorized access'}, status=status.HTTP_403_FORBIDDEN)



        
def update_orderitem_price(order_item):
    order_item.price = order_item.menuitem.price * order_item.quantity
    order_item.unit_price = order_item.menuitem.price
    order_item.save()
    
        
   
    
    
