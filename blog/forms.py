from django import forms

from .models import Post, Comment, Contact

class PostForm(forms.ModelForm):# There is model form and form form in Django.

    class Meta:
        model = Post
        fields = ('title', 'text', 'image',)

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
'''
class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50)
    file = forms.FileField()
'''
'''
class EcotectForm(forms.Form):
    ecotect_file = forms.FileField(
        label='Select a file',
        help_text='max. 1 megabytes'
    )
'''
class EcotectForm(forms.Form):
    docfile1 = forms.FileField(
        label='Choose the first ecotect result file',
        help_text='max. 1 megabytes'
    )
    docfile2 = forms.FileField(
        label='Choose the second ecotect result file',
        help_text='max. 1 megabytes'
    )