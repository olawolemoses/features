import re
import unittest
from flask import url_for
from app import create_app, db
from app.models import User, ProductArea

class ProductAreaModuleTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_admin_list_product_areas(self):

        # create 3  non-admin user
        product_area1 = ProductArea(product_area="ProductArea A")
        db.session.add(product_area1)
        product_area2 =ProductArea(product_area="ProductArea B")
        db.session.add(product_area2)
        product_area3 = ProductArea(product_area="ProductArea C")
        db.session.add(product_area3)

        # register an admin account
        admin = User(username="admin", email="admin@admin.com", password="admin2016", is_admin=True)
        db.session.add(admin)

        db.session.commit()

        # login admin
        # login with the new account
        response = self.client.post(url_for('auth.login'), data={
                'email': 'admin@admin.com',
                'password': 'admin2016'
            }, follow_redirects=True)
        self.assertTrue(re.search('admin', response.data))

        # check users list
        response = self.client.get(url_for('productareas.index'))
        self.assertTrue(response.status_code == 200)

        #confirm the list of users in the page
        self.assertTrue(product_area1.product_area in response.data)
        self.assertTrue(product_area2.product_area in response.data)
        self.assertTrue(product_area3.product_area in response.data)

    def test_admin_add_product_area(self):
        # register an admin account
        admin = User(username="admin", email="admin@admin.com", password="admin2016", is_admin=True)
        db.session.add(admin)
        db.session.commit()

        # login admin
        response = self.client.post(url_for('auth.login'), data={
                'email': 'admin@admin.com',
                'password': 'admin2016'
            }, follow_redirects=True)
        self.assertTrue(re.search('admin', response.data))

        # post a new role
        response = self.client.post(url_for('productareas.create'), data={
                'product_area': 'product_area A',
            }, follow_redirects=True)


        self.assertTrue(re.search('product_area A', response.data))

    def test_admin_edit_product_area(self):
        # register an admin account
        admin = User(username="admin", email="admin@admin.com", password="admin2016", is_admin=True)
        db.session.add(admin)

        product_area = ProductArea(product_area="product_area A")
        db.session.add(product_area)

        db.session.commit()

        # login admin
        response = self.client.post(url_for('auth.login'), data={
                'email': 'admin@admin.com',
                'password': 'admin2016'
            }, follow_redirects=True)
        self.assertTrue(re.search('admin', response.data))

        # view a edit role page
        response = self.client.get(url_for('productareas.edit', id=product_area.id))
        self.assertTrue(re.search('product_area A', response.data))

        # view a edit role page
        response = self.client.post(url_for('productareas.edit', id=product_area.id),  data={
                'product_area': 'product_area B'
            }, follow_redirects=True)


        self.assertTrue(re.search('product_area B', response.data))

    def test_admin_delete_product_area(self):
        # register an admin account
        admin = User(username="admin", email="admin@admin.com", password="admin2016", is_admin=True)
        db.session.add(admin)

        product_area = ProductArea(product_area="ProductArea A")
        db.session.add(product_area)

        db.session.commit()

        # login admin
        response = self.client.post(url_for('auth.login'), data={
                'email': 'admin@admin.com',
                'password': 'admin2016'
            }, follow_redirects=True)
        self.assertTrue(re.search('admin', response.data))

        # view a edit role page
        response = self.client.post(url_for('productareas.delete'),  data={
                'product_area_id':  product_area.id,
            }, follow_redirects=True)
        self.assertTrue(re.search('You have successfully deleted the Product Area.', response.data))
