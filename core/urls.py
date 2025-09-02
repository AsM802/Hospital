from django.urls import path
from . import views

urlpatterns = [
    # Patient URLs
    path('signup/', views.patient_registration, name='patient_signup'),
    path('dashboard/patient/', views.patient_dashboard, name='patient_dashboard'),
    path('book/', views.book_appointment, name='book_appointment'),
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('history/medical/', views.medical_history, name='medical_history'),
    path('history/billing/', views.billing_history, name='billing_history'),

    # Doctor URLs
    path('dashboard/doctor/', views.doctor_dashboard, name='doctor_dashboard'),
    path('doctor/patients/', views.doctor_patient_list, name='doctor_patient_list'),
    path('doctor/patient/<int:patient_id>/', views.patient_detail, name='patient_detail'),
    path('doctor/patient/<int:patient_id>/add_record/', views.add_medical_record, name='add_medical_record'),
    path('doctor/patient/<int:patient_id>/add_prescription/', views.add_prescription, name='add_prescription'),
]