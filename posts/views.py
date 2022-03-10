from pyexpat import model
from webbrowser import get
from django.shortcuts import render, redirect, get_object_or_404, reverse
from django.views.generic import TemplateView, UpdateView
from .models import Post, Comment
from .forms import AddPostForm, CommentForm, search_post, CommentUForm, ReplyForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse

# Create your views here.

def PostView(request):
    form = search_post
    posts = Post.objects.all().order_by('-created_at')

    #search
    if 'q' in request.GET:
        form = search_post(request.GET)
        if form.is_valid():
            q = form.cleaned_data['q']
            
            posts = Post.objects.filter(title__icontains=q).order_by('-created_at')

    #pagination
    page = request.GET.get('page', 1)

    paginator = Paginator(posts, 9)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

            
    
    
    return render(request, 'posts/posts.html', {'form':form,'posts': posts})

def post_detail(request, id):
    post = get_object_or_404(Post, pk=id)
    
    
    new_comment = None
    new_reply = None
    comment_form = CommentForm()
    reply_form = ReplyForm()
    # Comment posted
    
    if request.method == 'POST':
        if request.POST.get('form_type') == 'comment':
            comment_form = CommentForm(data=request.POST)
            if comment_form.is_valid():

                # Create Comment object but don't save to database yet
                new_comment = comment_form.save(commit=False)
                # Assign the current post to the comment
                new_comment.post = post
                new_comment.author = request.user
                # Save the comment to the database
                new_comment.save()
                return redirect('posts:post_details', id)
                # return render(request, 'posts/post_details.html')
            
        else:
            # request.POST.get('form_type') == 'reply':
            reply_form = ReplyForm(data=request.POST)
            if reply_form.is_valid():
                # Create Comment object but don't save to database yet

                parent_id = int(request.POST.get('form_type'))
                new_reply = reply_form.save(commit=False)
                # Assign the current post to the comment
                new_reply.comment = get_object_or_404(Comment, id=parent_id)
                new_reply.author = request.user
                # Save the comment to the database
                new_reply.save()
                print(parent_id)
                return redirect('posts:post_details', new_reply.comment.post_id)

                # return render(request, 'posts/post_details.html')
    
    else:
        return render(request,'posts/post_details.html', {'post': post,
                                           'comment_form': comment_form,
                                           'reply_form': reply_form,}
                )

@login_required
def add_post(request):
    context ={}
    form = AddPostForm(request.POST ,request.FILES)
    if form.is_valid():
        instance = form.save(commit=False)
        instance.author = request.user
        instance.save()

        return redirect('posts:post_details', instance.pk)


    context['form'] = form

    return render(request, 'posts/add_post.html', context)

def update_post(request, id):
        # dictionary for initial data with
    # field names as keys
    context = {}
 
    # fetch the object related to passed id
    obj = get_object_or_404(Post, id = id)
 
    # pass the object as instance in form
    form = AddPostForm(request.POST or None, instance = obj)
 
    # save the data from the form and
    # redirect to detail_view
    if form.is_valid():
        form.save()
        return redirect('posts:post_details', id)
 
    # add form dictionary to context
    context["form"] = form
 
    return render(request, "posts/update_view.html", context)

def delete_post(request, id):
    # dictionary for initial data with
    # field names as keys
    context ={}
 
    # fetch the object related to passed id
    obj = get_object_or_404(Post, id = id)
 
 
    if request.method =="POST":
        # delete object
        obj.delete()
        # after deleting redirect to
        # home page
        return redirect("posts:allposts")
    context['post'] = obj
 
    return render(request, "posts/delete_view.html", context)


def update_comment(request, id, id1):

    context = {}
    obj = get_object_or_404(Comment, id=id1)
    form = CommentUForm(request.POST or None, instance= obj)
    if form.is_valid():
        form.save()
        return redirect('posts:post_details', id)
    context['form'] = form

    return render(request, 'posts/update_comment.html', {'form': form})

def delete_comment(request, id, id1):
    context = {}
    obj = get_object_or_404(Comment, id=id1)

    if request.POST:
        obj.delete()
        return redirect('posts:post_details', id)
    
    context['post'] = id
    print(context)
    return render(request, "posts/delete_comment.html", context)
    

