from django.contrib import admin

from .models import Reservation, Restaurant


class ReservationAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Date')


class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')


# Register your models here.

admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Restaurant, RestaurantAdmin)
