from django import forms
from .models import Wydatek

class WydatekForm(forms.ModelForm):

    wydatek_nazwa = forms.CharField(help_text="Zapisz co kupiłeś")

    class Meta:
        model = Wydatek
        fields = ['wydatek_nazwa','wydatek_kwota','wydatek_rodzaj','wydatek_data']