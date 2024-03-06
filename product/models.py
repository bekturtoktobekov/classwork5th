from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    price = models.FloatField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title

    @property
    def count_reviews(self):
        return self.reviews.all().count()

    @property
    def all_reviews(self):
        reviews = Review.objects.filter(product=self)
        return [{'id' : i.id, 'text': i.text} for i in reviews]

    @property
    def rating(self):
        return Review.objects.filter(product=self).aggregate(Avg('stars'))
        # sum_ = 0
        # for i in reviews:
        #     sum_ += i.stars
        # try:
        #     return sum_ / reviews.count()
        # except:
        #     return 0

class Review(models.Model):
    text = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, related_name='reviews')
    stars = models.IntegerField(default=5, null=True)

    def __str__(self):
        return self.text