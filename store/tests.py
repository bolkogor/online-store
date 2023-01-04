import random

from django.test import TestCase, Client
from . import models
from . import factories


class ApiTestCase(TestCase):
    def setUp(self):
        models.Category.objects.create(name='Everything')
        models.Product.objects.create(name='Prod1', category_id=1, price=10)
        models.User.objects.create_superuser(username='admin', password='admin')
        self.client = Client()
        self.list_paths = ('/categories/', '/products/', '/orders/', '/users/')

    def test_get_requests(self):
        self.client = Client()
        response = self.client.get('/')
        self.client.login(username='admin', password='admin')
        self.assertEqual(response.status_code, 200)
        for path in (*self.list_paths, '/users/1/', '/products/1/'):
            resp = self.client.get(path)
            self.assertEqual(resp.status_code, 200)
        self.client.logout()
        for path in ('/categories/', '/products/', '/products/1/'):
            resp = self.client.get(path)
            self.assertEqual(resp.status_code, 200)
        for path in ('/orders/', '/users/'):
            resp = self.client.get(path)
            self.assertEqual(resp.status_code, 403)

    def test_CRUD(self):
        mods = (models.Order, models.Product, models.Category, models.User)
        self.client.login(username='admin', password='admin')
        product_data = vars(factories.ProductFactory.stub())
        product_data['category'] = models.Category.objects.first().id
        order_data = vars(factories.OrderFactory.stub())
        order_data['user'] = models.User.objects.first().id
        data_list = [
            vars(factories.CategoryFactory.stub()),
            product_data,
            order_data,
            vars(factories.UserFactory.stub())
        ]
        # create
        for path, data in zip(self.list_paths, data_list):
            resp = self.client.post(path, data=data, content_type='application/json')
            self.assertEqual(resp.status_code, 201)
            # created
            resp = self.client.get(f"{path}{resp.data['id']}/")
            self.assertEqual(resp.status_code, 200)
        # Order items have been created
        self.assertEqual(models.Item.objects.count(), len(order_data['items']))
        # delete
        ids = [cls.objects.first().id for cls in mods]
        paths = ('/orders/', '/products/', '/categories/', '/users/')
        for path, identifier in zip(paths, ids):
            resp = self.client.delete(f'{path}{identifier}/')
            self.assertEqual(resp.status_code, 204)

    def test_order_with_items(self):
        for i in range(3):
            cat = models.Category.objects.create(**vars(factories.CategoryFactory.stub()))
            product = models.Product.objects.create(**vars(factories.ProductFactory.stub(category=cat)))
            order_data = [
                {
                'item': models.Product.objects.first().id,
                'quantity': random.Random().randint(1, 10),
                }
                for i in range(3)
        ]
        pass

    def tearDown(self):
        super().tearDown()
        models.Category.objects.all().delete()
        models.User.objects.all().delete()
        models.Product.objects.all().delete()
        models.Order.objects.all().delete()





