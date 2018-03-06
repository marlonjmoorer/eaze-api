from django.core.files.storage import default_storage
from django.db import models
from users.models import  User


def createPath(instance, filename):
    return "media/{authorId}/{id}/{file}".format(id=instance.id, authorId=instance.author.id, file=filename)


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
    image= models.ImageField(storage=default_storage,null=True,upload_to=createPath)
    slug= models.SlugField(unique=True,null=True,max_length=255)
    draft=models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Comment(models.Model):
    body= models.TextField(max_length=20000)
    user=models.ForeignKey(User)
    post=models.ForeignKey(Post,related_name='comments')
    created= models.DateField(db_index=True, auto_now_add=True)

    def __str__(self):
        return self.body

class Like(models.Model):

    user=models.ForeignKey(User)
    post=models.ForeignKey(Post,related_name='likes')

    def __str__(self):
        return  "%s likes %s"%(self.user,self.post)