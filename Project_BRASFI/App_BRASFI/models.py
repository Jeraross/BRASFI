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

def video_upload_path(instance, filename):
    return f'videos/user_{instance.user.id}/{timezone.now().strftime("%Y%m%d%H%M%S")}_{filename}'

def thumbnail_upload_path(instance, filename):
    return f'video_thumbnails/user_{instance.user.id}/{filename}'

class Video(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    video_file = models.FileField(upload_to=video_upload_path)
    created_at = models.DateTimeField(default=timezone.now)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='videos')

    def __str__(self):
        return self.title

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'video_file': self.video_file.url if self.video_file else None,
            'created_at': self.created_at.isoformat(),
            'user': self.user.username,
        }