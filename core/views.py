from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from .forms import PatientSignUpForm, AppointmentForm, MedicalRecordForm, PrescriptionForm
from django.contrib.auth.decorators import login_required
from .models import Appointment, User, MedicalRecord, Prescription, Billing

class PatientLoginView(LoginView):
    template_name = 'registration/login.html'

    def form_valid(self, form):
        login(self.request, form.get_user())
        if self.request.user.role == 'PATIENT':
            return redirect('patient_dashboard')
        else:
            # If a non-patient tries to log in here, log them out and redirect to home
            return redirect('home') # Or show an error message

class StaffLoginView(LoginView):
    template_name = 'registration/login.html'

    def form_valid(self, form):
        login(self.request, form.get_user())
        if self.request.user.role == 'DOCTOR':
            return redirect('doctor_dashboard')
        elif self.request.user.role == 'ADMIN':
            return redirect('/admin')
        else:
            # If a patient tries to log in here, log them out and redirect to home
            return redirect('home') # Or show an error message

def home(request):
    return render(request, 'home.html')

def patient_registration(request):
    if request.method == 'POST':
        form = PatientSignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('patient_dashboard')
    else:
        form = PatientSignUpForm()
    return render(request, 'registration/patient_signup.html', {'form': form})

@login_required
def patient_dashboard(request):
    appointments = Appointment.objects.filter(patient=request.user)
    return render(request, 'dashboards/patient_dashboard.html', {'appointments': appointments})

@login_required
def doctor_dashboard(request):
    appointments = Appointment.objects.filter(doctor=request.user)
    return render(request, 'dashboards/doctor_dashboard.html', {'appointments': appointments})

@login_required
def doctor_patient_list(request):
    patients = User.objects.filter(patient_appointments__doctor=request.user).distinct()
    return render(request, 'doctor/patient_list.html', {'patients': patients})

@login_required
def patient_detail(request, patient_id):
    patient = get_object_or_404(User, id=patient_id, role='PATIENT')
    records = MedicalRecord.objects.filter(patient=patient)
    prescriptions = Prescription.objects.filter(patient=patient)
    
    record_form = MedicalRecordForm()
    prescription_form = PrescriptionForm()

    context = {
        'patient': patient,
        'records': records,
        'prescriptions': prescriptions,
        'record_form': record_form,
        'prescription_form': prescription_form,
    }
    return render(request, 'doctor/patient_detail.html', context)

@login_required
def add_medical_record(request, patient_id):
    patient = get_object_or_404(User, id=patient_id, role='PATIENT')
    if request.method == 'POST':
        form = MedicalRecordForm(request.POST)
        if form.is_valid():
            record = form.save(commit=False)
            record.patient = patient
            record.save()
    return redirect('patient_detail', patient_id=patient.id)

@login_required
def add_prescription(request, patient_id):
    patient = get_object_or_404(User, id=patient_id, role='PATIENT')
    if request.method == 'POST':
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            prescription = form.save(commit=False)
            prescription.patient = patient
            prescription.doctor = request.user
            prescription.save()
    return redirect('patient_detail', patient_id=patient.id)

@login_required
def book_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.patient = request.user
            appointment.save()
            return redirect('patient_dashboard')
    else:
        form = AppointmentForm()
    return render(request, 'appointments/book_appointment.html', {'form': form})

@login_required
def appointment_list(request):
    appointments = Appointment.objects.filter(patient=request.user)
    return render(request, 'appointments/appointment_list.html', {'appointments': appointments})

@login_required
def medical_history(request):
    records = MedicalRecord.objects.filter(patient=request.user)
    prescriptions = Prescription.objects.filter(patient=request.user)
    context = {
        'records': records,
        'prescriptions': prescriptions
    }
    return render(request, 'history/medical_history.html', context)

@login_required
def billing_history(request):
    bills = Billing.objects.filter(patient=request.user)
    return render(request, 'history/billing_history.html', {'bills': bills})