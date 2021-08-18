"""Celery tasks."""

# Django
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from django.urls import reverse

# Models
from django.contrib.auth import get_user_model

# Celery
from config import celery_app

# Utilities
from datetime import timedelta
import time
import jwt

User = get_user_model()


@celery_app.task()
def get_users_count():
    """A pointless Celery task to demonstrate usage."""
    return User.objects.count()


def gen_verification_token(user):
    """Create JWT token that the user can use to verify its account."""

    exp_date = timezone.now() + timedelta(days=3)
    payload = {
        'user': user.username,
        'exp': int(exp_date.timestamp()),
        'type': 'email_confirmation'
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
    return token


@celery_app.task(name='send_confirmation_email', max_retries=3)
def send_confirmation_email(user_pk, current_site, protocol):
    """Send account verification link to given user."""

    user = User.objects.get(pk=user_pk)
    verification_token = gen_verification_token(user)

    # relative_link = reverse('lands')
    relative_link = '/users/verify'
    abs_url = protocol + current_site + relative_link + '?token=' + verification_token

    subject = 'Welcome @{}! Verify your account to start using Farm-management'.format(user.username)
    from_email = 'Farm-management <noreply@farm-management.xyz>'
    content = render_to_string(
        'emails/users/account_verification1.html',
        {'abs_url': abs_url, 'user': user}
    )
    msg = EmailMultiAlternatives(subject, content, from_email, [user.email])
    msg.attach_alternative(content, "text/html")
    msg.send()
