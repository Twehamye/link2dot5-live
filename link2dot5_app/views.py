from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.template import loader
from django.db.models import Sum, Avg, Count
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import *
from django.contrib.auth import authenticate, login, logout
from .forms import *
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.db.models import Q
from .forms import CreateUserForm
from .filters import DepositFilter,FineFilter,ExpenseFilter
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.forms import inlineformset_factory
from django.db import connection
#from django.db.models import RawSQL
from django.db.models.expressions import RawSQL
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import csv

def deposit_csv(request):
    response =HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachment; filename = deposits.csv'

    #create a writer
    writer = csv.writer(response)

    #Designate the Model
    deposits =Deposit.objects.all().order_by("-date_created")
    #Add column heading
    writer.writerow(['member','amount','purpose','year','depositor','status','date_created'])

    for deposit in deposits:
        writer.writerow([deposit.member,deposit.amount,deposit.purpose, deposit.year, deposit.deposited_by,deposit.status,deposit.date_created]) 

    return response

def report(request):
    all_members = Member.objects.all()
    all_deposits = Deposit.objects.all()
    all_children = ChildrenDetail.objects.all()
    number_of_members = Member.objects.all().aggregate(Count('member_id'))
    sum_all = Deposit.objects.all().aggregate(Sum('amount'))
    pending_deposits = Deposit.objects.filter(status="pending").aggregate(models.Sum('amount'))['amount__sum'] or 0
    approved_deposits = Deposit.objects.filter(status="Approved").aggregate(models.Sum('amount'))['amount__sum'] or 0
    rejected_deposits = Deposit.objects.filter(status="rejected").aggregate(models.Sum('amount'))['amount__sum'] or 0

    cursor = connection.cursor()
    cursor.execute('select sum(amount) from link2dot5_app_fine union select sum(amount) from link2dot5_app_deposit')
    f = cursor.fetchone()

    fines_uncleared = Fine.objects.filter(status="unpaid").aggregate(models.Sum('amount'))['amount__sum'] or 0
    fines_cleared = FinePayment.objects.aggregate(models.Sum('amount'))['amount__sum'] or 0
    fines_total = fines_cleared + fines_uncleared
    savings_total = approved_deposits
    total_expenses = Expense.objects.aggregate(models.Sum('amount'))['amount__sum'] or 0
    asset_cost = Asset.objects.aggregate(models.Sum('purchase_amount'))['purchase_amount__sum'] or 0
    otherincome = OtherIncome.objects.aggregate(models.Sum('amount'))['amount__sum'] or 0

    grand_total = fines_cleared + savings_total + otherincome - total_expenses - asset_cost

    context = {
                'all': all_members,
                'all_d':all_deposits,
                'all_c':all_children, 
                'total':sum_all, 
                'f':f,
                'grand_total':grand_total,
                'fines_total':fines_total,
                'savings_total':savings_total,
                'pending_deposits': pending_deposits,
                'approved_deposits':approved_deposits,
                'rejected_deposits':rejected_deposits,
                'fines_uncleared': fines_uncleared,
                'fines_cleared':fines_cleared,
                'total_expenses':total_expenses,
                'asset_cost':asset_cost,
                }

    return render(request,'members/report.html', context)


def member(request, member_id):
    member = Member.objects.get(member_id=member_id)
    deposits = member.deposit_set.all().order_by('-date_created')
    children = member.childrendetail_set.all()
    relative = member.relative_set.all()
    deposit_count = deposits.count()
    ind_savings = member.deposit_set.filter(status='Approved').aggregate(models.Sum('amount'))['amount__sum'] or 0
    ind_fine = member.fine_set.filter(status='unpaid').aggregate(models.Sum('amount'))['amount__sum'] or 0
    myFilter = DepositFilter(request.GET, queryset=deposits)
    deposits = myFilter.qs
    
    context = {
    'member': member, 
    'deposits': deposits, 
    'deposit_count': deposit_count,
     'myFilter': myFilter,
     'ind_savings': ind_savings,
     'ind_fine': ind_fine,
     'children':children,
     'relative': relative,
    }

    return render(request, 'members/member.html', context)

def relative(request, id):
    relative = Relative.objects.get(id=id)
    
    children = relative.member.childrendetail_set.all()
    #info = relative.rel_set.all()

    context = {
    'relative': relative, 
    'children':children
    
    }

    return render(request, 'members/relative.html', context)



