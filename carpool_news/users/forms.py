# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rides.models import Location, Route
from users.models import UserRoute


class UserForm(forms.ModelForm):
    password2 = forms.CharField(max_length=128)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'password2')

    def clean_password2(self):
        """
        Check if both passwords match
        """
        form_data = self.cleaned_data
        if form_data['password'] != form_data['password2']:
            self.add_error('password', "Passwords do not match")
        return form_data


class UserRouteForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        # Current user should be passed from the view (request.user)
        self.user = user
        super(UserRouteForm, self).__init__(*args, **kwargs)

    class Meta:
        model = UserRoute
        fields = ['origin', 'destination', 'is_looking_for']
        widgets = {
            'is_looking_for': forms.RadioSelect()}
        labels = {
            'is_looking_for': 'Tipas'}

    origin = forms.ModelChoiceField(
        queryset=Location.objects.all().order_by('name'),
        label='Pradžia',
        required=True)
    destination = forms.ModelChoiceField(
        queryset=Location.objects.all().order_by('name'),
        label='Pabaiga',
        required=True)

    def clean(self):
        """
        Additional form validation
        """
        super(UserRouteForm, self).clean()

        # Selected origin and destination locations cannot match
        origin = self.cleaned_data['origin']
        destination = self.cleaned_data['destination']
        if origin == destination:
            raise ValidationError(u'Pradžia ir pabaiga negali sutapti')

        # User routes should be unique
        try:
            UserRoute.objects.get(
                user=self.user,
                route__origin=origin,
                route__destination=destination,
                is_looking_for=self.cleaned_data['is_looking_for'])
            raise ValidationError(u'Toks maršrutas jau pasirinktas')
        except UserRoute.DoesNotExist:
            pass

        return self.cleaned_data

    def save(self, commit=True):
        instance = super(UserRouteForm, self).save(commit=False)

        # Get route for specified origin/destination
        origin = self.cleaned_data['origin']
        destination = self.cleaned_data['destination']
        route, created = Route.objects.get_or_create(
            origin=origin,
            destination=destination)
        instance.route = route
        instance.user = self.user   # Set in constructor

        if commit:
            instance.save()
        return instance
