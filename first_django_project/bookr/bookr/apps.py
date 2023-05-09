from django.contrib.admin.apps import AdminConfig
from django.apps import AppConfig

class ReviewsAdminConfig(AdminConfig):
    default_site = 'bookr.admin.BookrAdminSite'
