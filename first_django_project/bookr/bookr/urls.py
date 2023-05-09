import namespace as namespace
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

import reviews.views

from reviews import views


urlpatterns = [
    path('accounts/', include(('django.contrib.auth.urls', 'auth'), namespace='accounts')),
    path('accounts/profile/', reviews.views.profile, name='profile'),
    path('', reviews.views.index),
    path('greet/', reviews.views.greeting_view, name='greeting'),
    path('admin/', admin.site.urls),
    path('books/', reviews.views.book_list),
    path('books-search/', reviews.views.book_search),
    path('books/<int:id>/', reviews.views.book_detail, name='book_detail'),
    path('publishers/<int:pk>/', views.publisher_edit, name='publisher_edit'),
    path('publishers/new/', views.publisher_edit, name='publisher_create'),
    path('books/<int:book_pk>/reviews/new/', views.review_edit, name='review_create'),
    path('books/<int:book_pk>/reviews/<int:review_pk>/', views.review_edit, name='review_edit'),
    path('books/<int:pk>/media/', views.book_media, name='book_media')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
