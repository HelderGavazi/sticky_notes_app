# note_post/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import NotePost


# Create your views here.
def index(request):
    posts = NotePost.objects.all() # Grabbing all the records from the BlogPost table
    return render(request, 'note_post/index.html', {'posts': posts})

def add_post(request):
    if request.method == 'POST':
        author = request.POST.get('author')
        title = request.POST.get('title')
        content = request.POST.get('content')
        # Below is the ORM to create a new post record in the BlogPost table
        NotePost.objects.create(author=author, title=title, content=content)
        # When done, return to the index.html page
        return redirect('index')
    return render(request, 'note_post/add_post.html')

def view_post(request, post_id):
    post = get_object_or_404(NotePost, id=post_id)
    return render(request, 'note_post/view_post.html', {'post': post})
                  
def edit_post(request, post_id):
    post = get_object_or_404(NotePost, id=post_id)
    if request.method == 'POST':
        author = request.POST.get('author')
        title = request.POST.get('title')
        content = request.POST.get('content')
        # Update the BlogPost record
        post.author = author
        post.title = title
        post.content = content
        post.save()
        # Redirect to the view_post page
        return redirect('view_post', post_id=post.id)
    return render(request, 'note_post/edit_post.html', {'post': post})