from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from .models import Book, Contributor, Publisher, Review
from .utils import average_rating
from .forms import PublisherForm, SearchForm, ReviewForm, BookMediaForm, NewUserForm
from django.utils import timezone
from django.conf import settings

from io import BytesIO
from django.core.files.images import ImageFile
import os

def index(request):
    return render(request, "home.html")


@login_required
def profile(request):
    return render(request, 'profile.html')


@login_required
def reservation(request):
    return render(request, 'reservation.html')


def login(request):
    return render(request, 'registration/login.html')


def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Registration successful.")
            return redirect("/accounts/profile/")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request, 'registration/register.html', context={"form": form})
