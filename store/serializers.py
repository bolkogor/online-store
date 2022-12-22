from rest_framework.serializers import ModelSerializer
from .models import User, Product, Order, Category


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email']


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'category']


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user_id', 'address', 'date', 'status']


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['name']