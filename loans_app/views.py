from django.shortcuts import render, redirect
from .models import Loan, Installment
from datetime import datetime
from datetime import timedelta
from datetime import date
from dateutil.relativedelta import relativedelta
from django.utils import timezone
from django.db.models.expressions import RawSQL
from django.db import connection
from django.conf import settings
from django.http import JsonResponse
from django.db.models import Sum

def create_loan(request):
    if request.method == 'POST':
        borrower_id = (request.POST['borrower_id'])
        borrower_name = (request.POST['borrower_name'])
        telephone = int(request.POST['telephone'])
        loan_type = (request.POST['loan_type'])
        amount = float(request.POST['amount'])
        interest_rate = float(request.POST['interest_rate'])
        duration_months = int(request.POST['duration_months'])
        collateral_name = (request.POST['collateral_name'])
        guarantor1 = (request.POST['guarantor1'])
        guarantor2 = (request.POST['guarantor2'])
        start_date = (request.POST['start_date'])
        loan = Loan.objects.create(borrower_id=borrower_id, borrower_name=borrower_name, telephone=telephone, loan_type=loan_type,
                                amount=amount, interest_rate=interest_rate, duration_months=duration_months, 
                                collateral_name=collateral_name, guarantor1=guarantor1, guarantor2=guarantor2, start_date=start_date)


        installment_amount = (amount + (amount * interest_rate / 100)) / duration_months
        monthly_interest = (amount * interest_rate / 100)/ duration_months

        for _ in range(0, (duration_months)):
            pay_date = start_date #+ timedelta(days=10)
            due_date = datetime.now() # Assuming each installment is due after 30 days
            Installment.objects.create(loan=loan, due_date=due_date, amount_due=installment_amount, interest=monthly_interest)
            current_date = due_date

        return redirect('loan_list')  # Redirect to a page showing list of loans

    return render(request, 'create_loan.html')  # Create a template for loan creation form

def pay_installment(request, installment_id):
    installment = Installment.objects.get(id=installment_id)
    if request.method == 'POST':
        installment.is_paid = True
        installment.payment_date = timezone.now()
        installment.save()
        return redirect('installment_list')  # Redirect to a page showing list of installments

    return render(request, 'pay_installment.html', {'installment': installment})

def installment_list(request):
    loans = Loan.objects.filter(status='approved')
    #install_approved = loan.installment_set.all()
    installments = Installment.objects.all()
    context = {
                'loans': loans,
                'installments': installments,
                #'install_approved':install_approved,
                #'total_loan':total_loan,
    }
    return render(request, 'installment_list.html', context)

def loan_list(request):
    loans = Loan.objects.all().order_by('-id')
    #total_loan = (loans.amount + (loans.amount * loans.interest_rate / 100))

    context = {
                'loans': loans,
                #'total_loan':total_loan,
    }
    return render(request, 'loan_list.html', context)

def payments_list(request):
    payments = Installment.objects.filter(is_paid=True).order_by('-payment_date')
    total_payments = payments.aggregate(Sum('amount_due'))['amount_due__sum'] or 0
    unpaid_loan = Installment.objects.filter(is_paid=False).aggregate(Sum('amount_due'))['amount_due__sum'] or 0
    earned_interest = Installment.objects.filter(is_paid=False).aggregate(Sum('interest'))['interest__sum'] or 0
    context = {
                'payments': payments,
                'total_payments':total_payments,
                'unpaid_loan':unpaid_loan,
                'earned_interest':earned_interest,
                
    }
    return render(request, 'all_payments.html', context)

def report(request, id):
    loan = Loan.objects.get(id=id)
    installment = loan.installment_set.all()
    ind_loan1 = loan.installment_set.filter(is_paid=True).aggregate(Sum('amount_due'))['amount_due__sum'] or 0
    monthly_interest = loan.installment_set.filter(is_paid=True).aggregate(Sum('interest'))['interest__sum'] or 0
    ind_loan = loan.total - ind_loan1
    total_loan = loan.total
    interest = total_loan - loan.amount
    context = {
            'loan': loan,
            'installment':installment,
            'ind_loan':ind_loan,
            'ind_loan1':ind_loan1,
            'total_loan':total_loan,
            'interest':interest,
            'monthly_interest':monthly_interest,

    }
    return render(request, 'loan_report.html', context)    

def home_loan(request):
    loan = Loan.objects.all()
    loans_pending = Loan.objects.filter(is_reviewed=False).aggregate(Sum('amount'))['amount__sum'] or 0
    loans_reviewed = Loan.objects.filter(is_reviewed=True).aggregate(Sum('amount'))['amount__sum'] or 0
    loans_approved = Loan.objects.filter(status="approved").aggregate(Sum('amount'))['amount__sum'] or 0
    loans_rejected = Loan.objects.filter(status="rejected").aggregate(Sum('amount'))['amount__sum'] or 0
    loans_rejected_number = Loan.objects.filter(status="rejected").count()
    loans_unreviewed_number = Loan.objects.filter(is_reviewed=False).count()
    loans_approved_number = Loan.objects.filter(status="approved").count()
    installment = Installment.objects.all()
    interest_amount =installment.filter(is_paid=True).aggregate(Sum('amount_due'))['amount_due__sum'] or 0

    context = {
            'loans_pending':loans_pending,
            'loans_reviewed':loans_reviewed,
            'loans_approved':loans_approved,
            'loans_rejected':loans_rejected,
            'loans_rejected_number':loans_rejected_number,
            'loans_unreviewed_number':loans_unreviewed_number,
            'loans_approved_number':loans_approved_number,
            'installment':installment,
            'interest_amount':interest_amount,

    }

    return render(request, 'home_loan.html', context)
