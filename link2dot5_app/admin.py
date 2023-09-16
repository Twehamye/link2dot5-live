from django.contrib import admin
from .models import *
# Register your models here.


admin.site.register(Fine)
admin.site.register(Expense)
admin.site.register(Asset)
admin.site.register(OtherIncome)


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
	list_display = ("member_id","full_name","email", "telephone",
					 "date_of_birth","current_address",)


@admin.register(Relative)
class RelativeAdmin(admin.ModelAdmin):
	list_display = ("member","spouse_name","spouse_telephone", "father_name",
					 "father_telephone","mother_name",'mother_telephone', 'number_of_children','next_of_kin_name',
					 'next_of_kin_telephone','next_of_kin_relationship','beneficiary_name',
					 'beneficiary_telephone','beneficiary_relationship')


@admin.register(ChildrenDetail)
class ChildrenDetailAdmin(admin.ModelAdmin):
	list_display = ("member","full_name","sex", "date_of_birth")


@admin.register(Deposit)
class DepositAdmin(admin.ModelAdmin):
	list_display = ('member', 'amount','purpose','status', 'date_created', )