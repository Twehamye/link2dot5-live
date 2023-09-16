from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms
from .models import Member, Relative, ChildrenDetail
from .models import *
from django.forms import ModelForm, widgets, DateTimeField, DateField, DateInput
from bootstrap_datepicker_plus.widgets import DatePickerInput


class MemberForm(ModelForm):
    date_of_birth= forms.DateField(widget=forms.widgets.DateInput(
        attrs={'type': 'date'}))
    class Meta:
        model = Member
        fields = '__all__'

class RelativeForm(ModelForm):
    class Meta:
        model = Relative
        fields = '__all__'

class DepositForm(ModelForm):
    class Meta:
        model = Deposit
        fields = '__all__'
        exclude = ["status"]


class ChildrenDetailForm(forms.ModelForm):
    date_of_birth = forms.DateField(widget=forms.widgets.DateInput(
        attrs={'type': 'date'})
    )
    class Meta:
        model = ChildrenDetail
        fields = '__all__'


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class FineForm(ModelForm):
    issue_date = forms.DateField(widget=forms.widgets.DateInput(
        attrs={'type': 'date'}))
    clearance_date = forms.DateField(widget=forms.widgets.DateInput(
        attrs={'type': 'date'}))
    
    class Meta:
        model = Fine
        fields = '__all__'
        exclude = ["status"]

class FinePaymentForm(forms.ModelForm):
    class Meta:
        model = FinePayment
        fields = ['amount']


class ExpenseForm(ModelForm):
    date_of_expense = forms.DateField(widget=forms.widgets.DateInput(
        attrs={'type': 'date'})
    )
    class Meta:
        model = Expense
        fields = '__all__'

class AssetForm(ModelForm):
    date_of_purchase = forms.DateField(widget=forms.widgets.DateInput(
        attrs={'type': 'date'})
    )
    class Meta:
        model = Asset
        fields = '__all__'

class OtherIncomeForm(ModelForm):
    date_of_income = forms.DateField(widget=forms.widgets.DateInput(
        attrs={'type': 'date'})
    )
    class Meta:
        model = OtherIncome
        fields = '__all__'


