from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from .models import Post, Comment, Contact
from django.utils import timezone
from .forms import PostForm, CommentForm, ContactForm, UploadFileForm, EcotectForm
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.template import RequestContext
from django.core.mail import send_mail, BadHeaderError
from django.template import Context
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.files import File
from django.conf import settings
import re
from .ecotect import ecotect_comparison, handle_uploaded_file
import os

# Create your views here.

def post_list(request):
    all_posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    paginator = Paginator(all_posts, 5) # Show 5 posts per page
    
    page = request.GET.get('page')#The page variable is get from the url information.
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        posts = paginator.page(paginator.num_pages)

    return render(request, 'mywebsite/posts.html', {'posts': posts})



@login_required
def contact_results(request):
    results = Contact.objects.order_by('created_date')
    return render(request, 'mywebsite/contact_result.html', {'results': results})

def post_detail(request, pk): #the parameter pk is extracted from user requested url
    post = get_object_or_404(Post, pk=pk)#The pk on the right is function parameter
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.approve()
            comment.save()
            return redirect('blog.views.post_detail', pk=post.pk)
    else:
        form = CommentForm()
        return render(request, 'mywebsite/post_detail.html', {'post': post,'form': form})

@login_required
def post_new(request):
    if request.method == "POST":
        # print(request.scheme,'||', request.body, '||',request.path, '||',
        #     request.encoding, '||',request.POST,'||',request.read()
        #     ) # this line of code is used to check the reqest object this view received.
        form = PostForm(request.POST, request.FILES or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            #post.published_date = timezone.now() # adding this line of code to let you 
            #store a drafts and published it later
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'mywebsite/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES or None , instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'mywebsite/post_edit.html', {'form': form})

@login_required
def post_draft_list(request):
    posts = Post.objects.filter(published_date__isnull=True).order_by('created_date')
    return render(request, 'mywebsite/post_draft_list.html', {'posts': posts})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('blog.views.post_detail', pk=pk)

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('blog.views.post_list')

def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('blog.views.post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('blog.views.post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('blog.views.post_detail', pk=post_pk)

def projects(request):
    return render(request, 'mywebsite/projects.html', {})

def contact(request):
    if request.method == 'GET':
        form = ContactForm()
        return render(request, "mywebsite/contact.html", {'form': form})
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            contact = form.save(commit=False)
            contact.save()

            # try:# these code are to be done for automatically sending emaill when a contact is received.
            #     send_mail(subject, message, from_email, ['tj37100022@gmail.com'])
            # except BadHeaderError:
            #     return HttpResponse('Invalid header found.')
            return redirect('thanks')

        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            #post.published_date = timezone.now() # adding this line of code to let you 
            #store a drafts and published it later
            post.save()
            return redirect('post_detail', pk=post.pk)


def thanks(request):# should I just incoporate this into view.contact?
    return HttpResponse('Thank you for your message.')


def ecotect(request):
    # Handle file upload
    if request.method == 'POST':
        form = EcotectForm(request.POST, request.FILES)
        if form.is_valid():
            PATH_1 = os.path.join(os.path.dirname(__file__),'..','media','ecotect','900.txt')
            print(PATH_1)
            PATH_2 = os.path.join(os.path.dirname(__file__), '..','media','ecotect','1500.txt')
            handle_uploaded_file(request.FILES['docfile1'],PATH_1) #read uploaded file content and write it into media file.
            handle_uploaded_file(request.FILES['docfile2'],PATH_2)
            ecotect_comparison(PATH_1,PATH_2)
            return HttpResponseRedirect('../media/ecotect/result.txt')
    else:
        form = EcotectForm() # A empty, unbound form



    # Render list page with the documents and the form
    return render_to_response(
        'mywebsite/ecotect.html',
        {'form': form},
        context_instance=RequestContext(request)
    )
