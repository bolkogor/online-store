import random

import factory

from .models import Order, Product, Category, User, Item


models = (Order, Product, Category, User)


class DictStubMixin:
    @classmethod
    def stub_as_dict(cls):
        stub = cls.stub()
        res = {}
        for attr, value in stub:
            res[attr] = value
        return res


class UserFactory(factory.Factory, DictStubMixin):
    class Meta:
        model = User
    first_name = factory.Faker('first_name')
    last_name = 'last'
    email = factory.LazyAttribute(lambda a: f'{a.first_name}.{a.last_name}@example.com'.lower())
    phone = '3154567656'


class OrderFactory(factory.Factory):
    class Meta:
        model = Order
    user = factory.SubFactory(UserFactory)
    items = [
        {'item': i, 'quantity': i, 'price': i*10}
        for i in range(1, 3)
    ]


class CategoryFactory(factory.Factory):
    class Meta:
        model = Category
    name = 'name'


class ProductFactory(factory.Factory, DictStubMixin):
    class Meta:
        model = Product
    name = 'product'
    price = 100
    description = 'category contains name'
    category = factory.SubFactory(CategoryFactory)


class ItemFactory(factory.Factory):
    class Meta:
        model = Item

    item = factory.SubFactory(ProductFactory)
    quantity = random.Random(x=1).randint(1, 10)
    price = random.Random(x=1).randint(1, 100)
    order = factory.SubFactory(OrderFactory)
