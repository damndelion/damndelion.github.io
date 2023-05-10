from django import forms
from .models import Publisher, Review, Book



class PublisherForm(forms.ModelForm):
    class Meta:
        app_label = "final"
        model = Publisher
        fields = "__all__"


class SearchForm(forms.Form):
    search = forms.CharField(required=False, min_length=3)
    search_in = forms.ChoiceField(required=False, choices=(("title", "Title"), ("contributer", "Contributer")))


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        exclude = ["date_edited", "book"]

    rating = forms.IntegerField(min_value=0, max_value=10)


class BookMediaForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ["cover", "sample"]



