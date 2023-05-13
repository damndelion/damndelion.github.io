from django.contrib import admin
from final.models import home

@admin.register(home)
class ContactAdmin(admin.ModelAdmin):
    pass



class BookrAdminSite(admin.AdminSite):
    title_header = 'Bookr Admin'
    site_header = 'Bookr administration'
    index_title = 'Bookr site admin'