def home(request): 
    total_members = Member.objects.all().count() #aggregate(Count('member_id'))
    pending_deposits = Deposit.objects.filter(status='pending').count()
    approved_deposits = Deposit.objects.filter(status='Approved').count()
    unpaid_fines = Fine.objects.filter(status='unpaid').count()
    paid_fines = Fine.objects.filter(status='paid').count()
    total_savings = Deposit.objects.filter(status="pending").aggregate(models.Sum('amount'))['amount__sum'] or 0
    mymembers = Member.objects.all()
    deposits = Deposit.objects.all().order_by("-date_created")
    total_members = Member.objects.all().count()
    myFilter = DepositFilter(request.GET, queryset=deposits)
    deposits = myFilter.qs
    
    expenses_total = Expense.objects.all().aggregate(models.Sum('amount'))['amount__sum'] or 0
    
    fines_total = FinePayment.objects.all().aggregate(models.Sum('amount'))['amount__sum'] or 0
    savings_total = Deposit.objects.filter(status='approved').aggregate(models.Sum('amount'))['amount__sum'] or 0
    asset_cost = Asset.objects.aggregate(models.Sum('purchase_amount'))['purchase_amount__sum'] or 0
    otherincome = OtherIncome.objects.aggregate(models.Sum('amount'))['amount__sum'] or 0

    current_balance = savings_total + fines_total + otherincome - expenses_total - asset_cost

    grand_total = fines_total + savings_total + expenses_total + asset_cost + otherincome

    context = {
        'pending_deposits': pending_deposits,
        'approved_deposits': approved_deposits,
        'mymembers': mymembers,
        'total_members': total_members,
        'unpaid_fines':unpaid_fines,
        'paid_fines':paid_fines,
        'total_savings': total_savings,
        'deposits': deposits,
        'myFilter': myFilter,
        'fines_total': fines_total,
        'current_balance': current_balance,
        'savings_total': savings_total,
        'expenses_total':expenses_total,
        'grand_total': grand_total,
        'asset_cost': asset_cost,
        'otherincome':otherincome,
        
      }

    return render(request,'members/dashboard.html', context)

def index(request):
    search_member = request.GET.get('search')
    if search_member:    
        members = Member.objects.filter(Q(member_id__icontains=search_member) |
                             Q(full_name__icontains=search_member) |
                             Q(sex__icontains=search_member))
    else:
        # If not searched, return default members
        members = Member.objects.all().order_by("-Registered_date")    
    

    return render(request, 'members/index.html', {'members': members})


def signupPage(request):
    form = CreateUserForm
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')

            group = Group.objects.get(name='member')
            user.groups.add(group)

            messages.success(request, "Account was created for" + username)
            return redirect('login')

    context = {'form': form}
    return render(request, 'members/signup.html', context)

def register(request):
    if request.method == "POST":
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            name = form.cleaned_data.get('full_name')
            messages.success(request, f'Hi {name}, your account was created successfully')
            return redirect('home')
    else:
        form = MemberForm()

    return render(request, 'members/register.html', {'form': form})

#@unauthenticated_user
def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else: 
            messages.info(request, "Username or password is incorrect")

    context = {}
    return render(request, 'members/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('login')

def userPage(request):
    context = {}
    return render(request, 'members/user.html', context)


def createMember(request):
    form = MemberForm()
    if request.method == "POST":
        form = MemberForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")

    context = {'form': form}
    return render(request, 'members/member_form.html', context)


def updateMember(request, member_id):

    member = Member.objects.get(member_id=member_id)
    form = MemberForm(instance=member)

    if request.method == "POST":
        form = MemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            return redirect('/')
    context = {'form': form}
    return render(request, 'members/member_form.html', context) 
    

def deleteMember(request, member_id):
    member = Member.objects.get(member_id=member_id)
    if request.method == "POST":
        member.delete()
        return redirect('home')

    context = {'item': member } 

    return render(request, 'members/delete_member.html', context) 

def updateChild(request, id):

    child = ChildrenDetail.objects.get(id=id)
    form = ChildrenDetailForm(instance=child)

    if request.method == "POST":
        form = ChildrenDetailForm(request.POST, instance=child)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'members/add_child_details.html', context)

def deleteChild(request, id):
    child = ChildrenDetail.objects.get(id=id)
    if request.method == "POST":
        child.delete()
        return redirect('all_children')

    context = {'child': child } 

    return render(request, 'members/delete_child.html', context)


def updateRelative(request, id):
    relative = Relative.objects.get(id=id)
    form = RelativeForm(instance=relative)

    if request.method == "POST":
        form = RelativeForm(request.POST, instance=relative)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'members/add_relative_detail.html', context)  

def deleteRelative(request, id):
    relative = Relative.objects.get(id=id)
    if request.method == "POST":
        relative.delete()
        return redirect('all_relative')
    context = {'relative': relative } 
    return render(request, 'members/delete_relative.html', context)

def deposit_create(request):
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = DepositForm()
    return render(request, 'members/deposit_create.html', {'form': form})

def deposit_success(request):
    return redirect('index')

