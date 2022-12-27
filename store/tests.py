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
        for path, data in zip(self.list_paths, data_list):
            resp = self.client.post(path, data=data)
            self.assertEqual(resp.status_code, 201)

    def tearDown(self):
        super().tearDown()
        models.Category.objects.delete()
        models.User.objects.delete()
        models.Product.objects.delete()
        models.Order.objects.delete()





