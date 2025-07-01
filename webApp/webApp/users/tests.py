from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model

User = get_user_model()


class UserRegistrationTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.register_url = reverse('register')

    def test_register_user_and_redirect(self):
        response = self.client.post(self.register_url, {
            'username': 'testuser',
            'email': 'test@example.com',
            'password1': 'StrongPassword123',
            'password2': 'StrongPassword123'
        })

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('blog-home'))
        self.assertTrue(User.objects.filter(username='testuser').exists())


class ProfileViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='user1', password='pass123')
        self.profile_url = reverse('profile')

    def test_profile_get_authenticated(self):
        self.client.login(username='user1', password='pass123')
        response = self.client.get(self.profile_url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'users/profile.html')
        self.assertIn('u_form', response.context)
        self.assertIn('p_form', response.context)
        self.assertIn('requests_count', response.context)

    def test_profile_post_update(self):
        self.client.login(username='user1', password='pass123')
        response = self.client.post(self.profile_url, {
            'username': 'user1',
            'email': 'newemail@example.com',
            'image': ''
        })

        self.user.refresh_from_db()
        self.assertEqual(response.status_code, 302)
        self.assertEqual(self.user.email, 'newemail@example.com')


class ProfileDeleteViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='user2', password='pass123')
        self.profile = self.user.user_profile
        self.delete_url = reverse('profile-delete', kwargs={'pk': self.profile.pk})

    def test_delete_own_profile(self):
        self.client.login(username='user2', password='pass123')
        response = self.client.post(self.delete_url)

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        self.assertFalse(User.objects.filter(username='user2').exists())

    def test_delete_other_profile_forbidden(self):
        other_user = User.objects.create_user(username='user3', password='pass123')
        self.client.login(username='user3', password='pass123')
        response = self.client.post(self.delete_url)

        self.assertEqual(response.status_code, 403)
