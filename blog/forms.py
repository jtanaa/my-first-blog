from django import forms

from .models import Post, Comment, Contact

class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ('title', 'text',)

class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('author', 'text',)

class ContactForm(forms.ModelForm):
    # from_email = forms.EmailField(required=True)
    # subject = forms.CharField(required=True)
    # message = forms.CharField(widget=forms.Textarea)
    class Meta:
    	model = Contact
    	fields = ('from_email', 'subject', 'message')