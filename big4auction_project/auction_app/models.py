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
