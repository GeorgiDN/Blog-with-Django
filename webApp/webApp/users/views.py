import os
from asgiref.sync import sync_to_async, async_to_sync
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib import messages
from django.views.generic import CreateView, View, DetailView, ListView
from django.urls import reverse_lazy
from webApp.blocking.views import get_blocked_users
from webApp.friends.models import FriendRequest, Friendship
from webApp.users.forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm, ChangePasswordForm
from webApp.users.models import Profile
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
User = get_user_model()


class AppUserRegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('blog-home')

    async def send_welcome_email(self, user_email, username):
        await sync_to_async(send_mail)(
            f'Welcome to our blog {username}!',
            'Thank you for you registration!',
            os.environ['EMAIL_HOST_USER'],
            [user_email],
            fail_silently=False,
        )

    def form_valid(self, form):
        response = super().form_valid(form)

        login(self.request, self.object)
        messages.success(self.request, 'Your account has been created!')

        email = self.object.email
        username = self.object.username
        async_to_sync(self.send_welcome_email)(email, username)

        return response


class ProfileView(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.user_profile)

        requests_count = FriendRequest.objects.filter(to_user=self.request.user).count()

        context = {
            'u_form': u_form,
            'p_form': p_form,
            'requests_count': requests_count,
        }

        return render(request, 'users/profile.html', context)

    def post(self, request, *args, **kwargs):
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.user_profile)

        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(self.request, 'Your profile has been updated!')
            return redirect('profile')

        context = {
            'u_form': u_form,
            'p_form': p_form
        }

        return render(request, 'users/profile.html', context)


class ProfileDeleteView(LoginRequiredMixin, UserPassesTestMixin, View):
    template_name = 'users/profile-delete-page.html'
    success_url = reverse_lazy('login')

    def test_func(self):
        profile = get_object_or_404(Profile, pk=self.kwargs["pk"])
        return self.request.user == profile.user

    def get(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, pk=self.kwargs["pk"])
        return render(request, self.template_name, {'profile': profile})

    def post(self, request, *args, **kwargs):
        profile = get_object_or_404(Profile, pk=self.kwargs["pk"])
        user = profile.user

        user.delete()
        profile.delete()

        return redirect(self.success_url)


class ConfirmRemoveImageView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        return render(request, 'users/confirm_remove_image.html')

    def post(self, request, *args, **kwargs):
        profile = request.user.user_profile
        profile.image = 'default.jpg'
        profile.save()
        messages.success(request, 'Your profile image has been removed!')
        return redirect('profile')


class ProfileDetailView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'users/profile_page.html'
    context_object_name = 'profile'

    def get_object(self, **kwargs):
        username = self.kwargs.get('username')
        return get_object_or_404(Profile, user__username=username)

    def dispatch(self, request, *args, **kwargs):
        username = self.kwargs.get('username')
        to_user = get_object_or_404(User, username=username)

        if request.user.is_authenticated:
            current_user = request.user
            if current_user.id in get_blocked_users(to_user) or to_user.id in get_blocked_users(current_user):
                return HttpResponseForbidden("You cannot view this profile.")

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        current_user = self.request.user
        username = self.kwargs.get('username')
        to_user = get_object_or_404(User, username=username)
        is_friend = Friendship.objects.filter(user=current_user, friends=to_user).exists()
        is_send_request = FriendRequest.objects.filter(from_user=current_user, to_user=to_user).exists()
        my_profile_page = current_user == to_user

        context['is_friend'] = is_friend
        context['is_send_request'] = is_send_request
        context['my_profile_page'] = my_profile_page
        return context


class UsersListView(LoginRequiredMixin, ListView):
    template_name = 'users/users_list.html'
    context_object_name = 'users'
    paginate_by = 10

    def get_queryset(self):
        blocked_ids = get_blocked_users(self.request.user)
        queryset = User.objects.exclude(id__in=blocked_ids).order_by('username')

        search_query = self.request.GET.get('q', '').strip()
        if search_query:
            queryset = queryset.filter(
                Q(username__icontains=search_query) |
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('q', '')
        return context


def update_password(request):
    if request.user.is_authenticated:
        current_user = request.user
        if request.method == 'POST':
            form = ChangePasswordForm(current_user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Your password has been changed!')
                return redirect('login')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)
                    return redirect('update-password')
        else:
            form = ChangePasswordForm(current_user)

    else:
        messages.error(request, 'You are not logged in!')
        return redirect('login')

    context = {
        'form': form,
    }

    return render(request, 'users/update_password.html', context)
