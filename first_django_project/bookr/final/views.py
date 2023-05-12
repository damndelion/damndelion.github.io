from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib import messages
from PIL import Image
from .models import Restaurant, Reservation, Menu
from .utils import average_rating
from .forms import NewUserForm
from django.utils import timezone
from django.conf import settings

from io import BytesIO
from django.core.files.images import ImageFile
import os


def index(request):
    return render(request, "home.html")


@login_required
def profile(request):
    username = request.user.username
    reservations = Reservation.objects.filter(Username=username)
    reservation_list = []
    for reservation in reservations:
        reservation_list.append({'reservation': reservation})
    return render(request, 'profile.html', {'reservation_list': reservation_list})


@login_required
def reservation(request):
    if request.method == 'POST':
        Username = request.user.username
        Name = request.POST.get('name')
        Email = request.POST.get('email')
        Phone_num = request.POST.get('phone')
        Date = request.POST.get('date')
        Number = request.POST.get('number')
        Time = request.POST.get('time')
        Res_name = request.POST.get('res_name')
        Message = request.POST.get('message')

        reservations = Reservation.objects.filter(Date=Date)
        reservation_list = []
        for reservation in reservations:
            reservation_list.append({'reservation': reservation})

        reservationss = Reservation.objects.filter(Username=Username)
        reservation_list2 = []
        for reservation in reservationss:
            reservation_list2.append({'reservation': reservation})
        if len(reservation_list) > 10:
            messages.error(request, "There are more than 10 reservations on this day. Please choose another day")
            return redirect('profile')

        if len(reservation_list2) > 8:
            messages.error(request, "There are more than 8 reservations on this user")
            return redirect('profile')
        reservation = Reservation.objects.create(Username=Username, Name=Name, Email=Email, Phone_num=Phone_num,
                                                 Date=Date, Number=Number, Time=Time, Res_name=Res_name,
                                                 Message=Message)
        reservation.save()
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

def ItemSearchView(request, id):
    print(id)
    if request.method == 'GET':
        search = request.GET.get('search_item')
        restaurant = get_object_or_404(Restaurant, id=id)
        title = restaurant.title
        description = restaurant.description
        logo = restaurant.logo
        img1 = restaurant.img1
        img2 = restaurant.img2
        img3 = restaurant.img3
        menu = Menu.objects.filter(restaurant_id=id).filter(name__contains=search)
        return render(request, "restaurant_detail.html", {"title": title, "description": description,
                                                          "logo": logo, "img1": img1, "img2": img2, "img3": img3,
                                                          "menus": menu, 'id': id})

def restaurant_detail(request, id):
    restaurant = get_object_or_404(Restaurant, id=id)
    title = restaurant.title
    description = restaurant.description
    logo = restaurant.logo
    img1 = restaurant.img1
    img2 = restaurant.img2
    img3 = restaurant.img3
    menu = Menu.objects.filter(restaurant_id=id)


    return render(request, "restaurant_detail.html", {"title": title, "description": description,
                                                      "logo": logo, "img1": img1, "img2": img2, "img3": img3,
                                                      "menus": menu, "id" : id})

# def book_media(request, pk):
#     book = get_object_or_404(Book, pk=pk)
#     if request.method == "POST":
#         form = BookMediaForm(request.POST, files=request.FILES, instance=book)
#         if form.is_valid():
#             book = form.save(False)
#             cover = form.cleaned_data.get("cover")
#             if cover:
#                 image = Image.open(cover)
#                 image.thumbnail((300, 300))
#                 image_data = BytesIO()
#                 image.save(fp=image_data, format=cover.image.format)
#                 image_file = ImageFile(image_data)
#                 book.cover.save(cover.name, image_file)
#             book.save()
#
#             messages.success(request, "Book \"{}\" was successfully updated.".format(book))
#             return redirect("book_detail", book.pk)
#     else:
#         form = BookMediaForm(instance=book)
#
#     return render(request, "reviews/instance-form.html",
#                   {"instance": book, "form": form, "model_type": "Book", "is_file_upload": True})
