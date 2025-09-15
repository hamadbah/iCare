from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User
from .models import Profile, Appointment, VitalSign, DoctorNote, Prescription, Lab, Diagnosis, NurseNote, DoctorOrder, Alert

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
        
class NurseNoteForm(ModelForm):
    class Meta:
        model = NurseNote
        fields = ['note_time', 'note']
        widgets = {
            'note_time': forms.TimeInput(
                format='%H:%M',
            ),
        }

class PrescriptionForm(ModelForm):
    class Meta:
        model = Prescription
        fields = ['drug_name', 'dosage','frequency','duration','notes']
        
class LabForm(ModelForm):
    class Meta:
        model = Lab
        fields = ['test_name', 'test_date','result','lab_status']

class DoctorOrderForm(ModelForm):
    class Meta:
        model = DoctorOrder
        fields = ['order_date', 'order_type','instructions','priority','order_status']

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
        
class AlertForm(forms.ModelForm):
    class Meta:
        model = Alert
        fields = ['infection_type', 'alert_status','alert_note']