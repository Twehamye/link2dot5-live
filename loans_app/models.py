from django.db import models
from django.utils.timezone import now
from django.utils import timezone
import datetime
from datetime import date  
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator
from auditlog.registry import auditlog

class Loan(models.Model):
    status_choices=(('under_review',"under_review"),('approved',"approved"),('rejected',"rejected"))
    borrower_id = models.CharField(max_length=100)
    borrower_name = models.CharField(max_length=100)
    telephone =models.PositiveIntegerField()
    loan_type = models.CharField(max_length=50, null=False)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    interest_rate = models.DecimalField(max_digits=5, decimal_places=1)
    duration_months = models.PositiveIntegerField()
    collateral_name= models.CharField(max_length=100, null=False) 
    guarantor1 = models.CharField(max_length=30,null=False)
    guarantor2 = models.CharField(max_length=30,null=False)
    start_date = models.DateField()
    is_reviewed = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=status_choices, default="under_review")

    def __str__(self):
        return str(self.id) +" "+ self.borrower_name +" "+ str(self.amount)

    @property
    def total(self):
        total_loan = (self.amount + (self.amount * self.interest_rate / 100))
        total_loan =round(total_loan,1)
        return total_loan
    @property    
    def day(self):
        date = self.start_date + relativedelta(months=self.duration_months)
        return date
    



class Installment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    due_date = models.DateField()
    amount_due = models.DecimalField(max_digits=10, decimal_places=2)
    interest = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    payment_date = models.DateField(null=True, blank=True)

    @property    
    def pay(self):
        date = self.due_date + relativedelta(months=self.loan.duration_months)
        return date

    @property
    def instal(self):
        monthly_inst = self.loan.amount/self.loan.duration_months
        return monthly_inst

    @property
    def interest_earned(self):
        interest = self.amount_due - (self.loan.amount/self.loan.duration_months)
        interest =round(interest,2)  
        return interest


auditlog.register(Loan)
auditlog.register(Installment)