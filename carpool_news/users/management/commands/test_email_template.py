# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.template import Template, Context
from django.template.loader import get_template
from django.contrib.auth.models import User
from users.models import get_rides_to_email


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        dest_file = args[0]
        user = User.objects.get(username='testas')
        rides = get_rides_to_email(user)
        # self.stdout.write(dest_file)
        html_content = get_template(
            'users/email_lite.html').render(Context({
                'user': user,
                'rides': rides,
            }))
        with open(dest_file, 'w') as f:
            f.write(html_content.encode('utf8'))
