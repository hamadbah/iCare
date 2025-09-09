from django.db import models
from django.contrib.auth.models import User

# Create your models here.
user_role = [
    ('clerk', 'Clerk'),
    ('doctor', 'Doctor'),
    ('nurse', 'Nurse')
]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    role = models.CharField(max_length=15, choices=user_role, blank=True, null=True)
    fullname = models.CharField(max_length=75, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.user.username