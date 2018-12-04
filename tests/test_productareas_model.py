import unittest
from app.models import ProductArea
from app import create_app, db
from tests.TestBase import TestBase


class ProductAreaModelTestCase(TestBase):

    def test_productarea_creation(self):
        # create test clients
        productarea1 = ProductArea(product_area="Project A")
        productarea2 = ProductArea(product_area="Project B")
        productarea3 = ProductArea(product_area="Project C")

        # save client to database
        db.session.add(productarea1)
        db.session.add(productarea2)
        db.session.add(productarea3)

        db.session.commit()

        self.assertEqual(ProductArea.query.count(), 3)
