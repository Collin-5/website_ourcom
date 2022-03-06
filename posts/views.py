from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import TemplateView
from .models import Post, Comment
from .forms import AddPostForm, CommentForm, search_post
from django.contrib.auth.decorators import login_required

# Create your views here.

def PostView(request):
    form = search_post
    posts = Post.objects.all()

    if 'q' in request.GET:
        form = search_post(request.GET)
        if form.is_valid():
            q = form.cleaned_data['q']
            
            posts = Post.objects.filter(title__icontains=q)
            
    
    
    return render(request, 'posts/posts.html', {'form':form,'posts': posts})

def post_detail(request, id):
    post = get_object_or_404(Post, pk=id)
    
    
    new_comment = None
    # Comment posted
    
    if request.method == 'POST':
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
    else:
        comment_form = CommentForm()
    
    return render(request,'posts/post_details.html', {'post': post,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form}
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
 
    return render(request, "posts/delete_view.html", context)


