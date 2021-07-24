from django.db import models

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=300)

class Image(models.Model):
    image = models.ImageField(upload_to='picshared', blank=True)
    tags = models.ManyToManyField(Tag, related_name='image_tags', blank=True)

class Post(models.Model):
    image = models.ManyToManyField(Image, related_name='post_image', blank=True)
    tags = models.ManyToManyField(Tag, related_name='post_tags', blank=True)
    

