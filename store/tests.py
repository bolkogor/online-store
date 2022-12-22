from django.test import TestCase, Client
from . import models


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

    def tearDown(self):
        pass


