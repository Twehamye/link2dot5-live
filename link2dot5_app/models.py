from django.db import models
import datetime
from datetime import date  
from django.core.validators import MinValueValidator
from django.core.validators import MaxValueValidator
from auditlog.registry import auditlog

class Member(models.Model):
    sex_choices = (("Male","male"), ("Female","Female"))
    status_choices = (("Married","Married"),("Single","Single"),
                        ("Windowed","Windowed"),("Divorsed","Divorsed"))
    
    member_id =models.CharField(max_length=10, primary_key=True )
    full_name = models.CharField(max_length=200, null=False)
    nin = models.CharField(max_length=100)
    occupation=models.CharField(max_length=500)
    sex = models.CharField(max_length=10,choices = sex_choices)
    marital_status = models.CharField(max_length=30, choices=status_choices)
    email = models.EmailField(max_length=100)
    telephone = models.PositiveIntegerField()
    date_of_birth = models.DateField(validators=[MaxValueValidator(datetime.date.today)])
    current_address = models.CharField(max_length=300)
    home_address = models.CharField(max_length=300)
    Registered_date = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):

        return self.member_id + " " +self.full_name


class Relative(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    spouse_name = models.CharField(max_length=200, null=False)
    spouse_telephone = models.PositiveIntegerField()
    father_name = models.CharField(max_length=200, null=False)
    father_telephone = models.PositiveIntegerField()
    mother_name = models.CharField(max_length=200, null=False)
    mother_telephone = models.PositiveIntegerField()
    number_of_children = models.PositiveIntegerField()
    next_of_kin_name = models.CharField(max_length=200, null=False)
    next_of_kin_telephone = models.IntegerField()
    next_of_kin_relationship = models.CharField(max_length=200, null=False)
    beneficiary_name = models.CharField(max_length=200, null=False)
    beneficiary_telephone = models.PositiveIntegerField()
    beneficiary_relationship = models.CharField(max_length=200, null=False)


class ChildrenDetail(models.Model):
    sex_choices = (("Male","Male"), ("Female","Female"))

    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200, null=False)
    sex = models.CharField(max_length=300, choices = sex_choices)
    date_of_birth = models.DateField(validators=[MaxValueValidator(datetime.date.today)])
    Registered_date = models.DateTimeField(auto_now_add=True)


class Deposit(models.Model):
    status_choices =(("pending","pending"),("Approved","Approved"),
                        ("Rejeted","Rejected"))
    purpose_choices = (("January","January"),("February","February"),("March","March"),
    				("April","April"),("May","May"),("June","June"),("July","July"),
    				("August","August"),("September","September"),("October","October"),
    				("November","November"),("December","December"))

    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    purpose = models.CharField(max_length=200, null=False, choices = purpose_choices)
    year = models.PositiveIntegerField()
    deposited_by = models.CharField(max_length=50,null=False)
    transaction_id = models.CharField(max_length=50,null=False)
    status = models.CharField(max_length=200, null=False, choices = status_choices, default="pending")
    date_created = models.DateTimeField(auto_now_add=True)
    receipt = models.ImageField(upload_to='deposits/%Y/%m/%d',blank=True)

    def __str__(self):

        return self.member_id + " " + self.purpose


class Expense(models.Model):
    purpose = models.CharField(max_length=300, null=False)
    amount = models.PositiveIntegerField()
    date_of_expense = models.DateTimeField()
    member_responsible = models.ForeignKey(Member, on_delete=models.SET_DEFAULT, default=None, null=False)
    receipt = models.ImageField(upload_to='deposits/%Y/%m/%d',blank=True)

    def __str__(self):
        return self.purpose +"  "+ str(self.amount)

class Asset(models.Model):
    asset_name = models.CharField(max_length=300, null=False)
    asset_desc = models.TextField()
    purchase_amount = models.PositiveIntegerField()
    date_of_purchase = models.DateTimeField()
    document = models.ImageField(upload_to='deposits/%Y/%m/%d',blank=True)

    def __str__(self):
        return self.asset_name +"  "+ str(self.purchase_amount)


class Fine(models.Model):
    status_choices = (("paid","paid"), ("unpaid","unpaid"))

    member = models.ForeignKey(Member, on_delete=models.CASCADE)
    reason = models.CharField(max_length=200, null=False)
    amount = models.PositiveIntegerField()
    status = models.CharField(max_length=300, choices = status_choices, default="unpaid")
    issue_date = models.DateField()
    clearance_date = models.DateField(validators=[MinValueValidator(datetime.date.today)])
    
    def __str__(self):
        return self.member.member_id +"  "+ self.reason +" "+ self.status   

class FinePayment(models.Model):
    fine = models.ForeignKey(Fine, on_delete=models.CASCADE)
    amount = models.PositiveIntegerField()
    payment_date = models.DateTimeField(auto_now_add=True)

class OtherIncome(models.Model):
    source = models.CharField(max_length=300, null=False)
    amount = models.PositiveIntegerField()
    date_of_income = models.DateTimeField()
    receipt = models.ImageField(upload_to='income/%Y/%m/%d',blank=True)



auditlog.register(Member)
auditlog.register(Deposit)