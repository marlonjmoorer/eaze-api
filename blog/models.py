
from django.db import models
from users.models import  User
class Tag(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255, null=True, default='')

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField(max_length=20000)
    tags = models.ManyToManyField(Tag)
    posted = models.DateField(db_index=True, auto_now_add=True)
    author = models.ForeignKey(User)
    imageUrl=models.CharField(max_length=500,null=True)

    def __str__(self):
        return self.title