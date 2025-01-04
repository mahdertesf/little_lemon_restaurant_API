from rest_framework import serializers
from .models import Category, MenuItems, Cart, Order, OrderItem 
from django.contrib.auth.models import User, Group

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields='__all__'
        
        
class MenuItemSerializer(serializers.ModelSerializer):
    category=CategorySerializer(read_only=True) 
    category_id=serializers.IntegerField(write_only=True)
    class Meta:
        model=MenuItems
        fields=['id','title','price','featured','category','category_id']
        


class CartSerializer(serializers.ModelSerializer):
    menuitem=MenuItemSerializer(read_only=True)
    menuitem_id=serializers.IntegerField(write_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'user', 'menuitem', 'quantity', 'unit_price', 'price', 'menuitem_id']
        read_only_fields = ['price', 'user', 'unit_price']
    

    
    def create(self, validated_data):
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['user'] = request.user
        menuitem_id= validated_data.pop('menuitem_id')
        menuitem=MenuItems.objects.get(id=menuitem_id)
        validated_data['menuitem']=menuitem        
        validated_data['unit_price'] = menuitem.price
        validated_data['price']=menuitem.price*validated_data['quantity']
        return super().create(validated_data)
    
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields='__all__'
    
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=OrderItem
        fields='__all__'
    
class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model=Group
        fields=['name']
        
        
class UserSerializer(serializers.ModelSerializer):
    groups=GroupSerializer(many=True, read_only=True)
    class Meta:
        model=User
        fields=['id','username','email','groups']
        