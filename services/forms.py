from django import forms
from .models import Service

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ['title', 'description', 'price', 'category']


class ServiceSearchForm(forms.Form):
    title = forms.CharField(max_length=200, required=False, label='Title')
    category = forms.ChoiceField(choices=[('', 'All Categories')] + Service.CATEGORY_CHOICES, required=False)
    min_price = forms.DecimalField(max_digits=10, decimal_places=2, required=False, label='Min Price')
    max_price = forms.DecimalField(max_digits=10, decimal_places=2, required=False, label='Max Price')