def updateDeposit(request, id):
    deposit = Deposit.objects.get(id=id)
    form = DepositForm(instance=deposit)

    if request.method == "POST":
        form = DepositForm(request.POST, instance=deposit)
        if form.is_valid():
            form.save()
            return redirect('all_deposit')

    context = {'form': form } 

    return render(request, 'members/deposit_create.html', context)         

def deleteDeposit(request, id):
    deposit = Deposit.objects.get(id=id)
    if request.method == "POST":
        deposit.delete()
        return redirect('all_deposit')

    context = {'item': deposit } 

    return render(request, 'members/delete_deposit.html', context)

def add_children_detail(request):
    if request.method == "POST":
        form = ChildrenDetailForm(request.POST)
        if form.is_valid():
            form.save()
            name = form.cleaned_data.get('full_name')
            messages.success(request, f'Details for {name}, have been added successfully')
            return redirect('home')
    else:
        form = ChildrenDetailForm()

    return render(request, 'members/add_child_details.html', {'form': form})

def add_relative_detail(request):
    if request.method == "POST":
        form = RelativeForm(request.POST)
        if form.is_valid():
            form.save()
            name = form.cleaned_data.get('member.member_id')
            messages.success(request, f'Details for {name} have been added successfully')
            return redirect('home')
    else:
        form = RelativeForm()

    return render(request, 'members/add_relative_detail.html', {'form': form})

def allDeposit(request):
    search_deposit = request.GET.get('search')
    if search_deposit:

        deposits = Deposit.objects.filter(Q(amount__icontains=search_deposit) |
                             Q(purpose__icontains=search_deposit) |
                             Q(date_created__icontains=search_deposit))
    else:
        # If not searched, return default members
        deposits = Deposit.objects.all().order_by("-date_created") 
        myFilter = DepositFilter(request.GET, queryset=deposits)
        deposits = myFilter.qs   
         
        context = {'deposits': deposits,
                    'myFilter': myFilter
        } #'members': members} 

    return render(request, 'members/all_deposits.html', context )


"""
def createStaff(request):
    form = StaffForm()
    if request.method == "POST":
        form = StaffForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")

    context = {'form': form}
    return render(request, 'members/staff_form.html', context)


def updateStaff(request, staff_id):

    staff = Staff.objects.get(staff_id=staff_id)
    form = StaffForm(instance=staff)

    if request.method == "POST":
        form = StaffForm(request.POST, instance=staff)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form': form}
    return render(request, 'members/staff_form.html', context) 
    

def deleteStaff(request, staff_id):
    staff = Staff.objects.get(staff_id=staff_id)
    if request.method == "POST":
        staff.delete()
        return redirect('home')

    context = {'staff': staff } 

    return render(request, 'members/delete_staff.html', context) """



def updateFine(request, id):
    fine = Fine.objects.get(id=id)
    form = FineForm(instance=fine)

    if request.method == "POST":
        form = FineForm(request.POST, instance=fine)
        if form.is_valid():
            form.save()
            return redirect('all_fine')

    context = {'form': form } 

    return render(request, 'members/fine_create.html', context)         

def deleteFine(request, id):
    fine = Fine.objects.get(id=id)
    if request.method == "POST":
        fine.delete()
        return redirect('all_deposit')

    context = {'fine': fine } 

    return render(request, 'members/delete_fine.html', context)



def createAsset(request):
    if request.method == 'POST':
        form = AssetForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('all_asset')
    else:
        form = AssetForm()
    return render(request, 'members/create_asset.html', {'form': form})


def updateAsset(request, id):
    asset = Asset.objects.get(id=id)
    form = AssetForm(instance=asset)

    if request.method == "POST":
        form = AssetForm(request.POST, instance=asset)
        if form.is_valid():
            form.save()
            return redirect('all_asset')

    context = {'form': form } 

    return render(request, 'members/create_asset.html', context)         

def deleteAsset(request, id):
    asset = Asset.objects.get(id=id)
    if request.method == "POST":
        asset.delete()
        return redirect('all_asset')

    context = {'asset': asset } 

    return render(request, 'members/delete_asset.html', context)   


def createExpense(request):
    if request.method == 'POST':
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('all_expense')
    else:
        form = ExpenseForm()
    return render(request, 'members/create_expense.html', {'form': form})


def updateExpense(request, id):
    expense = Expense.objects.get(id=id)
    form = ExpenseForm(instance=expense)

    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect('all_expense')

    context = {'form': form } 

    return render(request, 'members/create_expense.html', context)         

def deleteExpense(request, id):
    expense = Expense.objects.get(id=id)
    if request.method == "POST":
        expense.delete()
        return redirect('all_expense')

    context = {'expense': expense } 

    return render(request, 'members/delete_expense.html', context) 

def createPayment(request):
    form = PaymentForm()
    if request.method == "POST":
        form = PaymentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")

    context = {'form': form}
    return render(request, 'members/payment_form.html', context)


