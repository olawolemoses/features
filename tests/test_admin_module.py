import re
import unittest
from flask import url_for
from app import create_app, db
from app.models import User, Role

class AdminModuleTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()
        self.client = self.app.test_client(use_cookies=True)

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register_and_login(self):
        # register a new account
        response = self.client.post(url_for('auth.register'), data={
            'email': 'john@example.com',
            'username': 'john',
            'password': 'cat',
            'password2': 'cat'

        })
        self.assertTrue(response.status_code == 302)

        # login with the new account
        response = self.client.post(url_for('auth.login'), data={
                'email': 'john@example.com',
                'password': 'cat'
            }, follow_redirects=True)
        self.assertTrue(re.search('john', response.data))

        # # # send a confirmation token
        # user = User.query.filter_by(email='john@example.com').first()
        # token = user.generate_confirmation_token()
        # response = self.client.get(url_for('auth.confirm', token=token),
        #                            follow_redirects=True)
        # self.assertTrue(b'Login' in response.data)

        # log out
        response = self.client.get(url_for('auth.logout'), follow_redirects=True)
        self.assertTrue(b'Login' in response.data)

    def test_admin_list_users(self):
        # register an admin account
        admin = User(username="admin", email="admin@admin.com", password="admin2016", is_admin=True)
        db.session.add(admin)

        # create 3  non-admin user
        user1 = User(username="test_user1", password="test2016", email='test1@test.com')
        db.session.add(user1)
        user2 = User(username="test_user2", password="test2016", email='test2@test.com')
        db.session.add(user2)
        user3 = User(username="test_user3", password="test2016", email='test3@test.com')
        db.session.add(user3)

        db.session.commit()

        # login admin
        # login with the new account
        response = self.client.post(url_for('auth.login'), data={
                'email': 'admin@admin.com',
                'password': 'admin2016'
            }, follow_redirects=True)
        self.assertTrue(re.search('admin', response.data))

        # check users list
        response = self.client.get(url_for('admin.users_index'))
        self.assertTrue(response.status_code == 200)

        #confirm the list of users in the page
        self.assertTrue(user1.username in response.data)
        self.assertTrue(user2.username in response.data)
        self.assertTrue(user3.username in response.data)

    def test_admin_users_assign(self):
        # register an admin account
        admin = User(username="admin", email="admin@admin.com", password="admin2016", is_admin=True)
        db.session.add(admin)

        #create role
        role = Role(name="CEO", description="Run the whole company")

        # save role to database
        db.session.add(role)

        # create non-admin user
        user = User(username="test_user1", password="test2016", email='test1@test.com')
        db.session.add(user)
        db.session.commit()

        # login admin
        # login with the new account
        response = self.client.post(url_for('auth.login'), data={
                'role': 'admin@admin.com',
                'user_id': 'admin2016'
            }, follow_redirects=True)
        self.assertTrue(re.search('admin', response.data))

        # check users list
        response = self.client.post(url_for('admin.users_assign'), data={
                    'role':role.id,
                    'user_id':user.id
                })
        self.assertTrue(response.status_code == 302)

    def test_admin_list_roles(self):
        # register an admin account
        admin = User(username="admin", email="admin@admin.com", password="admin2016", is_admin=True)
        db.session.add(admin)

        # create 3  non-admin user
        role1 = Role(name="CEO1", description="Run the whole company")
        db.session.add(role1)
        role2 = Role(name="CEO2", description="Run the whole company")
        db.session.add(role2)
        role3 = Role(name="CEO3", description="Run the whole company")
        db.session.add(role3)

        db.session.commit()

        # login admin
        response = self.client.post(url_for('auth.login'), data={
                'email': 'admin@admin.com',
                'password': 'admin2016'
            }, follow_redirects=True)
        self.assertTrue(re.search('admin', response.data))

        # check users list
        response = self.client.get(url_for('admin.users_index'))
        self.assertTrue(response.status_code == 200)

        #confirm the list of users in the page
        self.assertTrue(role1.name in response.data)
        self.assertTrue(role2.name in response.data)
        self.assertTrue(role3.name in response.data)

    def test_admin_add_role(self):
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
        response = self.client.post(url_for('admin.add_role'), data={
                'name': 'CEO',
                'description': 'Chief Executive Operator'
            }, follow_redirects=True)


        self.assertTrue(re.search('CEO', response.data))

    def test_admin_edit_role(self):
        # register an admin account
        admin = User(username="admin", email="admin@admin.com", password="admin2016", is_admin=True)
        db.session.add(admin)

        role = Role(name="CEO3", description="Run the whole company")
        db.session.add(role)

        db.session.commit()

        # login admin
        response = self.client.post(url_for('auth.login'), data={
                'email': 'admin@admin.com',
                'password': 'admin2016'
            }, follow_redirects=True)
        self.assertTrue(re.search('admin', response.data))

        # view a edit role page
        response = self.client.get(url_for('admin.edit_role', id=role.id))
        self.assertTrue(re.search('CEO3', response.data))

        # view a edit role page
        response = self.client.post(url_for('admin.edit_role', id=role.id),  data={
                'name': 'CEO',
                'description': 'Chief Executive Operator'
            }, follow_redirects=True)

        self.assertTrue(re.search('CEO', response.data))

    def test_admin_delete_role(self):
        # register an admin account
        admin = User(username="admin", email="admin@admin.com", password="admin2016", is_admin=True)
        db.session.add(admin)

        role = Role(name="CEO3", description="Run the whole company")
        db.session.add(role)

        db.session.commit()

        # login admin
        response = self.client.post(url_for('auth.login'), data={
                'email': 'admin@admin.com',
                'password': 'admin2016'
            }, follow_redirects=True)
        self.assertTrue(re.search('admin', response.data))

        # view a edit role page
        response = self.client.post(url_for('admin.delete_role'),  data={
                'role_id':  role.id,
            }, follow_redirects=True)
        self.assertTrue(re.search('You have successfully deleted the Role', response.data))
