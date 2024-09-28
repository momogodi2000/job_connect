from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone



class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('expert', 'Expert'),
        ('client', 'Client'),
    )
    
    role = models.CharField(max_length=30, choices=ROLE_CHOICES, default='client')
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    phone = models.CharField(max_length=15, default='0000000000')  # Provide a default value
    address = models.TextField(null=True, blank=True)  # Temporarily allow null


class Contact(models.Model):
    email = models.EmailField()
    description = models.TextField()
    service_rate = models.CharField(max_length=50)  # Numeric rating or choice-based field
    date = models.DateField(auto_now_add=True)  # Automatically set the date to now
    location = models.CharField(max_length=255)

    def __str__(self):
        return self.email




class Domain(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Specification(models.Model):
    name = models.CharField(max_length=255)
    domain = models.ForeignKey(Domain, related_name='specifications', on_delete=models.CASCADE)

    def __str__(self):
        return self.name




class Region(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Town(models.Model):
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region, related_name='towns', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}, {self.region.name}'

class Quarter(models.Model):
    name = models.CharField(max_length=100)
    town = models.ForeignKey(Town, related_name='quarters', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name}, {self.town.name}'

class EducationalLevel(models.Model):
    level = models.CharField(max_length=100)

    def __str__(self):
        return self.level


class Portfolio(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    address = models.TextField()
    phone = models.CharField(max_length=15)
    profile_photo = models.ImageField(upload_to='profile_photos/')
    years_of_experience = models.PositiveIntegerField()
    educational_level = models.ForeignKey(EducationalLevel, related_name='portfolios', on_delete=models.CASCADE)
    specification = models.ForeignKey(Specification, related_name='portfolios', on_delete=models.CASCADE)
    domain = models.ForeignKey(Domain, related_name='portfolios', on_delete=models.CASCADE)
    region = models.ForeignKey(Region, related_name='portfolios', on_delete=models.CASCADE)
    town = models.ForeignKey(Town, related_name='portfolios', on_delete=models.CASCADE)
    quarter = models.ForeignKey(Quarter, related_name='portfolios', on_delete=models.CASCADE)
    age = models.IntegerField(default='20')
    created_at = models.DateTimeField(default="2023-01-01 00:00:00", blank=True)  # Default to a specific date
    payment_status = models.CharField(max_length=20, default='not paid')  # New field for payment status


    def __str__(self):
        return f"{self.name}'s Portfolio"


class Receipt(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    date = models.DateTimeField(auto_now_add=True)
    reference = models.CharField(max_length=100)
    external_reference = models.CharField(max_length=100, blank=True, null=True)
    from_phone = models.CharField(max_length=20)
    description = models.TextField()
    name = models.CharField(max_length=255)
    email = models.EmailField()
    from_number = models.CharField(max_length=20, default='0')  # Updated field name


    def __str__(self):
        return f"Receipt {self.id} - {self.user.username} - {self.amount} {self.currency}"



from django.utils import timezone
from datetime import timedelta

class ForumMessage(models.Model):

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    message = models.TextField(blank=True, null=True)
    file = models.FileField(upload_to='forum_files/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.timestamp}"

    @classmethod
    def delete_old_messages(cls):
        # Delete messages older than 7 days
        expiration_date = timezone.now() - timedelta(days=7)
        cls.objects.filter(timestamp__lt=expiration_date).delete()


class Networking(models.Model):
    domain = models.ForeignKey(Domain, on_delete=models.CASCADE)
    specification = models.ForeignKey(Specification, on_delete=models.CASCADE)
    location = models.CharField(max_length=255)
    description = models.TextField()
    age = models.PositiveIntegerField()
    resume = models.FileField(upload_to='resumes/')
    social_media_gmail = models.URLField(blank=True, null=True)
    social_media_facebook = models.URLField(blank=True, null=True)
    email = models.EmailField(max_length=255, unique=True, default='default@example.com')  # Set a default email
    facebook = models.URLField(max_length=255, blank=True, default='https://facebook.com/default-profile')  # Default Facebook URL


    def __str__(self):
        return f"{self.domain} - {self.specification}"


class Communication(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    photo = models.ImageField(upload_to='communications/')
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
