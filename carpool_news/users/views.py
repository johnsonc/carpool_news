from django.shortcuts import render
import django.contrib.auth as auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from users.forms import UserForm


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username, password=password)
        if user:
            auth.login(request, user)
            # login_required decorator redirect
            if 'next' in request.POST and request.POST['next'] != '':
                return HttpResponseRedirect(request.POST['next'])
            else:
                return HttpResponseRedirect('/')
        else:
            return render(request, 'users/login.html', {
                'error_message': 'Login failed',
            })
    else:
        return render(request, 'users/login.html', {
            # login_required decorator redirect
            'next': request.GET['next'] if 'next' in request.GET else '',
        })


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


def register(request):
    if request.method == 'POST':
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()

            # Login and redirect to root url
            user = auth.authenticate(
                username=request.POST['username'],
                password=request.POST['password'])
            auth.login(request, user)
            return HttpResponseRedirect('/')
    else:
        user_form = UserForm()

    return render(
        request,
        'users/register.html', {
            'form': user_form,
        })
