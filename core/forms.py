from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import User, PatientProfile, Appointment, DoctorProfile, MedicalRecord, Prescription

class PatientSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'PATIENT'
        if commit:
            user.save()
            PatientProfile.objects.create(user=user)
        return user

class AppointmentForm(forms.ModelForm):
    doctor = forms.ModelChoiceField(queryset=User.objects.filter(role='DOCTOR'))
    appointment_date = forms.DateTimeField(
        widget=forms.DateTimeInput(
            attrs={'class': 'form-control datepicker', 'placeholder': 'Select a date and time'}
        )
    )

    class Meta:
        model = Appointment
        fields = ['doctor', 'appointment_date', 'reason']

class MedicalRecordForm(forms.ModelForm):
    class Meta:
        model = MedicalRecord
        fields = ['diagnoses', 'allergies', 'treatment_history']
        widgets = {
            'diagnoses': forms.Textarea(attrs={'rows': 3}),
            'allergies': forms.Textarea(attrs={'rows': 3}),
            'treatment_history': forms.Textarea(attrs={'rows': 3}),
        }

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['medication', 'dosage', 'instructions']
        widgets = {
            'instructions': forms.Textarea(attrs={'rows': 3}),
        }