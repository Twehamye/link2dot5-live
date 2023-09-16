import django_filters
from django_filters import DateFilter, CharFilter

from .models import *

class DepositFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name="date_created", lookup_expr='gte')
    end_date = DateFilter(field_name="date_created", lookup_expr='lte')
    amount = CharFilter(field_name="amount", lookup_expr='icontains')


    class Meta:
        model = Deposit
        fields = '__all__'
        exclude = [ 'member', 'date_created','receipt','amount', 'deposited_by']


class FineFilter(django_filters.FilterSet):
    """start_date = DateFilter(field_name="date_created", lookup_expr='gte')
                end_date = DateFilter(field_name="date_created", lookup_expr='lte')
                amount = CharFilter(field_name="amount", lookup_expr='icontains')
            """

    class Meta:
        model = Fine
        fields = '__all__'
        exclude = [ 'issue_date','clearance_date']



class ExpenseFilter(django_filters.FilterSet):
    start_date = DateFilter(field_name="date_of_expense", lookup_expr='gte')
    end_date = DateFilter(field_name="date_of_expense", lookup_expr='lte')
    amount = CharFilter(field_name="amount", lookup_expr='icontains')


    class Meta:
        model = Expense
        fields = '__all__'
        exclude = [ 'member_responsible', 'date_of_expense','receipt','amount']
