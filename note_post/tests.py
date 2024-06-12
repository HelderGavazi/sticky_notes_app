from django.test import TestCase
from django.urls import reverse
from .models import NotePost

class NotePostModelTest(TestCase):
    """
    Test case for the NotePost model.
    """

    def setUp(self):
        """
        Set up the test environment by creating a NotePost instance.
        """
        NotePost.objects.create(title='Test Post', content='Test Content', author='Test Author')

    def test_post_content(self):
        """
        Verify the content of the created NotePost instance.
        """
        post = NotePost.objects.get(id=1)
        expected_object_name = f'{post.title}'
        self.assertEqual(expected_object_name, 'Test Post')  # Check if title is 'Test Post'
        self.assertEqual(post.content, 'Test Content')  # Check if content is 'Test Content'
        self.assertEqual(post.author, 'Test Author')  # Check if author is 'Test Author'

    def test_post_str_method(self):
        """
        Ensure the __str__ method returns the post title.
        """
        post = NotePost.objects.get(id=1)
        self.assertEqual(str(post), post.title)  # Check if __str__ returns the title


class NotePostViewTest(TestCase):
    """
    Test case for the views related to NotePost.
    """

    def setUp(self):
        """
        Set up the test environment by creating a NotePost instance.
        """
        self.post = NotePost.objects.create(title='Test Post', content='Test Content', author='Test Author')

    def test_index_view(self):
        """
        Test the index view to ensure it lists all posts.
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)  # Check if response status code is 200
        self.assertContains(response, 'Test Post')  # Check if response contains 'Test Post'
        self.assertTemplateUsed(response, 'note_post/index.html')  # Check if correct template is used

    def test_add_post_view(self):
        """
        Test the add_post view to ensure a post can be added successfully.
        """
        response = self.client.post(reverse('add_post'), {
            'title': 'New Post',
            'content': 'New Content',
            'author': 'New Author'
        })
        self.assertEqual(response.status_code, 302)  # Check if redirect status code is 302
        self.assertEqual(NotePost.objects.last().title, 'New Post')  # Check if the new post is created

    def test_view_post_view(self):
        """
        Test the view_post view to ensure it displays the correct post details.
        """
        response = self.client.get(reverse('view_post', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)  # Check if response status code is 200
        self.assertContains(response, 'Test Post')  # Check if response contains 'Test Post'
        self.assertTemplateUsed(response, 'note_post/view_post.html')  # Check if correct template is used

    def test_edit_post_view_get(self):
        """
        Test the edit_post view to ensure it displays the edit form correctly.
        """
        response = self.client.get(reverse('edit_post', args=[self.post.id]))
        self.assertEqual(response.status_code, 200)  # Check if response status code is 200
        self.assertTemplateUsed(response, 'note_post/edit_post.html')  # Check if correct template is used

    def test_edit_post_view_post(self):
        """
        Test the edit_post view to ensure a post can be edited successfully.
        """
        response = self.client.post(reverse('edit_post', args=[self.post.id]), {
            'title': 'Updated Post',
            'content': 'Updated Content',
            'author': 'Updated Author'
        })
        self.assertEqual(response.status_code, 302)  # Check if redirect status code is 302
        self.post.refresh_from_db()  # Refresh the post instance from the database
        self.assertEqual(self.post.title, 'Updated Post')  # Check if the post title is updated
        self.assertEqual(self.post.content, 'Updated Content')  # Check if the post content is updated
        self.assertEqual(self.post.author, 'Updated Author')  # Check if the post author is updated
