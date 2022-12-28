from rest_framework.serializers import ModelSerializer
from .models import User, Product, Order, Category


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email']


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'category']


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'user', 'address', 'date', 'status']

    def create(self, validated_data):
        return super().create(validated_data)

    def validate(self, attrs):
        return super().validate(attrs)

    def save(self, **kwargs):
        return super().save(**kwargs)
    
    def run_validation(self, data=None):
        return super(OrderSerializer, self).run_validation(data)


class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'id']