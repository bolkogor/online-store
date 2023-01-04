from rest_framework import serializers
from .models import User, Product, Order, Category, Item


def get_total(price, quantity):
    return price*quantity


class RelatedFieldRerp(serializers.RelatedField):
    def to_internal_value(self, data):
        return data.id

    def to_representation(self, value):
        return value.id


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'category', 'price']


class OrderItemSerializer(serializers.Serializer):
    order = RelatedFieldRerp(read_only=True)
    item = RelatedFieldRerp(read_only=False, queryset=Product.objects.all())
    quantity = serializers.IntegerField(default=1)
    price = serializers.DecimalField(max_digits=8, decimal_places=2)
    total = serializers.SerializerMethodField()

    def get_total(self, obj):
        return obj.quantity * obj.price

    def to_internal_value(self, data):
        data['item'] = Product.objects.get(pk=data['item'])
        return super(OrderItemSerializer, self).to_internal_value(data)

    def to_representation(self, instance):
        data = super(OrderItemSerializer, self).to_representation(instance)
        return data


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)
    total = serializers.SerializerMethodField()
    user = RelatedFieldRerp(read_only=True)


    class Meta:
        model = Order
        fields = ['id', 'user', 'address', 'date', 'status', 'items', 'total']

    def get_total(self, obj):
        total = 0
        for item in obj.items.all():
            total += item.price * item.quantity
        return total

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(**validated_data)
        for item_data in items_data:
            prod = Product.objects.get(id=item_data['item'])
            item_data['item'] = prod
            item_data['price'] = prod.price
            Item.objects.create(order=order, **item_data)
        return order

    def validate(self, attrs):
        return super().validate(attrs)

    def save(self, **kwargs):
        return super().save(**kwargs)

    def run_validation(self, data=None):
        return super(OrderSerializer, self).run_validation(data)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['name', 'id']