from django.shortcuts import render, redirect
from .models import BlockUser, BlogPost, CustomUser
from .forms import BlogPostForm, BlockUserForm


def get_all_posts(request):
    logged_in_user = request.user #get logged in user
    blocked_users = BlockUser.objects.all() #get all blocked users

    users_i_have_blocked = blocked_users\
        .filter(userThatBlocks=logged_in_user)\
        .values_list("blockedUser") #get users that I have blocked

    user_that_blocked_me = blocked_users\
        .filter(blockedUser=logged_in_user)\
        .values_list("userThatBlocks") #get users that have bloked me, this is not in the requiremtns of the lab exercise but i decided to add it because it makes sense

    # exclude posts from users I have blocked, then exclude posts from users that have blocked me, then exclude my posts
    posts_list = BlogPost.objects\
        .exclude(author__in=users_i_have_blocked)\
        .exclude(author__in=user_that_blocked_me)\
        .exclude(author=logged_in_user)

    context = {"posts": posts_list, }
    return render(request, "posts.html", context=context)


def add_post(request):
    if request.method == "POST":
        form_data = BlogPostForm(data=request.POST, files=request.FILES)
        if form_data.is_valid():
            post = form_data.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("posts")

    context = {"form": BlogPostForm}
    return render(request, "add-post.html", context=context)


def get_profile(request):
    logged_in_user = request.user

    posts_list = BlogPost.objects.filter(author=logged_in_user).all()
    profile = CustomUser.objects.filter(user=logged_in_user).all()

    context = {"profile": profile[0], "posts": posts_list, }
    return render(request, "profile.html", context=context)


def get_blocked_users(request):
    if request.method == "POST":
        form_data = BlockUserForm(data=request.POST, files=request.FILES)
        if form_data.is_valid():
            block_user = form_data.save(commit=False)
            block_user.userThatBlocks = request.user
            block_user.save()
            return redirect("blocked-users")

    logged_in_user = request.user

    blocked_users = BlockUser.objects.all()
    users_i_have_blocked = blocked_users.filter(userThatBlocks=logged_in_user).all()
    context = {"blockedUsers": users_i_have_blocked, "form": BlockUserForm}
    return render(request, "blocked-users.html", context=context)
