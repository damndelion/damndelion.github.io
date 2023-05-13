from django.contrib.auth.decorators import user_passes_test, login_required
from django.core.exceptions import PermissionDenied
from django.core.mail import send_mail
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, BadHeaderError, HttpResponseRedirect
from django.contrib import messages
from PIL import Image
from .models import Restaurant, Reservation, Menu, home
from .utils import average_rating
from .forms import NewUserForm
from django.conf import settings
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
        title = get_object_or_404(Restaurant, title = reservation.Res_name)
        logo = title.logo.url
        reservation_list.append({'logo' : logo,'reservation': reservation})

    return render(request, 'profile.html', {'reservation_list': reservation_list})


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
        messages.success(request, "Your table in \"{}\" was successfully reserved.".format(Res_name))

    return render(request, 'reservation.html', {"restaurants": restaurants})


def login(request):
    return render(request, 'registration/login.html')


def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            user = form.save()  
            new = Photo.objects.create(username = username)
            new.save()
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
                                                          "menus": menu, 'id': id, 'search': search})


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
                                                      "menus": menu, "id": id})


def email(request):
    if request.method == "POST":
        subject = "RESERVATION"
        message = "Name: {name},\n" \
                  "Phone number: {phone}\n" \
                  "Date: {date}\n" \
                  "Time: {time}\n" \
                  "Number of guests: {num}\n" \
                  "Comment: {comment}\n" \
                  "from Klassy reservation system".format(name=request.POST.get('name'),
                                                          phone=request.POST.get('phone'),
                                                          date=request.POST.get('date'), time=request.POST.get('time'),
                                                          num=request.POST.get('number'),
                                                          comment=request.POST.get('message'))

        if subject and message:
            try:
                send_mail(subject, message, 'settings.EMAIL_HOST_USER', ["210103468@stu.sdu.edu.kz"],
                          fail_silently=False)
                message = "Your reservation was sent successfully\n" + message
                send_mail(subject, message, 'settings.EMAIL_HOST_USER', ["210103468@stu.sdu.edu.kz"],
                          fail_silently=False)
            except BadHeaderError:
                return HttpResponse("Invalid header found.")
            messages.success(request, "Your table  was successfully reserved.")
            return HttpResponseRedirect("/reservation")
    return render(request, "reservation.html")


# def home_res(request):
    # homes = home.objects.all()
    # home_list = []
    # for homess in homes:
    #     home_list.append({'homess' :homess})
    # return render(request, 'home.html' , {'home_list': home_list} )



    # if request.metho
    # name_res = request.POST.get('name_res')
    # img_res = request.POST.get('img_res')
    # number_res = request.POST.get('number_res')
    # address_res = request.POST.get('address_res')
    # about_res = request.POST.get('about_res')
    # avg_check = request.POST.get('avg_check')
    # kitchen = request.POST.get('kitchen')
    # work_time = request.POST.get('work_time')
    # seats = request.POST.get('seats')
    # vip_zone = request.POST.get('vip_zone')
    # chef = request.POST.get('chef')
    # about_img = request.POST.get('about_img')
    # map_res = request.POST.get('map_res')
        # homes_list = []
        # for homess in homesis:
        #     homes_list.append({'homess' : homess})
        # return render(request, "home.html", {"name_res": name_res, "img_res": img_res,"number_res" : number_res,
        #                                      "address_res" : address_res, "about_res" : about_res, "avg_check" : avg_check,
        #                                      "kitchen" : kitchen, "work_time" : work_time, "seats" : seats,
        #                                      "vip_zone" : vip_zone, "chef" : chef, "about_img" : about_img, "map_res" : map_res})
        #     return render(request, 'home.html', {'homes_list' :homes_list})