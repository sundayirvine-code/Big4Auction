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