from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.db import models
from commerce import settings


class User(AbstractUser):
    pass

class Listing(models.Model):

    """ Listing class for creating listing model """

    createdby = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    image = models.ImageField(null=True, blank=True, upload_to="images/")
    description = models.CharField(max_length=255,default="description")
    price = models.CharField(max_length=100)
    link = models.CharField(max_length=100,blank=True)
    category = models.CharField(max_length=50,default="Home")
    date = models.DateTimeField(auto_now_add=True)
    isopen = models.BooleanField(default=True)
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("index")
    


class Bid(models.Model):
    user = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    price = models.CharField(max_length=100)

    def __str__(self):
        return self.price

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("index")

class Comment(models.Model):
    title =models.ForeignKey(Listing,on_delete=models.CASCADE,related_name="comments")
    comment = models.CharField(max_length=200)
    author = models.ForeignKey(get_user_model(),on_delete=models.CASCADE)

    def __str__(self):
        return self.comment
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("index")

class WatchLists(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    items = models.ManyToManyField(Listing)
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("watchlist")
