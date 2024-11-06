from typing import final

from django.contrib import admin
from django.conf import settings
from django.contrib.auth import logout
from django.urls import path, include
from django.conf.urls.static import static


from final.views import *



# urlpatterns = [
#     path('accounts/', include(('django.contrib.auth.urls', 'auth'), namespace='accounts')),
#     path('accounts/profile/', final.views.profile, name='profile'),
#     path('', final.views.index),
#     path('greet/', final.views.greeting_view, name='greeting'),
#     path('admin/', admin.site.urls),
#     path('books/', final.views.book_list),
#     path('books-search/', final.views.book_search),
#     path('books/<int:id>/', final.views.book_detail, name='book_detail'),
#     path('publishers/<int:pk>/', views.publisher_edit, name='publisher_edit'),
#     path('publishers/new/', views.publisher_edit, name='publisher_create'),
#     path('books/<int:book_pk>/final/new/', views.review_edit, name='review_create'),
#     path('books/<int:book_pk>/final/<int:review_pk>/', views.review_edit, name='review_edit'),
#     path('books/<int:pk>/media/', views.book_media, name='book_media')
# ]
# urls.py
urlpatterns = [
    path('accounts/', include(('django.contrib.auth.urls', 'auth'), namespace='accounts')),
    path('restaurant/<int:id>/search', ItemSearchView, name='search_items'),
    path('accounts/profile/', profile, name='profile'),
    path('accounts/profile/change', change, name='change'),
    path('accounts/logout/', logout_view, name='logout'),
    path('', index),
    path('restaurant/<int:restaurant_id>/<int:menu_id>/', restaurant_detail, name='restaurant_detail_menu'),
    path('reservation/', reservation, name='reservation'),
    path('register/', register, name="register"),
    path('admin/', admin.site.urls),
    path('restaurant/<int:id>/', restaurant_detail, name='restaurant_detail'),  # Handles only restaurant_id
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
