from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static


import final.views


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
urlpatterns = [
    path('accounts/', include(('django.contrib.auth.urls', 'auth'), namespace='accounts')),
    path('restaurant/<int:id>/search', final.views.ItemSearchView, name='search_items'),
    path('accounts/profile/', final.views.profile, name='profile'),
    path('accounts/profile/change', final.views.change, name='change'),
    path('accounts/logout/', final.views.profile, name='profile'),
    path('', final.views.index),
    path('reservation/', final.views.reservation, name='reservation'),
    path('register/', final.views.register, name="register"),
    path('admin/', admin.site.urls),
    path('restaurant/<int:id>/', final.views.restaurant_detail, name='restaurant_detail'),
    # path('send-email', final.views.email)
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
