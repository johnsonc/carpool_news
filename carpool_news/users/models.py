# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from rides.models import Ride, Route
from arrow_field.model_fields import ArrowField


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

    def get_current_rides(self):
        """
        Return rides which are:
        - Not yet expired
        - Not emailed to that user yet
        - Are of the defined type (is_looking_for)
        """
        rides = [
            ride for ride in self.route.rides.filter(
                is_expired=False,
                is_looking_for=self.is_looking_for)
            # Not emailed yet
            if not EmailedRide.objects.filter(
                user=self.user, ride=ride).exists()
        ]
        return rides


class EmailedRide(models.Model):
    """
    User and ride ad mapping for keeping track what was emailed to users
    """
    user = models.ForeignKey(User, related_name='emailed_rides')
    ride = models.ForeignKey(Ride, related_name='emailed_users')
    email_date = ArrowField()


def get_rides_to_email(user):
    """
    Find rides which are relevant to user
    and not yet emailed to him
    """
    rides = list(set([
        # Duplicates possible, as the same ride can belong to multiple routes
        ride
        for user_route in UserRoute.objects.filter(user=user)
        for ride in user_route.get_current_rides()
    ]))
    return rides
