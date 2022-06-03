from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class CustomUser(models.Model):
    name = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="profile_images/", null=True, blank=True)
    interests = models.TextField(max_length=200, null=True, blank=True)
    skills = models.TextField(max_length=200, null=True, blank=True)
    profession = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.name + " " + self.surname


class BlockUser(models.Model):
    userThatBlocks = models.ForeignKey(User, on_delete=models.CASCADE, related_name='userThatBlocks')
    blockedUser = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blockedUser')

    def __str__(self):
        return str(self.blockedUser)


class BlogPost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    content = models.TextField()
    files = models.FileField(upload_to="post_files/", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title + " | " + str(self.author)


class PostComment(models.Model):
    blog_post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    commentAuthor = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    content = models.TextField()

    def __str__(self):
        return self.content + " | " + str(self.commentAuthor)
