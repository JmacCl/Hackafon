from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    picture = models.ImageField(upload_to='profile_images', blank=True)
    xpLevel = models.IntegerField(default=1)

    def save(self, *args, **kwargs):
        split_file_name = self.picture.name.split('.')
        new_name = self.user.username
        if len(split_file_name) > 0:
            new_name += '.' + split_file_name[1]
        self.picture.name = new_name
        super(UserProfile, self).save(*args, **kwargs)

    def __str__(self):
        return self.user.username


class Goal(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    date = models.DateField()
    description = models.CharField(max_length=128)
