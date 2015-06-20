from django import forms
from lembretes.models import Lembrete

__author__ = 'GuiLe Garcia'

class FormLembrete(forms.ModelForm):
    data = forms.DateField(
        widget=forms.DateInput(format='%Y/%m/%d'),
        input_formats=['%Y-%m-%d', '%d/%m/%y']
    )

    class Meta:
        model = Lembrete
        fields = "__all__"
