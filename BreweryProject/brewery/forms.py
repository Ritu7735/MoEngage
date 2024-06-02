# brewery/forms.py
from django import forms

class BrewerySearchForm(forms.Form):
    city = forms.CharField(max_length=100, required=False)
    state = forms.CharField(max_length=100, required=False)
    # query = forms.CharField(label='Search', max_length=100)
    # search_type = forms.ChoiceField(choices=[
    #     ('by_city', 'City'),
    #     ('by_name', 'Name'),
    #     ('by_type', 'Type')
    # ], label='Search Type')
