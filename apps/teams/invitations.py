from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.translation import gettext_lazy as _
from qualifeed_app.settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD
from apps.users.models import CustomUser
from .models import Invitation


def send_invitation(invitation):
    project_name = settings.PROJECT_METADATA['NAME']
    email_context = {
        'invitation': invitation,
        'project_name': project_name,
    }
    from_email = EMAIL_HOST_USER
    auth_user = EMAIL_HOST_USER
    auth_password = EMAIL_HOST_PASSWORD
    #import ipdb;
    #ipdb.set_trace()
    send_mail(
        subject=_("You're invited to {}!").format(project_name),
        message=render_to_string('teams/email/invitation.txt', context=email_context),
        from_email= from_email,
        recipient_list=[invitation.email],
        fail_silently=False,
        html_message=render_to_string('teams/email/invitation.html', context=email_context),
        auth_user =auth_user,
        auth_password =auth_password
    )


def process_invitation(invitation: Invitation, user: CustomUser):
    invitation.team.members.add(user, through_defaults={'role': invitation.role})
    invitation.is_accepted = True
    invitation.accepted_by = user
    invitation.save()


def get_invitation_id_from_request(request):
    return (
        # URL takes precedence over session/cookie
        request.GET.get('invitation_id')
        or request.session.get('invitation_id')
    )


def clear_invite_from_session(request):
    if 'invitation_id' in request.session:
        del request.session['invitation_id']
