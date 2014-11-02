# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from rides.models import Route


class UserRoute(models.Model):
    """
    Many-to-many mapping between users and routes
    with additional details of ad type
    """
    user = models.ForeignKey(User)
    route = models.ForeignKey(Route)

    # Type of route ads user is interested in
    is_looking_for = models.BooleanField(
        default=False,
        choices=((False, 'Siūlo'), (True, 'Ieško')))
