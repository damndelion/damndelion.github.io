from django.contrib import admin

<<<<<<< HEAD
from .models import Reservation, Restaurant, Menu , home

=======
from .models import Reservation, Restaurant, Menu, Photo
>>>>>>> 2f34bbd370707c94f26a085815fd2900099f3aab

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('username', 'avatar')
class ReservationAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Date')


class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('title', 'description')


class MenuAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant_id')

class homeAdmin(admin.ModelAdmin):
    list_display = ('name_res', 'about_res')


# Register your models here.
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(home, homeAdmin)
