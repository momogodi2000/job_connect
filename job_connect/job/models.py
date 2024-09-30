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
    location = models.CharField(max_length=255, blank=True)  # New location field



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


class Review(models.Model):
    expert = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='expert_reviews', limit_choices_to={'role': 'expert'})
    client_name = models.CharField(max_length=255)
    client_email = models.EmailField()
    comment = models.TextField()
    rating = models.PositiveSmallIntegerField(choices=[(i, i) for i in range(1, 6)])  # Rating from 1 to 5
    created_at = models.DateTimeField(default=timezone.now)
    
    def __str__(self):
        return f"Review by {self.client_name} for {self.expert.username}"



class Booking(models.Model):
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='client_bookings')
    expert = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='expert_bookings', limit_choices_to={'role': 'expert'})
    date = models.DateTimeField()
    service_description = models.TextField()
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('confirmed', 'Confirmed'), ('completed', 'Completed')], default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Booking by {self.client.username} with {self.expert.username}"

        

from django.conf import settings  # Import settings to reference AUTH_USER_MODEL

class JobPost(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    requirements = models.TextField()
    qualifications = models.TextField()
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # Use AUTH_USER_MODEL
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class JobApplication(models.Model):
    job_post = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='applications')
    candidate_name = models.CharField(max_length=255)
    candidate_email = models.EmailField()
    resume = models.FileField(upload_to='resumes/')
    cover_letter = models.TextField()
    applied_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.candidate_name} applied for {self.job_post.title}"


class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    subject = models.CharField(max_length=255, null=True, blank=True)
    body = models.TextField()
    file = models.FileField(upload_to='message_files/', null=True, blank=True)  # Allow file sharing
    created_at = models.DateTimeField(auto_now_add=True)
    
    # To auto-delete records older than 1 month
    def is_old(self):
        return self.created_at <= timezone.now() - timedelta(days=30)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.sender} to {self.recipient}"

# You can schedule automatic deletion of old messages using a periodic task (e.g., cron or Django Celery)
