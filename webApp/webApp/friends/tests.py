from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from webApp.friends.models import FriendRequest, Friendship

User = get_user_model()


class FriendRequestViewsTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(username='alice', password='pass123')
        self.user2 = User.objects.create_user(username='bob', password='pass123')
        self.send_url = reverse('send-friend-request', kwargs={'user_id': self.user2.id})
        self.friend_requests_url = reverse('friend-requests')

    def test_send_friend_request(self):
        self.client.login(username='alice', password='pass123')
        response = self.client.post(self.send_url)

        self.assertEqual(response.status_code, 302)
        self.assertTrue(FriendRequest.objects.filter(from_user=self.user1, to_user=self.user2).exists())

    def test_send_to_self(self):
        self.client.login(username='alice', password='pass123')
        url = reverse('send-friend-request', kwargs={'user_id': self.user1.id})
        response = self.client.post(url)

        self.assertRedirects(response, reverse('profile-view', kwargs={'username': 'alice'}))
        self.assertFalse(FriendRequest.objects.exists())

    def test_duplicate_friend_request(self):
        FriendRequest.objects.create(from_user=self.user1, to_user=self.user2)
        self.client.login(username='alice', password='pass123')
        response = self.client.post(self.send_url)

        self.assertRedirects(response, reverse('profile-view', kwargs={'username': 'bob'}))
        self.assertEqual(FriendRequest.objects.filter(from_user=self.user1, to_user=self.user2).count(), 1)


class AcceptRejectFriendRequestTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.sender = User.objects.create_user(username='alice', password='pass123')
        self.receiver = User.objects.create_user(username='bob', password='pass123')
        self.friend_request = FriendRequest.objects.create(from_user=self.sender, to_user=self.receiver)

    def test_accept_friend_request(self):
        self.client.login(username='bob', password='pass123')
        url = reverse('accept-friend-request', kwargs={'request_id': self.friend_request.id})
        response = self.client.post(url)

        self.assertRedirects(response, reverse('friend-requests'))
        self.assertFalse(FriendRequest.objects.filter(id=self.friend_request.id).exists())
        self.assertIn(self.sender, self.receiver.friendship.friends.all())
        self.assertIn(self.receiver, self.sender.friendship.friends.all())

    def test_reject_friend_request(self):
        self.client.login(username='bob', password='pass123')
        url = reverse('reject-friend-request', kwargs={'request_id': self.friend_request.id})
        response = self.client.post(url)

        self.assertRedirects(response, reverse('friend-requests'))
        self.assertFalse(FriendRequest.objects.filter(id=self.friend_request.id).exists())


class FriendListViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='alice', password='pass123')
        self.friend = User.objects.create_user(username='bob', password='pass123')
        friendship = Friendship.objects.create(user=self.user)
        friendship.friends.add(self.friend)
        self.url = reverse('friend-list-user', kwargs={'user_id': self.user.id})

    def test_friend_list_view(self):
        self.client.login(username='alice', password='pass123')
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'friends/friend_list.html')
        self.assertIn(self.friend, response.context['friends'])


class FriendRequestListViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='alice', password='pass123')
        self.sender = User.objects.create_user(username='bob', password='pass123')
        FriendRequest.objects.create(from_user=self.sender, to_user=self.user)
        self.url = reverse('friend-requests')

    def test_request_list_view(self):
        self.client.login(username='alice', password='pass123')
        response = self.client.get(self.url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'friends/friend_requests.html')
        self.assertEqual(len(response.context['requests_received']), 1)


class RemoveFriendViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='alice', password='pass123')
        self.friend = User.objects.create_user(username='bob', password='pass123')

        self.friendship1 = Friendship.objects.create(user=self.user)
        self.friendship2 = Friendship.objects.create(user=self.friend)
        self.friendship1.friends.add(self.friend)
        self.friendship2.friends.add(self.user)

        self.url = reverse('remove-friend', kwargs={'user_id': self.friend.id})

    def test_remove_friend(self):
        self.client.login(username='alice', password='pass123')
        response = self.client.post(self.url)

        self.assertRedirects(response, reverse('friend-list-user', kwargs={'user_id': self.user.id}))
        self.assertNotIn(self.friend, self.user.friendship.friends.all())
        self.assertNotIn(self.user, self.friend.friendship.friends.all())

