from django import forms
from .models import GilKvar, Flat


class GilKvarForm(forms.ModelForm):
    class Meta:
        model = GilKvar
        fields = ['name', 'city', 'street', 'house', 'housing', 'site', 'email', 'phone']


class FlatForm(forms.ModelForm):

    class Meta:
        model = Flat
        fields = ['gilkvar', 'uid', 'housing', 'section', 'floor', 'num_on_floor', 'area', 'price', 'balcony']

    def __init__(self, *args, **kwargs):
        super(FlatForm, self).__init__(*args, **kwargs)
        self.fields['gilkvar'].widget = forms.widgets.HiddenInput()




