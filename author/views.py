from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from .forms import RegisterForm, LoginForm
from .dec import login_denied


@login_denied
def register_view(request):
    form = RegisterForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return HttpResponseRedirect(reverse_lazy('home'))
    context = {
        'form': form,
        'title': 'Register',
        'subtitle': 'register and write',
        'submit': 'Register'
    }
    return render(request, 'generic_form.html', context)


@login_denied
def login_view(request):
    form = LoginForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = User.objects.filter(username=username).first()
        if user and user.check_password(password):
            login(request, user)
            return HttpResponseRedirect(reverse_lazy('home'))
        messages.add_message(request, messages.ERROR, 'user or password incorrect')
    context = {'form': form,
               'title': 'Login',
               'subtitle': 'login site',
               'submit': 'Login'
               }
    return render(request, 'generic_form.html', context)


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('home'))
