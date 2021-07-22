from django.db import models
from django.contrib.auth.models import User


# Create your models here.
choices = (
    ('Male','Male'), 
    ('Female','Female'), 
    ('Other','Prefer not to disclose')
)

class userform(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
    profileImage = models.ImageField(upload_to='profiles/' ,null=True,blank=True)
    firstName = models.CharField(max_length=200, null=True)
    lastName = models.CharField(max_length=200, null=True)
    gender = models.CharField(max_length=200, choices=choices, null=True)
    contactNumber = models.CharField(max_length=10, null=True)
    address = models.CharField(max_length=200, null=True)
    followers = models.ManyToManyField(User, related_name="follower", blank=True)
    following = models.ManyToManyField(User, related_name="hasfollowed", blank=True)
    bio = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):          
        return str(self.user)

    def follower_list(self):
        f = self.followers
        return f
    
    @property
    def img_url(self):
        return self.profileImage.url
        