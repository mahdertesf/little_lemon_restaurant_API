from rest_framework import serializers
from .models import Category, MenuItems, Cart, Order, OrderItem

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields='__all__'
        
        
class MenuItemSerializer(serializers.ModelSerializer):
    category=CategorySerializer()
    class Meta:
        model=MenuItems
        fields=['id','title','price','featured','category']
        

class CartSerializer(serializers.ModelSerializer):
    price=serializers.SerializerMethodField(method_name='price')
    class Meta:
        model=Cart
        fields=['id','user','menuitem','quantity','unit_price','price']
    def price(self,product):
        return product.unit_price*product.quantity
    
    
class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model=Order
        fields='__all__'
    
class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model=OrderItem
        fields='__all__'
    
