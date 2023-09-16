from django import forms
from .models import Loan, Installment
from django.forms import ModelForm, widgets, DateTimeField, DateField, DateInput
from bootstrap_datepicker_plus.widgets import DatePickerInput


class LoanForm(ModelForm):
    class Meta:
        model = Loan
        fields = '__all__'
        exclude = ["status", "is_reviewed"]