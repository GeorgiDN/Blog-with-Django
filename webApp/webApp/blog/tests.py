from django.test import TestCase, RequestFactory
from django.urls import reverse
from webApp.blocking.views import block_user
from webApp.blog.models import Post
from webApp.common.models import Like
from webApp.blog.views import PostListView, UserPostListView, PostDetailView
from webApp.common.forms import SearchForm
from django.contrib.auth import get_user_model
User = get_user_model()


class BlogViewsTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        self.post = Post.objects.create(
            title='Test Post',
            content='Test Content',
            author=self.user
        )
        self.factory = RequestFactory()

    def test_user_post_list_view(self):
        # Test with authenticated user
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('user-posts', kwargs={'username': 'testuser'}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/user_posts.html')
        self.assertContains(response, 'Test Post')

        response = self.client.get(reverse('user-posts', kwargs={'username': 'nonexistent'}))
        self.assertEqual(response.status_code, 404)

    def test_post_create_view(self):
        self.client.login(username='testuser', password='testpass123')

        response = self.client.get(reverse('post-create'))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('post-create'), {
            'title': 'New Post',
            'content': 'New Content'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(title='New Post').exists())

    def test_post_update_view(self):
        self.client.login(username='testuser', password='testpass123')

        response = self.client.get(reverse('post-update', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('post-update', kwargs={'pk': self.post.pk}), {
            'title': 'Updated Post',
            'content': 'Updated Content'
        })
        self.assertEqual(response.status_code, 302)
        self.post.refresh_from_db()
        self.assertEqual(self.post.title, 'Updated Post')

        other_user = User.objects.create_user('other', 'other@test.com', 'testpass')
        self.client.login(username='other', password='testpass')
        response = self.client.get(reverse('post-update', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 403)

    def test_post_delete_view(self):
        self.client.login(username='testuser', password='testpass123')

        response = self.client.get(reverse('post-delete', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 200)

        response = self.client.post(reverse('post-delete', kwargs={'pk': self.post.pk}))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Post.objects.filter(pk=self.post.pk).exists())

        post = Post.objects.create(title='Other Post', content='Content', author=self.user)
        other_user = User.objects.create_user('other', 'other@test.com', 'testpass')
        self.client.login(username='other', password='testpass')
        response = self.client.post(reverse('post-delete', kwargs={'pk': post.pk}))
        self.assertEqual(response.status_code, 403)

    def test_about_view(self):
        response = self.client.get(reverse('about'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/about.html')
