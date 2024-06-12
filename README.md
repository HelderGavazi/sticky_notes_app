Here’s an updated version of the Django Sticky Notes app guide with added comments to explain each part of the scripts and an included model class diagram.

*) Read the file incluided "Sticky_Notes_App Design Diagrams" (.pdf) for App blue print!

### Django Sticky Notes App Guide

This guide will walk you through the process of creating a Sticky Notes app using Django. It covers setting up your project, designing models, creating views and templates, handling static files, and configuring URLs.

#### Project Structure

```plaintext
Work_Space/
    .venv/
    Sticky_Notes_project_folder/
        |
        └── static/css/note_post/
        |
        └── note_post/
            |
            └── templates/note_post/
                ├── partials/
                ├── add_post.html
                ├── edit_post.html
                ├── view_post.html
                ├── index.html
                ├── base.html
        |
        └── Sticky_Notes_project/
```

### 1. Setting Up the Project

#### 1.1 Create a Virtual Environment

Open your terminal and navigate to your `Work_Space` directory. Then create a virtual environment:

```bash
python -m venv .venv
```

Activate the virtual environment:

- On Windows:

  ```bash
  .venv\Scripts\activate
  ```

- On macOS/Linux:

  ```bash
  source .venv/bin/activate
  ```

#### 1.2 Install Django

Install Django using pip:

```bash
pip install django
```

#### 1.3 Create Django Project

Create a new Django project called `Sticky_Notes_project`:

```bash
django-admin startproject Sticky_Notes_project
```

Navigate into the project directory:

```bash
cd Sticky_Notes_project
```

#### 1.4 Create Sticky Notes App

Create a new app called `note_post`:

```bash
python manage.py startapp note_post
```

### 2. Configure Project Settings

#### 2.1 Add App to Installed Apps

In `Sticky_Notes_project/settings.py`, add `note_post` to the `INSTALLED_APPS` list:

```python
INSTALLED_APPS = [
    ...
    'note_post',
]
```

### 3. Design Models

In `note_post/models.py`, define the model for sticky notes:

```python
from django.db import models

# Define the NotePost model with fields for title, content, and created_at timestamp
class NotePost(models.Model):
    title = models.CharField(max_length=100)  # Title of the note, max length 100 characters
    content = models.TextField()  # Content of the note
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp when the note is created, automatically set on creation
    
    def __str__(self):
        return self.title  # String representation of the note, showing its title
```

Run migrations to create the model in the database:

```bash
python manage.py makemigrations
python manage.py migrate
```

### 4. Create Views

In `note_post/views.py`, create views for CRUD operations:

```python
from django.shortcuts import render, get_object_or_404, redirect
from .models import NotePost
from .forms import NotePostForm

# View for listing all notes
def index(request):
    notes = NotePost.objects.all()  # Retrieve all notes from the database
    return render(request, 'note_post/index.html', {'notes': notes})

# View for displaying a single note
def view_post(request, pk):
    note = get_object_or_404(NotePost, pk=pk)  # Retrieve the note with the given primary key (pk)
    return render(request, 'note_post/view_post.html', {'note': note})

# View for adding a new note
def add_post(request):
    if request.method == "POST":
        form = NotePostForm(request.POST)  # Create a form instance with POST data
        if form.is_valid():
            form.save()  # Save the new note to the database
            return redirect('index')  # Redirect to the index page
    else:
        form = NotePostForm()  # Create an empty form instance
    return render(request, 'note_post/add_post.html', {'form': form})

# View for editing an existing note
def edit_post(request, pk):
    note = get_object_or_404(NotePost, pk=pk)  # Retrieve the note with the given primary key (pk)
    if request.method == "POST":
        form = NotePostForm(request.POST, instance=note)  # Create a form instance with POST data and the note to be edited
        if form.is_valid():
            form.save()  # Save the changes to the note
            return redirect('index')  # Redirect to the index page
    else:
        form = NotePostForm(instance=note)  # Create a form instance with the note to be edited
    return render(request, 'note_post/edit_post.html', {'form': form})

# View for deleting a note
def delete_post(request, pk):
    note = get_object_or_404(NotePost, pk=pk)  # Retrieve the note with the given primary key (pk)
    if request.method == "POST":
        note.delete()  # Delete the note from the database
        return redirect('index')  # Redirect to the index page
    return render(request, 'note_post/delete_post.html', {'note': note})
```

### 5. Create Forms

In `note_post/forms.py`, create a form for the `NotePost` model:

```python
from django import forms
from .models import NotePost

# Create a form for the NotePost model
class NotePostForm(forms.ModelForm):
    class Meta:
        model = NotePost  # Specify the model to use
        fields = ['title', 'content']  # Specify the fields to include in the form
```

### 6. Configure URLs

In `note_post/urls.py`, configure the URL patterns:

