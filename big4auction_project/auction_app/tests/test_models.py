from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from auction_app.models import Item, ItemImage, Bid, Transaction, Notification, Feedback, Report, PaymentMethod, Category, User

class ItemModelTest(TestCase):
    def setUp(self):
        # Create test data for the Item model
        category = Category.objects.create(category_name='Test Category')
        user = User.objects.create(username='testuser', phone_number='1234567890')
        self.item = Item.objects.create(
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
        self.item.save()

    def test_item_str(self):
        self.assertEqual(str(self.item), 'Test Item')

    def test_item_status_choices(self):
        # Ensure that status choices are valid
        for status, _ in Item.STATUS_CHOICES:
            self.assertIn(status, ['active', 'expired', 'sold'])

    '''def test_item_absolute_url(self):
        expected_url = reverse('item_detail', kwargs={
            'year': self.item.created.year,
            'month': self.item.created.month,
            'day': self.item.created.day,
            'id': self.item.id,
            'slug': self.item.slug,
        })
        self.assertEqual(self.item.get_absolute_url(), expected_url)'''