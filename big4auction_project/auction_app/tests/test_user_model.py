# myapp/tests/test_models.py
from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser
from auction_app.models import User

class UserModelTest(TestCase):
    def setUp(self):
        """
        Set up test data for the User model.
        """
        self.user = User.objects.create_user(
            username='testuser',
            address='Test Address',
            phone_number='1234567890',
            first_name='Test',
            last_name='User',
            email='testuser@example.com',
            password='securepassword',
        )

    def test_user_str(self):
        """
        Test the string representation of the User model.
        """
        self.assertEqual(str(self.user), 'testuser')

    def test_user_inheritance(self):
        """
        Test that the User model inherits from AbstractUser.
        """
        self.assertTrue(issubclass(User, AbstractUser))

    def test_user_fields(self):
        """
        Test individual fields of the User model.
        """
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.first_name, 'Test')
        self.assertEqual(self.user.last_name, 'User')
        self.assertEqual(self.user.email, 'testuser@example.com')
        self.assertEqual(self.user.address, 'Test Address')
        self.assertEqual(self.user.phone_number, '1234567890')

    def test_user_optional_address(self):
        """
        Test that the address field in User model is optional.
        """
        user_without_address = User.objects.create_user(
            username='userwithoutaddress',
            phone_number='9876543210',
            first_name='UserWithout',
            last_name='Address',
            email='userwithoutaddress@example.com',
            password='securepassword',
        )
        self.assertIsNone(user_without_address.address)

    def test_user_validation(self):
        """
        Test validation of the User model.
        """
        invalid_user = User(
            username='',  # Username is required
            address='Invalid Address',
            phone_number='9876543210',
        )
        with self.assertRaises(ValidationError) as context:
            invalid_user.full_clean()

        # Check that the error message for the blank username is present
        self.assertIn('This field cannot be blank.', context.exception.error_dict['username'][0])

    def test_user_creation_date(self):
        """
        Test that the date_joined field is automatically filled during creation.
        """
        self.assertIsNotNone(self.user.date_joined)

    def test_user_last_login(self):
        """
        Test that the last_login field has no default value.
        """
        self.assertIsNone(self.user.last_login)

    def test_user_password_hashing(self):
        """
        Test that the password is hashed during creation.
        """
        self.assertNotEqual(self.user.password, 'securepassword')
        self.assertTrue(self.user.check_password('securepassword'))
