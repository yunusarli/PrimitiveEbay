from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):

    """ Listing class for creating listing model """

    createdby = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    price = models.PositiveIntegerField()
    link = models.CharField(max_length=100,blank=True)
    category = models.CharField(max_length=50,default="Home")
    date = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("index")
    


class Bids(models.Model):
    title = models.ForeignKey(Listing,on_delete=models.CASCADE)
    price = models.PositiveIntegerField()

    def __str__(self):
        return str(self.price)

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("index")
    