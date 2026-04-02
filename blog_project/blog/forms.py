from django import forms

from .models import Comment, Post, Tag


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["name", "email", "body"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "input", "placeholder": "Your name"}),
            "email": forms.EmailInput(attrs={"class": "input", "placeholder": "you@example.com"}),
            "body": forms.Textarea(
                attrs={"class": "textarea", "rows": 4, "placeholder": "Share your thoughts"}
            ),
        }


class PostForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Post
        fields = ["title", "body", "status", "cover_image", "tags"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "input", "placeholder": "Post title"}),
            "body": forms.Textarea(attrs={"class": "textarea", "rows": 8}),
            "status": forms.Select(attrs={"class": "input"}),
        }