def fine_create(request):
    if request.method == 'POST':
        form = FineForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('all_fine')
    else:
        form = FineForm()
    return render(request, 'members/fine_create.html', {'form': form})

def fine_detail(request, fine_id):
    fine_application = get_object_or_404(Fine, id=fine_id)
    fines = Fine.objects.all() #.order_by("-date_created")

    context ={
                'fine_application': fine_application,
                'fines' : fines,
    }
    return render(request, 'members/fine_details.html', context)

def make_payment(request, fine_id):
    fine = get_object_or_404(Fine, id=fine_id)
    if request.method == 'POST':
        form = FinePaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.fine = fine
            payment.save()

            # Perform balance reduction or other payment processing logic
            # For simplicity, we'll assume the payment reduces the loan amount
            fine.amount -= payment.amount
            if fine.amount <= 0:
                fine.status = 'paid'
            fine.save()

            return redirect('all_fine')#('loan_application_detail', loan_id=loan.id)
    else:
        form = FinePaymentForm()
    return render(request, 'members/make_payment.html', {'form': form, 'fine': fine})

def allFines(request):
    search_fine = request.GET.get('search')
    if search_fine:

        fines = Fine.objects.filter(Q(member__icontains=search_fine) |
                             Q(reason__icontains=search_fine) |
                             Q(status__icontains=search_fine))
    else:
        # If not searched, return default members
        fines_unpaid = Fine.objects.filter(status="unpaid").order_by("-id")
        fines_cleared = FinePayment.objects.all().order_by("-id")
        fines_number = Fine.objects.all().count()
        fines = Fine.objects.all().order_by("-issue_date") 
        fineFilter = FineFilter(request.GET, queryset=fines)
        fines = fineFilter.qs   
         

    context = {
                'fines_unpaid': fines_unpaid, 
                'fines_number': fines_number,
                'fines_cleared':fines_cleared,
                'fines': fines,
                'fineFilter': fineFilter,
                    
        }  

    return render(request, 'members/all_fines.html', context )


def allExpense(request):
    search_expense = request.GET.get('search')
    if search_expense:

        expense = Expense.objects.filter(Q(member_responsible__icontains=search_expense) |
                             Q(purpose__icontains=search_expense) |
                             Q(date_of_expense__icontains=search_expense))
    else:
        # If not searched, return default members
        expense_list = Expense.objects.all().order_by("-date_of_expense") 
        expenseFilter = ExpenseFilter(request.GET, queryset=expense_list)
        expense_list = expenseFilter.qs   
         

    context = {
                'expense_list': expense_list, 
                #'expense': expense,
                'expenseFilter': expenseFilter,
                    
        }  

    return render(request, 'members/all_expenses.html', context )


def allMember(request):

    member_list = Member.objects.all()  
         

    context = {
                'member_list': member_list, 
                #'expense': expense,
             
        }  

    return render(request, 'members/all_members.html', context )

def allStaff(request):

    staff_list = Staff.objects.all()  
         

    context = {
                'staff_list': staff_list, 
                #'expense': expense,
                    
        }  

    return render(request, 'members/all_staff.html', context )


def allAsset(request):

    asset_list = Asset.objects.all()  
         

    context = {
                'asset_list': asset_list, 
                #'expense': expense,
                    
        }  

    return render(request, 'members/all_assets.html', context )

def allchildren(request):

    children_list = ChildrenDetail.objects.all()  
         

    context = {
                'children_list': children_list, 
               
        }  

    return render(request, 'members/all_children.html', context )

def allrelative(request):

    relative_list = Relative.objects.all()  
         

    context = {
                'relative_list': relative_list, 
                
                    
        }  

    return render(request, 'members/all_relatives.html', context )


def createOtherIncome(request):
    if request.method == 'POST':
        form = OtherIncomeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('all_otherincome')
    else:
        form = OtherIncomeForm()
    return render(request, 'members/create_otherincome.html', {'form': form})


def updateOtherIncome(request, id):
    asset = OtherIncome.objects.get(id=id)
    form = OtherIncomeForm(instance=asset)

    if request.method == "POST":
        form = OtherIncomeForm(request.POST, instance=asset)
        if form.is_valid():
            form.save()
            return redirect('all_otherincome')

    context = {'form': form } 

    return render(request, 'members/create_otherincome.html', context)         

def deleteOtherIncome(request, id):
    asset = OtherIncome.objects.get(id=id)
    if request.method == "POST":
        asset.delete()
        return redirect('all_otherincome')

    context = {'asset': asset } 

    return render(request, 'members/delete_otherincome.html', context)   

def allOtherIncome(request):

    otherincome_list = OtherIncome.objects.all()  
         

    context = {
                'otherincome_list': otherincome_list, 
                    
        }  

    return render(request, 'members/all_otherincome.html', context )