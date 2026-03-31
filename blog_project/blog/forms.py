from django import forms

from .models import Comment


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
