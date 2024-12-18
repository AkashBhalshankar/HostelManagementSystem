from django.urls import path
from . import views
from .views import registration_form, login_form
urlpatterns=[
    path('',views.index,name='index'),
    path('register/', views.registration_form, name='register'),
    path('login_form/', views.login_form, name='login'),
    path('complaint/', views.complaint_form, name='complaint_form'),
    path('complaint_success/', views.complaint_success, name='complaint_success'),
    path('fee_receipt/', views.fee_receipt_form, name='fee_receipt_form'),
    path('receipt_success/<int:receipt_id>/', views.receipt_success, name='receipt_success'),
    path('generate_receipt_pdf/<int:receipt_id>/', views.generate_receipt_pdf, name='generate_receipt_pdf'),
    path('student_home_page/', views.student_home_page, name='student_home_page'),
    path('logout/', views.logout_view, name='logout'),  # Logout URL
    path('admin_login/', views.admin_login_form, name='admin_login'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('students/', views.view_students, name='view_students'),
    path('complaints/', views.view_complaints, name='view_complaints'),
    path('fee_receipts/', views.view_fee_receipts, name='view_fee_receipts'),
    path('dashboard/', views.dashboard, name='dashheader'),
    
]
