from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    level = models.IntegerField(default=0)
    xp_level = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username


class UserGoal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, unique=False)
    date = models.DateField()
    description = models.CharField(max_length=128)
    completed = models.BooleanField(default=False)
    xpAmount = models.IntegerField(default=10)
