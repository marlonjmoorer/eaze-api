from django.core.files.storage import default_storage
from django.db import IntegrityError
from django.db import models
from django.db import transaction
from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver

from blog.static import blogImagePath, SOCIAL_TYPES,profileImagePath,generate_username
from users.models import  User




class Tag(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, null=True, max_length=255)
    # description = models.CharField(max_length=255, null=True, default='')

    def __str__(self):
        return self.name

class Profile(models.Model):
    user = models.OneToOneField(User, related_name="profile")
    about = models.CharField(max_length=1000)
    photo = models.ImageField(storage=default_storage, null=True, upload_to=profileImagePath)
    website = models.URLField(default='', blank=True)
    joined = models.DateField(auto_now_add=True)
    handle=models.CharField(max_length=255)
    following= models.ManyToManyField("self",symmetrical=False, blank=True,related_name="followers")


class Post(models.Model):
    title = models.CharField(max_length=255)
    body = models.TextField(max_length=20000)
    posted = models.DateField(db_index=True, auto_now_add=True)
    author = models.ForeignKey(Profile,related_name="posts")
    image= models.ImageField(storage=default_storage,null=True,upload_to=blogImagePath)
    slug= models.SlugField(unique=True,null=True,max_length=255)
    draft=models.BooleanField(default=False)
    tags= models.ManyToManyField(Tag,symmetrical=False, blank=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    body= models.TextField(max_length=20000)
    profile=models.ForeignKey(Profile)
    parent= models.ForeignKey('self',null=True,blank=True)
    post=models.ForeignKey(Post,related_name='comments')
    created= models.DateField(db_index=True, auto_now_add=True)

    def __str__(self):
        return self.body

class Like(models.Model):
    profile = models.ForeignKey(Profile)
    post=models.ForeignKey(Post,related_name='likes')

    def __str__(self):
        return  "%s likes %s"%(self.user,self.post)




class SocialLink(models.Model):
    link_type=models.CharField(max_length=50)
    profile = models.ForeignKey(Profile,related_name="links")
    url=models.URLField(default='', blank=True)


@receiver(post_save, sender=User)
def create_profile(sender, instance=None, created=False, **kwargs):
    if created:
        handle= generate_username(instance.first_name,instance.last_name)
        Profile.objects.create(user=instance, handle=handle)



