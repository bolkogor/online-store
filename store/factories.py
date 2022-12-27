import factory

from .models import Order, Product, Category, User


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
