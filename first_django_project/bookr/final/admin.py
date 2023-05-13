from django.contrib import admin

from .models import Reservation, Restaurant, Menu , home


class ReservationAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Date')


class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')


class MenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant_id')

class homeAdmin(admin.ModelAdmin):
    list_display = ('name_res', 'about_res')


# Register your models here.

admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(home, homeAdmin)
