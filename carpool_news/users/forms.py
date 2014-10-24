from django import forms
from django.contrib.auth.models import User


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