```python
from django.urls import path
from . import views

# Define URL patterns for the note_post app
urlpatterns = [
    path('', views.index, name='index'),  # URL for listing all notes
    path('post/<int:pk>/', views.view_post, name='view_post'),  # URL for viewing a single note
    path('post/add/', views.add_post, name='add_post'),  # URL for adding a new note
    path('post/<int:pk>/edit/', views.edit_post, name='edit_post'),  # URL for editing a note
    path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),  # URL for deleting a note
]
```

In `Sticky_Notes_project/urls.py`, include the `note_post` URLs:

```python
from django.contrib import admin
from django.urls import path, include

# Define URL patterns for the project
urlpatterns = [
    path('admin/', admin.site.urls),  # URL for the admin site
    path('', include('note_post.urls')),  # Include the URL patterns from the note_post app
]
```

### 7. Create Templates

Create templates in `note_post/templates/note_post/`:

#### 7.1 Base Template (`base.html`)

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Sticky Notes</title>
    <link rel="stylesheet" href="{% static 'css/note_post/styles.css' %}">
</head>
<body>
    <header>
        <h1>Sticky Notes</h1>
        <nav>
            <a href="{% url 'index' %}">Home</a>
            <a href="{% url 'add_post' %}">Add Note</a>
        </nav>
    </header>
    <main>
        {% block content %}
        {% endblock %}
    </main>
</body>
</html>
```

#### 7.2 Index Template (`index.html`)

```html
{% extends 'note_post/base.html' %}

{% block content %}
    <h2>Notes</h2>
    <ul>
        {% for note in notes %}
            <li>
                <a href="{% url 'view_post' note.pk %}">{{ note.title }}</a>
                <a href="{% url 'edit_post' note.pk %}">Edit</a>
                <a href="{% url 'delete_post' note.pk %}">Delete</a>
            </li>
        {% endfor %}
    </ul>
{% endblock %}
```

#### 7.3 View Post Template (`view_post.html`)

```html
{% extends 'note_post/base.html' %}

{% block content %}
    <h2>{{ note.title }}</h2>
    <p>{{ note.content }}</p>
    <a href="{% url 'edit_post' note.pk %}">Edit</a>
    <a href="{% url 'delete_post' note.pk %}">Delete</a>
{% endblock %}
```

#### 7.4 Add/Edit Post Template (`add_post.html` / `edit_post.html`)

```html
{% extends 'note_post/base.html' %}

{% block content %}
    <h2>{% if form.instance.pk %}Edit{% else %}Add{% endif %} Note</h2>
    <form method="post">
        {% csrf_token %}
        {{ form.as_p }}
        <button type="submit">Save</button>
    </form>
{% endblock %}
```

#### 7.5 Delete Post Template (`delete_post.html`)

```html
{% extends 'note_post/base.html' %

}

{% block content %}
    <h2>Delete Note</h2>
    <p>Are you sure you want to delete "{{ note.title }}"?</p>
    <form method="post">
        {% csrf_token %}
        <button type="submit">Yes, delete</button>
        <a href="{% url 'index' %}">Cancel</a>
    </form>
{% endblock %}
```

### 8. Styling with CSS

Create a CSS file in `static/css/note_post/`:

#### styles.css

```css
body {
    font-family: Arial, sans-serif;
}

header {
    background-color: #f8f9fa;
    padding: 1em;
    text-align: center;
}

nav a {
    margin: 0 1em;
    text-decoration: none;
    color: #007bff;
}

nav a:hover {
    text-decoration: underline;
}

main {
    margin: 2em auto;
    max-width: 800px;
}

h2 {
    color: #343a40;
}
```

### 9. Collect Static Files

Configure your Django project to collect static files:

In `Sticky_Notes_project/settings.py`, add:

```python
STATIC_URL = '/static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
```

Collect static files:

```bash
python manage.py collectstatic
```

### 10. Run the Development Server

Run the development server to test your application:

```bash
python manage.py runserver
```

Open your web browser and navigate to `http://127.0.0.1:8000/` to view and interact with your Sticky Notes app.

---

### Class Model Diagram

Here is a class diagram to illustrate the structure of the NotePost model:

```plaintext
+-------------------+
|     NotePost      |
+-------------------+
| - id: AutoField   |
| - title: CharField|
| - content: TextField|
| - created_at: DateTimeField |
+-------------------+
| + __str__()       |
+-------------------+
```

- **NotePost**: This is the model class representing a sticky note.
  - **id**: An automatically generated field for the primary key.
  - **title**: A character field for the title of the note.
  - **content**: A text field for the content of the note.
  - **created_at**: A date-time field that stores when the note was created.
  - **__str__()**: A method to return the string representation of the note, which is its title.

---

By following this guide, you'll have a fully functional Sticky Notes app built with Django. The comments within the code help to understand the functionality of each part, making it easier to follow and modify as needed.
