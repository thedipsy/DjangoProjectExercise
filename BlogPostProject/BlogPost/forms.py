from django import forms
from .models import BlogPost, BlockUser


class BlogPostForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(BlogPostForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = BlogPost
        exclude = ("author", )


class BlockUserForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(BlockUserForm, self).__init__(*args, **kwargs)
        for field in self.visible_fields():
            field.field.widget.attrs["class"] = "form-control"

    class Meta:
        model = BlockUser
        exclude = ("userThatBlocks", )