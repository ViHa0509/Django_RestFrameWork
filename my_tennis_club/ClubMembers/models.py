from django.db import models
from members.models import CustomUser

# Create your models here.
class Club(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, unique=True)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    contact_email = models.EmailField(blank=True)
    contact_phone = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Add more fields as needed

    def __str__(self):
        return self.name

class ClubMember(models.Model):
    ROLE_CHOICES = (
        ('member', 'Member'),
        ('admin', 'Admin'),
    )
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    club = models.ForeignKey(Club, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    join_date = models.DateTimeField(auto_now_add=True)