from django.db import models
from django.conf import settings
from ckeditor.fields import RichTextField

User = settings.AUTH_USER_MODEL



class Blog(models.Model):
    parent = models.ForeignKey("self", null=True, on_delete=models.SET_NULL, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    image = models.ImageField(upload_to='image/',blank=True, null=True)
    captions = RichTextField(blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='blogpost', blank=True)
    dateTime = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return self.captions or "Retweeted"
    
    def post_url(self):
        return "detail/"+str(self.id)

    def total_likes(self):
        return self.likes.count()
    
    def total_comments(self):
        return str(BlogComment.objects.filter(post=self.id).count())
    
class BlogComment(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    post = models.ForeignKey(Blog, on_delete=models.CASCADE)
    text = models.CharField(max_length=200)
    timestamp = models.TimeField(auto_now=True)

    def __str__(self):
        return self.text