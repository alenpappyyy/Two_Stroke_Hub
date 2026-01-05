from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.conf import settings

User = get_user_model()

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='forum_profile')   
    signature = models.TextField(blank=True)

    bio = models.TextField(blank=True)
    is_moderator = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to="avatars/", blank=True, null=True)

    def __str__(self):
        return f"Profile: {self.user}"

class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

class Thread(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="threads")
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="threads")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    pinned = models.BooleanField(default=False)
    locked = models.BooleanField(default=False)

    class Meta:
        ordering = ["-pinned", "-updated_at"]

    def __str__(self):
        return self.title

class Post(models.Model):
    thread = models.ForeignKey(Thread, on_delete=models.CASCADE, related_name="posts")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="posts")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Post #{self.id} on {self.thread}"

class Reply(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="replies")
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name="replies")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"Reply #{self.id} to Post #{self.post.id}"

class Vote(models.Model):
    VOTE_CHOICES = ((1, "Upvote"), (-1, "Downvote"))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="forum_votes")
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="votes")
    value = models.SmallIntegerField(choices=VOTE_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "post")
