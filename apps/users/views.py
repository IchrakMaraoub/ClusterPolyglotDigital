from allauth_2fa.utils import user_has_valid_totp_device
from allauth.account.utils import send_email_confirmation
from allauth.socialaccount.models import SocialAccount
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils import translation
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_POST

from apps.api.models import UserAPIKey

from .forms import CustomUserChangeForm, UploadAvatarForm
from .helpers import require_email_confirmation, user_has_confirmed_email_address
from .models import CustomUser
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .serializers import CustomUserSerializer, LoginSerializer
from django.contrib.auth import authenticate
from rest_framework import permissions
from rest_framework import views
from rest_framework.response import Response
from django.contrib.auth import authenticate, login,logout

from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from apps.teams.models import Team,Membership
from django.db.models import Q

@login_required
def profile(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save(commit=False)
            user_before_update = CustomUser.objects.get(pk=user.pk)
            need_to_confirm_email = (
                user_before_update.email != user.email
                and require_email_confirmation()
                and not user_has_confirmed_email_address(user, user.email)
            )
            if need_to_confirm_email:
                # don't change it but instead send a confirmation email
                # email will be changed by signal when confirmed
                new_email = user.email
                send_email_confirmation(request, user, signup=False, email=new_email)
                user.email = user_before_update.email
                # recreate the form to avoid populating the previous email in the returned page
                form = CustomUserChangeForm(instance=user)
            user.save()

            user_language = user.language
            if user_language and user_language != translation.get_language():
                translation.activate(user_language)

    else:
        form = CustomUserChangeForm(instance=request.user)
    return render(request, 'account/profile.html', {
        'form': form,
        'active_tab': 'profile',
        'page_title': _('Profile'),
        'api_keys': request.user.api_keys.filter(revoked=False),
        'social_accounts': SocialAccount.objects.filter(user=request.user),
        'user_has_valid_totp_device': user_has_valid_totp_device(request.user),
    })


@login_required
@require_POST
def upload_profile_image(request):
    user = request.user
    form = UploadAvatarForm(request.POST, request.FILES)
    if form.is_valid():
        user.avatar = request.FILES['avatar']
        user.save()
    return HttpResponse(_('Success!'))


@login_required
def create_api_key(request):
    api_key, key = UserAPIKey.objects.create_key(
        name=f"{request.user.get_display_name()} API Key",
        user=request.user
    )
    messages.success(
        request,
        _('API Key created. Your key is: {key}. Save this somewhere safe - you will only see it once!').format(
            key=key,
        ),
    )
    return HttpResponseRedirect(reverse('users:user_profile'))


@login_required
@require_POST
def revoke_api_key(request):
    key_id = request.POST.get('key_id')
    api_key = request.user.api_keys.get(id=key_id)
    api_key.revoked = True
    api_key.save()
    messages.success(
        request,
        _('API Key {key} has been revoked. It can no longer be used to access the site.').format(
            key=api_key.prefix,
        ),
    )
    return HttpResponseRedirect(reverse('users:user_profile'))

    
class LoginView(views.APIView):
    # This view should be accessible also for unauthenticated users.
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        #import ipdb;
        #ipdb.set_trace()
        serializer = LoginSerializer(data=self.request.data,
            context={ 'request': self.request })
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        if serializer.is_valid(raise_exception=True):    
            data = {
                "First name":  user.first_name,
                "Last name": user.last_name,
                "Email address": user.email,
                "Username": user.username
            }
            res = { "response" : "Log in",
                   "data" :  data   
            }
        return Response(res, status=status.HTTP_202_ACCEPTED)
        
        
class UserLogout(views.APIView):
    # This view should be accessible also for unauthenticated users.

    def get(self, request):

        logout(request)

        return Response('User Logged out successfully')
    
class LoginAPI(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        #import ipdb;
        #ipdb.set_trace()
        team_name =  request.data['team']
        del request.data['team']
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        id_team = Team.objects.filter(name=team_name).values('id')[0]['id']
        membership = Membership.objects.filter(Q(user=user) & Q(team=id_team)).first()
        role = membership.role

        response = super(LoginAPI, self).post(request, format=None)
        token = response.data.get('token')
        
        if serializer.is_valid(raise_exception=True):    
            data = {
                "ID" : user.id,
                "First name":  user.first_name,
                "Last name": user.last_name,
                "Email address": user.email,
                "Username": user.username,
                "role":role
            }
            res = { "response" : "Log in",
                    "token": token,
                   "data" :  data   
            }
        return Response(res, status=status.HTTP_202_ACCEPTED)