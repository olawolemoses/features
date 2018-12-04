import unittest
from app.models import User, Client
from app import create_app, db
from tests.TestBase import TestBase

class ClientModelTestCase(TestBase):


    def test_client_creation(self):
        # create test clients
        clientA = Client(client_name="Client A")
        clientB = Client(client_name="Client B")
        clientC = Client(client_name="Client C")

        # save client to database
        db.session.add(clientA)
        db.session.add(clientB)
        db.session.add(clientC)
        db.session.commit()

        self.assertEqual(Client.query.count(), 3)
