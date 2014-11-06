import arrow
import requests
from django.core.management.base import BaseCommand
from django.template import Context
from django.template.loader import get_template
from django.contrib.auth.models import User
from urlparse import urljoin
from users.models import EmailedRide, get_rides_to_email
from carpool_news.settings import MAIL_API_URL, MAIL_API_KEY
from carpool_news.settings import MAIL_FROM, MAIL_SUBJECT


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        for user in User.objects.all():
            # Ads which might be interesting to this user
            rides = get_rides_to_email(user)
            if rides:
                # Form the email
                mail_from = MAIL_FROM
                mail_to = user.email
                mail_subject = MAIL_SUBJECT
                mail_text = get_template(
                    'users/email_lite.html').render(Context({
                        'user': user,
                        'rides': rides,
                    }))
                # Send it
                response = requests.post(
                    MAIL_API_URL,
                    auth=("api", MAIL_API_KEY),
                    data={
                        "from": mail_from,
                        "to": mail_to,
                        "subject": mail_subject,
                        "html": mail_text,
                    }
                )
                print "%s(%s): %s" % (user.username, user.email, response)
                # Mark these as emailed
                for ride in rides:
                    EmailedRide.objects.create(
                        user=user,
                        ride=ride,
                        email_date=arrow.utcnow())
