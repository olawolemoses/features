import re
import unittest
from flask import url_for
from app import create_app, db
from app.models import User, Client

class ClientModuleTestCase(unittest.TestCase):
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

    def test_admin_list_clients(self):
        """
        Test that the user can list clients
        """
        # create 3  non-admin user
        client1 = Client(client_name="test_client1")
        db.session.add(client1)
        client2 =Client(client_name="test_client2")
        db.session.add(client2)
        client3 = Client(client_name="test_client3")
        db.session.add(client3)

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
        response = self.client.get(url_for('clients.index'))
        self.assertTrue(response.status_code == 200)

        #confirm the list of users in the page
        self.assertTrue(client1.client_name in response.data)
        self.assertTrue(client2.client_name in response.data)
        self.assertTrue(client3.client_name in response.data)

    def test_admin_add_client(self):
        """
        Test that the user can add client
        """
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
        response = self.client.post(url_for('clients.create'), data={
                'client_name': 'Client A',
            }, follow_redirects=True)


        self.assertTrue(re.search('Client A', response.data))

    def test_admin_edit_client(self):
        """
        Test that the user can edit a client
        """
        # register an admin account
        admin = User(username="admin", email="admin@admin.com", password="admin2016", is_admin=True)
        db.session.add(admin)

        client = Client(client_name="client A")
        db.session.add(client)

        db.session.commit()

        # login admin
        response = self.client.post(url_for('auth.login'), data={
                'email': 'admin@admin.com',
                'password': 'admin2016'
            }, follow_redirects=True)
        self.assertTrue(re.search('admin', response.data))

        # view a edit role page
        response = self.client.get(url_for('clients.edit', id=client.id))
        self.assertTrue(re.search('client A', response.data))

        # view a edit role page
        response = self.client.post(url_for('clients.edit', id=client.id),  data={
                'client_name': 'Client B'
            }, follow_redirects=True)

        self.assertTrue(re.search('Client B', response.data))

    def test_admin_delete_client(self):
        """
        Test that the user can delete a client
        """
        # register an admin account
        admin = User(username="admin", email="admin@admin.com", password="admin2016", is_admin=True)
        db.session.add(admin)

        client = Client(client_name="Client A")
        db.session.add(client)

        db.session.commit()

        # login admin
        response = self.client.post(url_for('auth.login'), data={
                'email': 'admin@admin.com',
                'password': 'admin2016'
            }, follow_redirects=True)
        self.assertTrue(re.search('admin', response.data))

        # view a edit role page
        response = self.client.post(url_for('clients.delete'),  data={
                'client_id':  client.id,
            }, follow_redirects=True)
        self.assertTrue(re.search('You have successfully deleted the Client', response.data))
