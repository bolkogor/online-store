import factory

from .models import Order, Product, Category, User


models = (Order, Product, Category, User)


class UserFactory(factory.Factory):
    class Meta:
        model = User
    first_name = 'name'
    last_name = 'last'
    factory.LazyAttribute(lambda a: f'{a.first_name}.{a.last_name}@example.com'.lower())
    phone = '3154567656'


class OrderFactory(factory.Factory):
    class Meta:
        model = Order
    user = factory.SubFactory(UserFactory)
    last_name = 'last'
    factory.LazyAttribute(lambda a: f'{a.first_name}.{a.last_name}@example.com'.lower())


class CategoryFactory(factory.Factory):
    class Meta:
        model = Category
    name = 'name'


class ProductFactory(factory.Factory):
    class Meta:
        model = Product
    name = 'name'
    price = 100
    description = 'category contains name'
    category = factory.SubFactory(CategoryFactory)
