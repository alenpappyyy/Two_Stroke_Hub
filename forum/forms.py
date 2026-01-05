from django import forms
from .models import Thread, Post, Reply

class CreateThreadForm(forms.ModelForm):
    class Meta:
        model = Thread
        fields = ["title"]

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={"rows":4, "placeholder":"Write your post..."}),
        }

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={"rows":3, "placeholder":"Write a reply..."}),
        }
