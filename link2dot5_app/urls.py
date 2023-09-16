from django.urls import path
from link2dot5_app import views
from django.contrib.auth import views as auth_view

urlpatterns = [
    path("", views.home, name='home'),
    path('report/',views.report,name='report'),
    path("index/", views.index, name='index'),
    path('member/<str:member_id>/', views.member, name='member'),
    path('relative/<int:id>/', views.relative, name='relative'),
    path('signup/', views.signupPage, name="signup"),
    path('register/', views.register, name='register'),
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('user/', views.userPage, name="user-page"),
    
    path('create_member/', views.createMember, name="create_member"),
    path('update_member/<str:member_id>/', views.updateMember, name='update_member'),
    path('delete_member/<str:member_id>/', views.deleteMember, name='delete_member'),

    path('deposit_create/', views.deposit_create, name='deposit_create'),
    path('update_deposit/<int:id>/', views.updateDeposit, name='update_deposit'),
    path('delete_deposit/<int:id>/', views.deleteDeposit, name='delete_deposit'),

    path('fine_create/', views.fine_create, name='fine_create'),
    path('update_fine/<int:id>/', views.updateFine, name='update_fine'),
    path('delete_fine/<int:id>/', views.deleteFine, name='delete_fine'),

    path('create_asset/', views.createAsset, name='create_asset'),
    path('update_asset/<int:id>/', views.updateAsset, name='update_asset'),
    path('delete_asset/<int:id>/', views.deleteAsset, name='delete_asset'),

    path('create_otherincome/', views.createOtherIncome, name='create_otherincome'),
    path('update_otherincome/<int:id>/', views.updateOtherIncome, name='update_otherincome'),
    path('delete_otherincome/<int:id>/', views.deleteOtherIncome, name='delete_otherincome'),

    path('create_expense/', views.createExpense, name='create_expense'),
    path('update_expense/<int:id>/', views.updateExpense, name='update_expense'),
    path('delete_expense/<int:id>/', views.deleteExpense, name='delete_expense'),

    path('add_child_detail/', views.add_children_detail, name='add_child_detail'),
    path('add_relative_detail/', views.add_relative_detail, name='add_relative_detail'),
    path('all_deposit/', views.allDeposit, name='all_deposit'),
    path('all_fine/', views.allFines, name='all_fine'),
    path('fine/<int:fine_id>/', views.fine_detail, name='fine_detail'),
    path('fine/<int:fine_id>/make-payment/', views.make_payment, name='make_payment'),

    path('update_child/<int:id>/', views.updateChild, name='update_child'),
    path('delete_child/<int:id>/', views.deleteChild, name='delete_child'),
    path('update_relative/<int:id>/', views.updateRelative, name='update_relative'),
    path('delete_relative/<int:id>/', views.deleteRelative, name='delete_relative'),

    path('all_expense/', views.allExpense, name='all_expense'),
    path('all_member/', views.allMember, name='all_member'),
    path('all_asset/', views.allAsset, name='all_asset'),
    path('all_children/', views.allchildren, name='all_children'),
    path('all_relative/', views.allrelative, name='all_relative'),
    path('all_otherincome/', views.allOtherIncome, name='all_otherincome'),

    path('deposit_csv/', views.deposit_csv, name='deposit_csv'),
    
    
]