from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=500)
    starting_bid = models.IntegerField()
    image_url = models.URLField(max_length=500, blank = True)
    category = models.CharField(max_length=50, blank = True)
    listing_user = models.ForeignKey('User', on_delete=models.CASCADE, related_name = "listings")
    is_active = models.BooleanField()
    comment = models.ForeignKey('Comment', on_delete=models.CASCADE, blank = True, null = True, related_name = "listings")

    def __str__(self):
        return f"Item: {self.title}, Category: {self.category} Starting bid: {self.starting_bid}"



class Comment(models.Model):
    text = models.CharField(max_length = 500)
    user = models.ForeignKey(User, on_delete = models.CASCADE, related_name = "comments")
    listing = models.ForeignKey('Listing', on_delete = models.CASCADE, related_name = "comments")

    def __str__(self):
        return f"User: {self.user}, Listing: {self.listing}, Comment: {self.comment}"
    


class Bid(models.Model):
    listing = models.ForeignKey('Listing', on_delete = models.CASCADE, related_name = "bids")
    bid = models.IntegerField()
    
    def __str__(self):
        return f"Listing: {self.listing}, Bid: {self.bid}"