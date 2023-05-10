from django.contrib import admin
from .models import Publisher, Contributor, Book, BookContributor, Review, Reservation



class ContributorAdmin(admin.ModelAdmin):
    list_display = ('last_names', 'first_names')
    search_fields = ('last_names__startswith', 'first_names')
    list_filter = ('last_names',)

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Date')


class BookAdmin(admin.ModelAdmin):
    search_fields = ('title', 'isbn', 'publisher__name__startswith')
    date_hierarchy = 'publication_date'
    list_display = ('title', 'isbn')
    list_filter = ('publisher', 'publication_date')
    model = Book
    list_display = ('title', 'isbn',\
                      'get_publisher',\
                      'publication_date')
    search_fields = ['title', 'publisher__name']
    def get_publisher(self, obj):
      return obj.publisher.name

# Register your models here.
admin.site.register(Publisher)
admin.site.register(Reservation, ReservationAdmin)
admin.site.register(Contributor, ContributorAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(BookContributor)
admin.site.register(Review)
ContributorAdmin