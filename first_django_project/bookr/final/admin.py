from django.contrib import admin

from .models import Reservation, Restaurant, Menu , home, Basket
from .models import Reservation, Restaurant, Menu, Photo

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('username', 'avatar')


class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')


class MenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant_id')

class homeAdmin(admin.ModelAdmin):
    list_display = ('name_res', 'about_res')

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Date')




admin.site.register(Reservation, ReservationAdmin)


# Register your models here.
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(home, homeAdmin)
admin.site.register(Basket)
