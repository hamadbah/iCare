from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from .models import Profile, Appointment, VitalSign, DoctorNote, Prescription, Lab, Diagnosis

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['fullname', 'phone','address']

class AppointmentForm(ModelForm):
    doctor_code = forms.ModelChoiceField(
        queryset=Profile.objects.filter(role='doctor'),
        empty_label="-- Select a Doctor --",
        label="Doctor Name",
    )
    class Meta:
        model = Appointment
        fields = ['appointment_date', 'appointment_time','doctor_code','visit_type','status']
        
class VitalSignForm(ModelForm):
    class Meta:
        model = VitalSign
        fields = ['temperature', 'heart_rate','respiratory_rate','systolic_bp','diastolic_bp','oxygen_saturation']
        
class DoctorNoteForm(ModelForm):
    class Meta:
        model = DoctorNote
        fields = ['subjective', 'objective','plan']
        
class PrescriptionForm(ModelForm):
    class Meta:
        model = Prescription
        fields = ['drug_name', 'dosage','frequency','duration','notes']
        
class LabForm(ModelForm):
    class Meta:
        model = Lab
        fields = ['test_name', 'test_date','result','status']

class DiagnosisForm(ModelForm):
    class Meta:
        model = Diagnosis
        fields = ['diagnosis_name', 'diagnosis_date','diagnosis_status']
        
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['fullname', 'phone', 'address', 'role']


class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']