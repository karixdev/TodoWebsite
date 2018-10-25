from django.shortcuts import render
from django.views import View
from .forms import AddFriendForm
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from userauth.models import User
from .models import FriendRequest
from django.contrib.auth.decorators import login_required

class AddFriendView(View):
    def get(self, request):
        form = AddFriendForm()
        return render(request, 'add_friend.html', {'form': form})

    def post(self, request):
        form = AddFriendForm(request.POST)

        ctx = {'form': form}

        if form.is_valid():
            username = form.cleaned_data['username']
            users = self.get_users(request, username)
            ctx['users'] = users

        return render(request, 'add_friend.html', ctx)

    def get_user_by_his_username(self, request, username):
        return User.objects.filter(
            Q(username__icontains=username)
        ).exclude(username=request.user.username)
        
    def are_users_friends(self, request, user):
        sended = FriendRequest.objects.filter(sender=request.user).filter(receiver=user)
        received = FriendRequest.objects.filter(sender=request.user).filter(receiver=request.user)
        return True if len(sended) > 0 or len(received) > 0 else False

    def get_proper_users(self, request, username):
        users = self.get_user_by_his_username(request, username)
        for user in users:
            if not self.are_users_friends(request, user):
                yield {
                    'username': user.username,
                    'id': user.id,
                    'profile_image': user.profile_image.url
                }

    def get_users(self, request, username):
        return [user for user in self.get_proper_users(request, username)]

@login_required
def add_friend(request, id):
    pass