# -*- coding: utf-8 -*-
from django import forms
from django.http import QueryDict
from rides.models import Location


class SearchForm(forms.Form):
    origin = forms.ModelChoiceField(
        label='Važiuoja iš',
        initial=None,
        queryset=Location.objects.order_by('name').all())
    destination = forms.ModelChoiceField(
        label='Važiuoja į',
        initial=None,
        queryset=Location.objects.order_by('name').all())
    is_looking_for = forms.BooleanField(
        initial=False,
        required=False,
        label='',
        widget=forms.RadioSelect(
            choices=(
                (False, 'Siūlo'),
                (True, 'Ieško')
            )
        )
    )

    @property
    def origin_value(self):
        return self['origin'].value()

    @property
    def destination_value(self):
        return self['destination'].value()

    @property
    def is_looking_for_value(self):
        value = self['is_looking_for'].value()
        if isinstance(value, str) or isinstance(value, unicode):
            if value == 'True':
                return True
            elif value == 'False':
                return False
            else:
                return None
        else:
            return value
