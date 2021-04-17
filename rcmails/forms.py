from django import forms
from .models import Departement, Cmail 


# we'll use this class to display html5 date input
class DateInput(forms.DateInput):
    input_type = 'date'


class DepartementForm(forms.ModelForm):
    class Meta:
        model = Departement
        fields = ('abbreviation', 'english_name', 'arabic_name', 'location')

class CmailForm(forms.ModelForm):
    class Meta:
        model = Cmail
        fields = ('number', 'title', 'recieving_date', 'source')
        widgets = {'recieving_date': DateInput()}


