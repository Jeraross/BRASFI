from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

# Create your models here.
class User(AbstractUser):
    TIPO_USUARIO = (
        ('mentor', 'Mentor'),
        ('aprendiz', 'Aprendiz'),
    )

    profilePic = models.ImageField(upload_to='profile_pic/', blank=True, null=True)
    userType = models.CharField(max_length=10, choices=TIPO_USUARIO, default='aprendiz')

    def __str__(self):
        return self.username

    def serialize(self):
        return {
            'id': self.id,
            "username": self.username,
            "profilePic": self.profilePic.url if self.profilePic else None,
            "userType": self.userType,
        }