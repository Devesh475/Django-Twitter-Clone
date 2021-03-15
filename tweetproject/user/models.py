from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class userform(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    followers = models.ManyToManyField(User, related_name="follower", blank=True)
    following = models.ManyToManyField(User, related_name="hasfollowed", blank=True)
    bio = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return str(self.user)

    def follower_list(self):
        f = self.followers
        return f