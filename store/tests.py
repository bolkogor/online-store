
from django.test import TestCase, Client
from . import models
from . import factories


class ApiTestCase(TestCase):
    def setUp(self):
        models.Category.objects.create(name='Everything')
        models.Product.objects.create(name='Prod1', category_id=1, price=10)
        models.User.objects.create_superuser(username='admin', password='admin')
        models.User.objects.create_user(username='user', password='user')
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
        # orders not accessible for anonymous users
        resp = self.client.get('/orders/')
        self.assertEqual(resp.status_code, 403)
        # no access
        resp = self.client.get('/users/')
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
        user_client = Client()
        user_client.login(username='user', password='user')
        # user gets filtered queryset / not available
        resp = user_client.get('/orders/1/')
        self.assertEqual(resp.status_code, 404)
        # create new order by that user
        resp = user_client.post('/orders/', data=order_data, content_type='application/json')
        self.assertEqual(resp.status_code, 201)
        # has access to their order
        resp = user_client.get(f'/orders/{resp.data["id"]}/')
        self.assertEqual(resp.status_code, 200)
        # filter products for categories
        resp = self.client.get('/products/?category=2')
        self.assertEqual(len(resp.data), 0)
        resp = self.client.get('/products/?category=1')
        self.assertEqual(len(resp.data), 2)
        # search product by name
        resp = self.client.get('/products/?search=prod1')
        self.assertEqual(len(resp.data), 1)
        resp = self.client.get('/products/?search=prod')
        self.assertEqual(len(resp.data), 2)
        resp = self.client.get('/products/?search=non_existing')
        self.assertEqual(len(resp.data), 0)

        # delete
        ids = [cls.objects.first().id for cls in mods]
        paths = ('/orders/', '/products/', '/categories/', '/users/')
        for path, identifier in zip(paths, ids):
            resp = self.client.delete(f'{path}{identifier}/')
            self.assertEqual(resp.status_code, 204)
        # Items deleted with order
        self.assertEqual(models.Item.objects.count(), 0)



    def tearDown(self):
        super().tearDown()
        models.Category.objects.all().delete()
        models.User.objects.all().delete()
        models.Product.objects.all().delete()
        models.Order.objects.all().delete()





