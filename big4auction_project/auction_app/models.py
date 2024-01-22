from django.db import models

class User(models.Model):
    """
    Represents a user in the system.

    Attributes:
        user_id (AutoField): Primary key auto-incremented identifier for the user.
        username (CharField): Unique username for the user.
        email (EmailField): Unique email address for the user.
        password_hash (CharField): Hashed password for the user.
        full_name (CharField): Full name of the user.
        address (CharField, optional): Address of the user. Can be empty.
        phone_number (CharField): Phone number of the user.
        registration_date (DateTimeField): Date and time of user registration.
    """

    username = models.CharField(max_length=255, unique=True)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=255)
    full_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=255)
    registration_date = models.DateTimeField()

    def __str__(self):
        return self.username

class Item(models.Model):
    """
    Represents an item for sale in the system.

    Attributes:
        seller (ForeignKey to User): Reference to the user who is selling the item.
        title (CharField): Title of the item.
        description (TextField): Description of the item.
        category (ForeignKey to Category): Reference to the category of the item.
        start_time (DateTimeField): Date and time when the item listing starts.
        end_time (DateTimeField): Date and time when the item listing ends.
        starting_bid (DecimalField): Starting bid for the item.
        reserve_price (DecimalField): Reserve price for the item.
        current_bid (DecimalField): Current highest bid for the item.
        image_url (URLField): URL to the image of the item.
        status (CharField): Status of the item (active, expired, sold).

    Note:
        The `status` field is represented using a CharField with choices to emulate an enum-like behavior.
    """

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('sold', 'Sold'),
    ]

    seller = models.ForeignKey('User', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=250)
    description = models.TextField()
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    reserve_price = models.DecimalField(max_digits=10, decimal_places=2)
    current_bid = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    def __str__(self):
        return self.title
    
class Bid(models.Model):
    """
    Represents a bid placed on an item.

    Attributes:
        bid_id (AutoField, Primary Key): Unique identifier for the bid.
        bidder (ForeignKey to User): Reference to the user who placed the bid.
        item (ForeignKey to Item): Reference to the item on which the bid is placed.
        bid_amount (DecimalField): Amount of the bid.
        bid_time (DateTimeField): Date and time when the bid was placed.
    """

    bid_id = models.AutoField(primary_key=True)
    bidder = models.ForeignKey('User', on_delete=models.CASCADE)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    bid_time = models.DateTimeField()

    def __str__(self):
        return f'Bid #{self.bid_id} on {self.item.title} by {self.bidder.username}'
    
class Transaction(models.Model):
    """
    Represents a transaction between a buyer and a seller for a specific item.

    Attributes:
        transaction_id (AutoField, Primary Key): Unique identifier for the transaction.
        buyer (ForeignKey to User): Reference to the user who is the buyer in the transaction.
        seller (ForeignKey to User): Reference to the user who is the seller in the transaction.
        item (ForeignKey to Item): Reference to the item involved in the transaction.
        transaction_date (DateTimeField): Date and time when the transaction occurred.
        transaction_amount (DecimalField): Amount of the transaction.
        payment_method (ForeignKey to PaymentMethod): Reference to the payment method used in the transaction.
    """

    transaction_id = models.AutoField(primary_key=True)
    buyer = models.ForeignKey('User', related_name='buyer_transactions', on_delete=models.CASCADE)
    seller = models.ForeignKey('User', related_name='seller_transactions', on_delete=models.CASCADE)
    item = models.ForeignKey('Item', on_delete=models.CASCADE)
    transaction_date = models.DateTimeField()
    transaction_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.ForeignKey('PaymentMethod', on_delete=models.CASCADE)

    def __str__(self):
        return f'Transaction #{self.transaction_id} - {self.buyer.username} bought {self.item.title} from {self.seller.username}'
    
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
        return f'Notification #{self.notification_id} for {self.user.username}' 

class Category(models.Model):
    """
    Represents a category for items.

    Attributes:
        category_name (CharField): Name of the category.
    """

    category_name = models.CharField(max_length=255)

    def __str__(self):
        return self.category_name 