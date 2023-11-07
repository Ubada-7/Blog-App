from django import forms
from .models import Comment
from django.contrib.auth.forms import UserCreationForm


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        
class CustomUserCreationForm(UserCreationForm):
    is_moderator = forms.BooleanField(required=False, initial=False)
