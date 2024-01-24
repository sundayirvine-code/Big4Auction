from django.test import TestCase
from django.utils import timezone
from django.core.exceptions import ValidationError
from auction_app.models import Item, ItemImage, Bid, User, Category

class ItemImageModelTest(TestCase):
    def setUp(self):
        """
        Set up test data for the ItemImage model.
        """
        category = Category.objects.create(category_name='Test Category')
        user = User.objects.create(username='testuser', phone_number='1234567890')
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
        self.item_image = ItemImage.objects.create(item=item, image_url='https://example.com/image.jpg')

    def test_item_image_validation(self):
        """
        Test validation of the ItemImage model.
        """
        invalid_image = ItemImage(item=None, image_url='https://example.com/invalid.jpg')
        with self.assertRaises(ValidationError) as context:
            invalid_image.full_clean()

        # Check that the error message for the missing item is present
        self.assertIn('This field cannot be null.', context.exception.error_dict['item'][0])

    def test_item_image_relationship(self):
        """
        Test relationships with Item for the ItemImage model.
        """
        self.assertEqual(self.item_image.item.title, 'Test Item')

    def test_item_image_cascade_delete(self):
        """
        Test that deleting an item also deletes associated item images.
        """
        item_id = self.item_image.item.id
        self.item_image.item.delete()

        with self.assertRaises(ItemImage.DoesNotExist):
            ItemImage.objects.get(pk=self.item_image.pk)

    def test_item_image_lifecycle(self):
        """
        Test the lifecycle of the ItemImage model.
        """
        initial_image_url = self.item_image.image_url

        # Modify the item image URL
        self.item_image.image_url = 'https://example.com/modified.jpg'
        self.item_image.save()

        self.assertNotEqual(self.item_image.image_url, initial_image_url)

        # Delete the item image
        image_id = self.item_image.id
        self.item_image.delete()

        with self.assertRaises(ItemImage.DoesNotExist):
            ItemImage.objects.get(pk=image_id)


class BidModelTest(TestCase):
    def setUp(self):
        """
        Set up test data for the Bid model.
        """
        category = Category.objects.create(category_name='Test Category')
        user = User.objects.create(username='testuser', phone_number='1234567890')
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
        self.bid = Bid.objects.create(bidder=user, item=item, bid_amount=25.00, bid_time=timezone.now())

    def test_bid_validation(self):
        """
        Test validation of the Bid model.
        """
        invalid_bid = Bid(bidder=None, item=None, bid_amount=0, bid_time=timezone.now())
        with self.assertRaises(ValidationError) as context:
            invalid_bid.full_clean()

        # Check that the error messages for the missing bidder and item are present
        self.assertIn('This field cannot be null.', context.exception.error_dict['bidder'][0])
        self.assertIn('This field cannot be null.', context.exception.error_dict['item'][0])

    def test_bid_relationships(self):
        """
        Test relationships with User and Item for the Bid model.
        """
        self.assertEqual(self.bid.bidder.username, 'testuser')
        self.assertEqual(self.bid.item.title, 'Test Item')

    def test_bid_lifecycle(self):
        """
        Test the lifecycle of the Bid model.
        """
        initial_bid_time = self.bid.bid_time

        # Modify the bid time
        self.bid.bid_time = timezone.now() + timezone.timedelta(days=1)
        self.bid.save()

        self.assertNotEqual(self.bid.bid_time, initial_bid_time)

        # Delete the bid
        bid_id = self.bid.id
        self.bid.delete()

        with self.assertRaises(Bid.DoesNotExist):
            Bid.objects.get(pk=bid_id)
