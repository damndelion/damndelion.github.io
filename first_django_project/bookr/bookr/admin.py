from django.contrib import admin

from first_django_project.bookr.reviews.models import Book


class BookrAdminSite(admin.AdminSite):
    title_header = 'Bookr Admin'
    site_header = 'Bookr administration'
    index_title = 'Bookr site admin'

