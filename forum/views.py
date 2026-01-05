from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.text import slugify
from django.urls import reverse
from .models import Category, Thread, Post, Reply, Vote, Profile
from .forms import CreateThreadForm, PostForm, ReplyForm
from django.http import JsonResponse, HttpResponseForbidden
from django.db import models

def forum_home(request):
    categories = Category.objects.prefetch_related("threads").all()
    return render(request, "forum/forum_home.html", {"categories": categories})

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    threads = category.threads.select_related("creator").all()
    return render(request, "forum/category_detail.html", {"category": category, "threads": threads})

@login_required
def create_thread(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    if request.method == "POST":
        thread_form = CreateThreadForm(request.POST)
        post_form = PostForm(request.POST)
        if thread_form.is_valid() and post_form.is_valid():
            title = thread_form.cleaned_data["title"]
            slug = slugify(title)[:240]
            # ensure unique slug
            base_slug = slug
            n = 1
            while Thread.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{n}"
                n += 1

            thread = Thread.objects.create(
                category=category,
                title=title,
                slug=slug,
                creator=request.user
            )
            Post.objects.create(thread=thread, author=request.user, content=post_form.cleaned_data["content"])
            return redirect("forum:thread_detail", category_slug=category.slug, thread_slug=thread.slug)
    else:
        thread_form = CreateThreadForm()
        post_form = PostForm()
    return render(request, "forum/create_thread.html", {"category": category, "thread_form": thread_form, "post_form": post_form})

def thread_detail(request, category_slug, thread_slug):
    thread = get_object_or_404(Thread, slug=thread_slug, category__slug=category_slug)
    posts = thread.posts.select_related("author").prefetch_related("votes", "replies").all()
    reply_form = ReplyForm()
    post_form = PostForm()
    return render(request, "forum/thread_detail.html", {"thread": thread, "posts": posts, "reply_form": reply_form, "post_form": post_form})

@login_required
def create_post(request, category_slug, thread_slug):
    thread = get_object_or_404(Thread, slug=thread_slug, category__slug=category_slug)
    if thread.locked:
        return HttpResponseForbidden("Thread is locked.")
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            Post.objects.create(thread=thread, author=request.user, content=form.cleaned_data["content"])
    return redirect("forum:thread_detail", category_slug=category_slug, thread_slug=thread_slug)

@login_required
def create_reply(request, post_id, category_slug, thread_slug):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        form = ReplyForm(request.POST)
        if form.is_valid():
            Reply.objects.create(post=post, author=request.user, content=form.cleaned_data["content"])
    return redirect("forum:thread_detail", category_slug=category_slug, thread_slug=thread_slug + "#post-" + str(post.id))

@login_required
def vote_post(request):
    # expects POST with post_id and value (1 or -1)
    if request.method != "POST":
        return JsonResponse({"error": "POST only"}, status=405)
    post_id = request.POST.get("post_id")
    value = int(request.POST.get("value", 1))
    post = get_object_or_404(Post, id=post_id)
    vote, created = Vote.objects.get_or_create(user=request.user, post=post, defaults={"value": value})
    if not created:
        if vote.value == value:
            # cancel vote
            vote.delete()
            action = "removed"
        else:
            vote.value = value
            vote.save()
            action = "updated"
    else:
        action = "created"
    total = post.votes.aggregate(total=models.Sum("value"))["total"] or 0
    return JsonResponse({"action": action, "total": total})
