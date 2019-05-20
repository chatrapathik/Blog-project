from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Blog(models.Model):
    blog_id = models.CharField(max_length=255)
    title = models.TextField(default="")
    content = models.TextField(default="")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    likes = models.IntegerField(default=0)
    un_likes = models.IntegerField(default=0)
    comments = models.IntegerField(default=0)
    views = models.IntegerField(default=0)
    dt_uploaded = models.DateTimeField(auto_now=True)

    class meta:
        unique_together = (("blog_id", "title"),)

    def __str__(self):
        return "{}- {}".format(self.blog_id, self.title)

    def as_dict(obj):
        d = dict()
        d["blog_id"] = obj.blog_id
        d["title"] = obj.title
        d["content"] = obj.content
        d["owner"] = obj.user.username
        d["likes"] = obj.likes
        d["un_likes"] = obj.un_likes
        d["comments"] = obj.comments
        d["views"] = obj.views
        d["dt_created"] = obj.dt_uploaded.strftime("%d %b %Y %H:%M:%S")

        return d

class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(default="")
    dt_commented = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}- {}".format(self.blog, self.comment)

    def as_dict(obj):
        d = dict()
        d["blog_title"] = obj.blog.title
        d["username"] = obj.user.username
        d["comment"] = obj.comment
        d["dt_commented"] = obj.dt_commented.strftime("%d %b %Y %H:%M:%S")

        return d

class Like(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    like = models.IntegerField(default=0)
    dt_like = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}- {}".format(self.blog, self.user)

    def as_dict(obj):
        d = dict()
        d["username"] = obj.user.username
        d["blog_title"] = obj.blog.title
        d["dt_liked"] = obj.dt_like.strftime("%d %b %Y %H:%M:%S")

        return d

class UnLike(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    unlike = models.IntegerField(default=0)
    dt_unlike = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}- {}".format(self.blog, self.user)

    def as_dict(obj):
        d = dict()
        d["username"] = obj.user.username
        d["blog_title"] = obj.blog.title
        d["dt_unliked"] = obj.dt_unlike.strftime("%d %b %Y %H:%M:%S")

        return d

class View(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dt_view = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "{}- {}".format(self.blog, self.user)

    def as_dict(obj):
        d = dict()
        d["username"] = obj.user.username
        d["blog_title"] = obj.blog.title
        d["dt_viewed"] = obj.dt_view.strftime("%d %b %Y %H:%M:%S")

        return d
