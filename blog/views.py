from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from .models import Post, Category, Tag, Comment
from .forms import PostForm, CommentForm


# BLOG LIST + SEARCH + FILTER
def blog_list(request):
    q = request.GET.get("q", "")
    category_slug = request.GET.get("category")
    tag_slug = request.GET.get("tag")

    posts = Post.objects.all()

    if q:
        posts = posts.filter(
            Q(title__icontains=q) |
            Q(content__icontains=q)
        )

    if category_slug:
        posts = posts.filter(categories__slug=category_slug)

    if tag_slug:
        posts = posts.filter(tags__slug=tag_slug)

    categories = Category.objects.all()
    tags = Tag.objects.all()

    return render(request, "blog/blog_list.html", {
        "posts": posts,
        "categories": categories,
        "tags": tags,
        "q": q,
    })


# BLOG DETAIL + COMMENTS
def blog_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.order_by("-created_at")

    if request.method == "POST":
        if request.user.is_authenticated:
            form = CommentForm(request.POST)
            if form.is_valid():
                c = form.save(commit=False)
                c.post = post
                c.author = request.user
                c.save()
                return redirect("blog_detail", slug=slug)
        else:
            return redirect("login")

    form = CommentForm()

    return render(request, "blog/blog_detail.html", {
        "post": post,
        "comments": comments,
        "form": form
    })


# CREATE POST
def blog_create(request):
    if not request.user.is_authenticated:
        return redirect("login")

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            p = form.save(commit=False)
            p.author = request.user
            p.save()
            form.save_m2m()
            return redirect("blog_detail", slug=p.slug)
    else:
        form = PostForm()

    return render(request, "blog/blog_create.html", {"form": form})


# EDIT POST
def blog_edit(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.user != post.author:
        return redirect("blog_detail", slug=slug)

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect("blog_detail", slug=post.slug)
    else:
        form = PostForm(instance=post)

    return render(request, "blog/blog_edit.html", {"form": form})


# DELETE POST
def blog_delete(request, slug):
    post = get_object_or_404(Post, slug=slug)

    if request.user == post.author:
        post.delete()

    return redirect("blog_list")


# DASHBOARD (Author Posts)
def blog_dashboard(request):
    if not request.user.is_authenticated:
        return redirect("login")

    posts = Post.objects.filter(author=request.user)

    return render(request, "blog/blog_dashboard.html", {"posts": posts})
