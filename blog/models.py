from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models

# Create your models here.



class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.TextField()
    cover_photo = models.ImageField("Image", upload_to = "images/")
    post_text = models.TextField()
    post_date = models.DateTimeField('Posted on')

    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment_text = models.TextField()
    comment_date = models.DateTimeField('Commented on')

    def __str__(self):
        return self.comment_text

class Message(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField()
    contact = models.CharField(max_length=50)
    message = models.TextField()

    def __str__(self):
        return self.name