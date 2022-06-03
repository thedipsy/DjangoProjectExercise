from django.contrib import admin
from .models import BlogPost, CustomUser, PostComment, BlockUser
from rangefilter.filters import DateRangeFilter


# ---------------------------------------------------------

class BlogPostCommentAdmin(admin.StackedInline):
    model = PostComment
    extra = 0
    exclude = ("commentAuthor",)


# ---------------------------------------------------------

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "author",)
    list_filter = (('date_created', DateRangeFilter),)
    search_fields = ("title", "content")
    exclude = ("author",)
    inlines = [BlogPostCommentAdmin]
    readonly_fields = [
        "author",
        "title",
        "content",
        "files",
        "date_created",
        "last_updated"
    ]

    # List only content that is not blocked from the logged-in user
    def get_queryset(self, request):
        users_that_blocked_our_user = BlockUser.objects.filter(blockedUser=request.user).values_list(
            "userThatBlocks")  # get all users that blocked our user
        qs = super(BlogPostAdmin, self).get_queryset(request)  # get all posts
        qs = qs.exclude(author__in=users_that_blocked_our_user)  # exclude content that is blocked for our user
        return qs

    # If we create new Post then all fields are available
    # If we are the author of the existing post, all fields are available in order to change them
    # If we view post from another author, all fields are disabled except for the comment
    def get_readonly_fields(self, request, obj=None):
        if obj is None or (obj and request.user == obj.author):
            return []
        return self.readonly_fields

    # Save current user as author of the BlogPost if the author is not saved
    def save_model(self, request, obj, form, change):
        if getattr(obj, 'author', None) is None:
            obj.author = request.user
        super().save_model(request, obj, form, change)

    # Allow all users to view all blog-posts
    def has_view_permission(self, request, obj=None):
        return True

    # Allow all users to add a new blog-post
    def has_add_permission(self, request, obj=None):
        return True

    # Allow only author to delete the blog-post
    def has_delete_permission(self, request, obj=None):
        if (obj and request.user == obj.author) or request.user.is_superuser:
            return True
        return False

    def save_formset(self, request, form, formset, change):
        comments = formset.save(commit=False)
        for comment in comments:
            comment.commentAuthor = request.user
            comment.save()


admin.site.register(BlogPost, BlogPostAdmin)


# ---------------------------------------------------------

class BlockUserAdmin(admin.ModelAdmin):
    list_display = ("blockedUser",)
    exclude = ("userThatBlocks",)

    # List only blocks from logged-in user
    def get_queryset(self, request):
        qs = super(BlockUserAdmin, self).get_queryset(request)  # get blocks
        qs = qs.filter(userThatBlocks=request.user)  # filter blocks where our user blocked another
        return qs

    # save current user as the user that blocks
    def save_model(self, request, obj, form, change):
        if getattr(obj, 'userThatBlocks', None) is None:
            obj.userThatBlocks = request.user
        super().save_model(request, obj, form, change)

    # Allow all users to view other users
    def has_view_permission(self, request, obj=None):
        return True

    # Everyone can block a user
    def has_add_permission(self, request, obj=None):
        return True

    # Only the user that blocked another user can edit that object
    def has_change_permission(self, request, obj=None):
        if obj and request.user == obj.userThatBlocks:
            return True
        return False


admin.site.register(BlockUser, BlockUserAdmin)


# ---------------------------------------------------------

class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("name", "surname")
    readonly_fields = ("user",)

    def get_readonly_fields(self, request, obj=None):
        if obj is None or (obj and request.user.is_superuser):
            return []
        return self.readonly_fields

    def has_view_permission(self, request, obj=None):
        return True

    # Allow for users to only edit their information or admin to edit all users
    def has_change_permission(self, request, obj=None):
        if (obj and request.user == obj.user) or request.user.is_superuser:
            return True
        return False

    # Allow only admin to add Custom Users
    def has_add_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False

    # Allow only admin to delete Custom Users
    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return False


admin.site.register(CustomUser, CustomUserAdmin)
