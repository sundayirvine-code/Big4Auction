from django.test import TestCase
from auction_app.models import PaymentMethod, Category

class PaymentMethodModelTest(TestCase):
    def setUp(self):
        """
        Set up test data for the PaymentMethod model.
        """
        self.payment_method = PaymentMethod.objects.create(method='Test Payment Method')

    def test_payment_method_str(self):
        """
        Test the string representation of the PaymentMethod model.
        """
        self.assertEqual(str(self.payment_method), 'Test Payment Method')

    def test_payment_method_fields(self):
        """
        Test individual fields of the PaymentMethod model.
        """
        self.assertEqual(self.payment_method.method, 'Test Payment Method')

class CategoryModelTest(TestCase):
    def setUp(self):
        """
        Set up test data for the Category model.
        """
        self.category = Category.objects.create(category_name='Test Category')

    def test_category_str(self):
        """
        Test the string representation of the Category model.
        """
        self.assertEqual(str(self.category), 'Test Category')

    def test_category_fields(self):
        """
        Test individual fields of the Category model.
        """
        self.assertEqual(self.category.category_name, 'Test Category')
