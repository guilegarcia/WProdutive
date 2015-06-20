# -*- encoding: utf-8 -*-
__author__ = 'GuiLe Garcia'
from django import forms


class DiaForm(forms.Form):
    # data = forms.DateField(widget=forms.DateInput(format('%Y/%m/%d'), input_formats=['%Y-%m-%d', '%d/%m/%y']), required=None)
    data = forms.DateField(
        widget=forms.DateInput(format='%Y/%m/%d'),
        input_formats=['%Y-%m-%d', '%d/%m/%y'], required=None)
    ant_prox = forms.CharField(max_length=200, required=None)

class SemanaForm(forms.Form):
    data = forms.DateField(
        widget=forms.DateInput(format='%Y/%m/%d'),
        input_formats=['%Y-%m-%d', '%d/%m/%y'], required=None)
    ant_prox = forms.CharField(max_length=200, required=None)

