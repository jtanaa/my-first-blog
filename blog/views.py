from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment, Contact
from django.utils import timezone
from .forms import PostForm, CommentForm, ContactForm, UploadFileForm
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.core.mail import send_mail, BadHeaderError
from django.template import Context
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

# Create your views here.

def post_list(request):
    all_posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
    paginator = Paginator(all_posts, 5) # Show 5 posts per page
    
    page = request.GET.get('page')
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

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
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
    return render(request, 'blog/post_draft_list.html', {'posts': posts})

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
