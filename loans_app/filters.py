import django_filters
from django_filters import DateFilter, CharFilter

from .models import *

class LoanApplicationFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name="start_date", lookup_expr='gte')
    end_date = DateFilter(field_name="start_date", lookup_expr='lte')
    amount = CharFilter(field_name="amount", lookup_expr='icontains')


    class Meta:
        model = Loan
        fields = '__all__'
        exclude = ['borrower_id','telephone','interest_rate','duration_months','guarantor1','guarantor2']
        