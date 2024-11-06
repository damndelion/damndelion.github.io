from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, BadHeaderError, HttpResponseRedirect
from django.contrib import messages
from PIL import Image
from .models import Restaurant, Reservation, Menu, home, Photo, Basket
from .utils import average_rating
from .forms import NewUserForm
from django.conf import settings
from django.utils import timezone
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.urls import reverse
from django.conf import settings

from io import BytesIO
from django.core.files.images import ImageFile
import os


def index(request):
    homes = home.objects.filter()
    home_list = []
    for homess in homes:
        home_list.append({'homess' : homess})
    return render(request, "home.html", {'home' : home_list})


def change(request):
    username = request.user.username
    reservations = Reservation.objects.filter(Username=username)
    reservation_list = []
    for reservation in reservations:
        title = get_object_or_404(Restaurant, title=reservation.Res_name)
        logo = title.logo.url
        reservation_list.append({'logo': logo, 'reservation': reservation})

    if request.method == 'POST':
        Img_path = request.POST.get("photo")
        Img_path = "ava/" + Img_path
        ava = Photo.objects.filter(username=username).update(avatar=Img_path)
        change = ""

    ava = get_object_or_404(Photo, username=username)
    photo = ava.avatar
    return render(request, 'profile.html', {'reservation_list': reservation_list, "photo": photo, "change": "change"})


@login_required
def profile(request):
    username = request.user.username
    reservations = Reservation.objects.filter(Username=username)
    basket = Basket.objects.filter(Username=username).first()
    reservation_list = []
    for reservation in reservations:
        title = get_object_or_404(Restaurant, title=reservation.Res_name)
        logo = title.logo.url
        reservation_list.append({'logo': logo, 'reservation': reservation})

    ava = get_object_or_404(Photo, username=username)
    photo = ava.avatar
    if not photo:
        photo = ''

    basket_items = basket.items if basket else {}
    menu_items = []
    if basket_items:
        for item_id, quantity in basket_items.items():
            menu_item = get_object_or_404(Menu, id=item_id)  # Get the menu item by ID
            menu_items.append({
                'name': menu_item.name,
                'price': menu_item.price,
                'img_url': menu_item.img.url,  # Get the image URL
                'quantity': quantity,
            })
    return render(request, 'profile.html', {'reservation_list': reservation_list, "photo": photo, 'menu_items': menu_items})




@login_required
def reservation(request):
    restaurants = Restaurant.objects.all()
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

        subject = "RESERVATION"
        message = "Name: {name},\n" \
                  "Phone number: {phone}\n" \
                  "Date: {date}\n" \
                  "Time: {time}\n" \
                  "Number of guests: {num}\n" \
                  "Comment: {comment}\n" \
                  "from Klassy reservation system".format(name=Name, phone=Phone_num, date=Date, time=Time, num=Number,
                                                          comment=Message)

        if subject and message:
            try:
                send_mail(subject, message, settings.EMAIL_HOST_USER, [Email],
                          fail_silently=False)
                message = "Your reservation was sent successfully\n" + message
                send_mail(subject, message, settings.EMAIL_HOST_USER, [Email],
                          fail_silently=False)
            except BadHeaderError:
                return HttpResponse("Invalid header found.")
            messages.success(request, "Your table  was successfully reserved.")
            return HttpResponseRedirect("/reservation")

    return render(request, 'reservation.html', {"restaurants": restaurants})


def login(request):
    return render(request, 'registration/login.html')


def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            user = form.save()
            new = Photo.objects.create(username=username)
            new.save()
            messages.success(request, "Registration successful.")
            return redirect("/accounts/profile/")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request, 'registration/register.html', context={"form": form})


def ItemSearchView(request, id):
    if request.method == 'GET':
        search = request.GET.get('search_item')
        restaurant = get_object_or_404(Restaurant, id=id)
        menu = Menu.objects.filter(restaurant_id=id).filter(name__contains=search)
        return render(request, "restaurant_detail.html", {"restaurant": restaurant,
                                                          "menus": menu, 'id': id, 'search': search})


def logout_view(request):
    logout(request)
    return redirect(reverse('login'))

# views.py
def restaurant_detail(request, restaurant_id, menu_id=None):
    restaurant = get_object_or_404(Restaurant, id=restaurant_id)  # Ensure the restaurant exists
    menu = Menu.objects.filter(restaurant_id=restaurant_id)  # Get all menu items for this restaurant

    if request.method == "POST":
        # Get the menu item that was selected
        item_id = menu_id
        quantity = int(request.POST.get('quantity', 1))
        user = request.user

        # Get or create the basket for the current user
        basket, created = Basket.objects.get_or_create(Username=user.username)

        # Initialize the items dictionary if it's empty
        items = basket.items if basket.items else {}

        # Update items in the basket
        if item_id in items:
            items[item_id] += quantity  # Increment quantity if already in basket
        else:
            items[item_id] = quantity  # Add new item with quantity

        # Save the updated items in the basket
        basket.items = items
        basket.save()

    return render(request, "restaurant_detail.html", {
        "restaurant": restaurant,
        "menus": menu,
        "id": restaurant_id,
        "menu_id": menu_id,
    })
