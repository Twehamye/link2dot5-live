# urls.py

from django.urls import path
from loans_app import views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_loan, name='home_loan'),
    path('create_loan/', views.create_loan, name='create_loan'),
    path('pay_installment/<int:installment_id>/', views.pay_installment, name='pay_installment'),
    path('installment_list/', views.installment_list, name='installment_list'),
    path('loan_list/', views.loan_list, name='loan_list'),
    path('all_payments/', views.payments_list, name='all_payments'),
    path('loan_report/<int:id>/', views.report, name='loan_report'),
]
