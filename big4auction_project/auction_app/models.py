from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from django.core.validators import MaxValueValidator, MinValueValidator
from django.core.exceptions import ValidationError

class PaymentMethod(models.Model):
    """
    Represents a payment method available in the system.

    Attributes:
        method (CharField): Name or description of the payment method.
    """

    method = models.CharField(max_length=255)

    def __str__(self):
        return self.method
    
class Category(models.Model):
    """
    Represents a category for items.

    Attributes:
        category_name (CharField): Name of the category.
    """

    category_name = models.CharField(max_length=255)

    def __str__(self):
        return self.category_name 
    
class User(AbstractUser):
    """
    Represents a user in the system.

    Attributes:
        address (CharField, optional): Address of the user. Can be empty.
        phone_number (CharField): Phone number of the user.
        stripe_customer_id (CharField, optional): Stripe customer ID.
    """
    username = models.CharField(max_length=150, unique=True, blank=True, null=True)
    address = models.CharField(max_length=255, null=False, blank=True, default='')
    phone_number = models.CharField(max_length=255, unique=True)
    stripe_customer_id = models.CharField(max_length=255, null=True, blank=True, unique=True)

    def __str__(self):
        return '{} {}'.format(self.first_name, self.last_name)

class Item(models.Model):
    """
    Represents an item for sale in the system.

    Attributes:
        seller (ForeignKey to User): Reference to the user who is selling the item.
        title (CharField): Title of the item.
        slug (SlugField): SEO-friendly URL slug for the item.
        description (TextField): Description of the item.
        category (ForeignKey to Category): Reference to the category of the item.
        start_time (DateTimeField): Date and time when the item listing starts.
        end_time (DateTimeField): Date and time when the item listing ends.
        created (DateTimeField): Date and time when the item listing was created.
        starting_bid (DecimalField): Starting bid for the item.
        reserve_price (DecimalField): Reserve price for the item.
        current_bid (DecimalField): Current highest bid for the item.
        status (CharField): Status of the item (active, expired, sold).
    """

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('sold', 'Sold'),
    ]

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=250)
    description = models.TextField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    reserve_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_bid = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return self.title
    
    def clean(self):
        if self.reserve_price < self.starting_bid:
            raise ValidationError("Reserve price must be greater than or equal to starting bid.")
    
    def get_absolute_url(self):
        """
        Returns the canonical URL for the item.
        """
        return reverse('item_detail', kwargs={
            'year': self.created.year,
            'month': self.created.month,
            'day': self.created.day,
            'id': self.id,
            'slug': self.slug,
        })
    
    class Meta:
        constraints = [
            models.CheckConstraint(
                check=models.Q(start_time__lt=models.F('end_time')),
                name='start_time_before_end_time'
            ),
        ]

class ItemImage(models.Model):
    """
    Represents an image associated with an auction item.

    Attributes:
        item (ForeignKey to Item): Reference to the auction item.
        image_url (URLField): URL to the image of the item.
    """

    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='images')
    image_url = models.URLField()

    def __str__(self):
        return f'Image #{self.pk} for {self.item.title}'
        
class Bid(models.Model):
    """
    Represents a bid placed on an item.

    Attributes:
        bidder (ForeignKey to User): Reference to the user who placed the bid.
        item (ForeignKey to Item): Reference to the item on which the bid is placed.
        bid_amount (DecimalField): Amount of the bid.
        bid_time (DateTimeField): Date and time when the bid was placed.
    """

    bidder = models.ForeignKey('User', on_delete=models.CASCADE)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    bid_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Bid #{self.pk} on {self.item.title} by {self.bidder.username}'
    
class Transaction(models.Model):
    """
    Represents a transaction between a buyer and a seller for a specific item.

    Attributes:
        buyer (ForeignKey to User): Reference to the user who is the buyer in the transaction.
        seller (ForeignKey to User): Reference to the user who is the seller in the transaction.
        item (ForeignKey to Item): Reference to the item involved in the transaction.
        transaction_date (DateTimeField): Date and time when the transaction occurred.
        transaction_amount (DecimalField): Amount of the transaction.
        payment_method (ForeignKey to PaymentMethod): Reference to the payment method used in the transaction.
    """

    buyer = models.ForeignKey('User', related_name='buyer_transactions', on_delete=models.CASCADE)
    seller = models.ForeignKey('User', related_name='seller_transactions', on_delete=models.CASCADE)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    transaction_date = models.DateTimeField(auto_now_add=True)
    transaction_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.ForeignKey('PaymentMethod', on_delete=models.CASCADE)

    def __str__(self):
        return f'Transaction #{self.pk} - {self.buyer.username} bought {self.item.title} from {self.seller.username}'
    
class Notification(models.Model):
    """
    Represents a notification for a user.

    Attributes:
        user (ForeignKey to User): Reference to the user who receives the notification.
        message (TextField): Content of the notification message.
        timestamp (DateTimeField): Date and time when the notification was created.
        read_status (CharField): Status indicating whether the notification has been read or unread.
            Possible values are 'unread' and 'read'.
    """

    READ_STATUS_CHOICES = [
        ('unread', 'Unread'),
        ('read', 'Read'),
    ]

    user = models.ForeignKey('User', on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read_status = models.CharField(max_length=10, choices=READ_STATUS_CHOICES, default='unread')

    def __str__(self):
        return f'Notification #{self.pk} for {self.user.username}' 
    
class Feedback(models.Model):
    """
    Represents feedback provided by users.

    Attributes:
        user (ForeignKey to User): Reference to the user who provided the feedback.
        rating (IntegerField): Rating given by the user (values between 0 and 5).
        comment (TextField): Comment or additional information provided by the user.
        timestamp (DateTimeField): Date and time when the feedback was submitted.
    """

    user = models.ForeignKey('User', on_delete=models.CASCADE)
    rating = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    comment = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Feedback #{self.pk} from {self.user.username}'
    
class Report(models.Model):
    """
    Represents a report filed by a user against another user or item.

    Attributes:
        reporter (ForeignKey to User): Reference to the user who filed the report.
        reported_user (ForeignKey to User): Reference to the user who is being reported.
        item (ForeignKey to Item): Reference to the item involved in the report.
        report_description (TextField): Description of the report.
        timestamp (DateTimeField): Date and time when the report was filed.
    """

    reporter = models.ForeignKey('User', related_name='reported_by', on_delete=models.CASCADE)
    reported_user = models.ForeignKey('User', related_name='reported_user', on_delete=models.CASCADE)
    item = models.ForeignKey('Item', on_delete=models.CASCADE, null=True, blank=True)
    report_description = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Report #{self.pk} by {self.reporter.username} against {self.reported_user.username}'
    
    class Meta:
        unique_together = ['reporter', 'reported_user']