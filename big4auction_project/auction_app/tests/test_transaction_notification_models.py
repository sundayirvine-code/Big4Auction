from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from auction_app.models import Transaction, Notification, PaymentMethod, User, Item, Category

class TransactionModelTest(TestCase):
    def setUp(self):
        """
        Set up test data for the Transaction model.
        """
        buyer = User.objects.create(username='buyer', phone_number='1234567890')
        seller = User.objects.create(username='seller', phone_number='9876543210')
        category = Category.objects.create(category_name='Test Category')
        item = Item.objects.create(
            title='Test Item',
            slug='test-item',
            description='This is a test item.',
            category=category,
            start_time=timezone.now(),
            end_time=timezone.now() + timezone.timedelta(days=7),
            created=timezone.now(),
            starting_bid=10.00,
            reserve_price=20.00,
            current_bid=15.00,
            status='active',
        )
        payment_method = PaymentMethod.objects.create(method='Test Payment Method')

        self.transaction = Transaction.objects.create(
            buyer=buyer,
            seller=seller,
            item=item,
            transaction_date=timezone.now(),
            transaction_amount=25.00,
            payment_method=payment_method,
        )

    def test_transaction_str(self):
        """
        Test the string representation of the Transaction model.
        """
        expected_str = f'Transaction #{self.transaction.pk} - buyer bought Test Item from seller'
        self.assertEqual(str(self.transaction), expected_str)

    def test_transaction_validation(self):
        """
        Test validation of the Transaction model.
        """
        invalid_transaction = Transaction(
            buyer=None,  # Buyer is required
            seller=None,  # Seller is required
            item=None,  # Item is required
            transaction_amount=0,  # Amount should be greater than 0
            payment_method=None,  # Payment method is required
        )
        with self.assertRaises(ValidationError) as context:
            invalid_transaction.full_clean()

        # Check exact error messages
        self.assertIn('This field cannot be null.', context.exception.error_dict['buyer'][0])
        self.assertIn('This field cannot be null.', context.exception.error_dict['seller'][0])
        self.assertIn('This field cannot be null.', context.exception.error_dict['item'][0])
        self.assertIn('This field cannot be null.', context.exception.error_dict['payment_method'][0])


    def test_transaction_relationships(self):
        """
        Test relationships with User, Item, and PaymentMethod for the Transaction model.
        """
        self.assertEqual(self.transaction.buyer.username, 'buyer')
        self.assertEqual(self.transaction.seller.username, 'seller')
        self.assertEqual(self.transaction.item.title, 'Test Item')
        self.assertEqual(self.transaction.payment_method.method, 'Test Payment Method')

    def test_transaction_cascade_delete(self):
        """
        Test that deleting an item also deletes associated transactions.
        """
        item_id = self.transaction.item.id
        self.transaction.item.delete()

        with self.assertRaises(Transaction.DoesNotExist):
            Transaction.objects.get(pk=self.transaction.pk)

    def test_transaction_lifecycle(self):
        """
        Test the lifecycle of the Transaction model.
        """
        initial_transaction_amount = self.transaction.transaction_amount

        # Modify the transaction amount
        self.transaction.transaction_amount = 30.00
        self.transaction.save()

        self.assertNotEqual(self.transaction.transaction_amount, initial_transaction_amount)

        # Delete the transaction
        transaction_id = self.transaction.id
        self.transaction.delete()

        with self.assertRaises(Transaction.DoesNotExist):
            Transaction.objects.get(pk=transaction_id)


class NotificationModelTest(TestCase):
    def setUp(self):
        """
        Set up test data for the Notification model.
        """
        user = User.objects.create(username='testuser', phone_number='1234567890')
        self.notification = Notification.objects.create(
            user=user,
            message='Test Notification',
            timestamp=timezone.now(),
            read_status='unread',
        )

    def test_notification_str(self):
        """
        Test the string representation of the Notification model.
        """
        expected_str = f'Notification #{self.notification.pk} for testuser'
        self.assertEqual(str(self.notification), expected_str)

    def test_notification_validation(self):
        """
        Test validation of the Notification model.
        """
        invalid_notification = Notification(
            user=None,  # User is required
            message='',  # Message should not be empty
            timestamp=None,  # Timestamp is required
            read_status='',  # Read status should be one of the choices
        )
        with self.assertRaises(ValidationError) as context:
            invalid_notification.full_clean()

        # Check exact error messages
        self.assertIn('This field cannot be null.', context.exception.error_dict['user'][0])
        self.assertIn('This field cannot be blank.', context.exception.error_dict['message'][0])
        self.assertIn('This field cannot be blank.', context.exception.error_dict['read_status'][0])
        # Check for the absence of timestamp field in the error_dict
        self.assertNotIn('timestamp', context.exception.error_dict)

    def test_notification_relationships(self):
        """
        Test relationships with User for the Notification model.
        """
        self.assertEqual(self.notification.user.username, 'testuser')

    def test_notification_lifecycle(self):
        """
        Test the lifecycle of the Notification model.
        """
        initial_message = self.notification.message

        # Modify the notification message
        self.notification.message = 'Modified Message'
        self.notification.save()

        self.assertNotEqual(self.notification.message, initial_message)

        # Delete the notification
        notification_id = self.notification.id
        self.notification.delete()

        with self.assertRaises(Notification.DoesNotExist):
            Notification.objects.get(pk=notification_id)
