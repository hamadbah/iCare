from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from .forms import ProfileForm, AppointmentForm, VitalSignForm, DoctorNoteForm, PrescriptionForm, LabForm, DiagnosisForm, UserUpdateForm, ProfileUpdateForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile, Patient, Appointment, VitalSign, DoctorNote, Prescription, Lab, Diagnosis
from django.contrib.auth.models import User
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.db.models import Q
import requests, re
from django.utils.timezone import now

OLLAMA_URL = "http://localhost:11434/v1/chat/completions"
OLLAMA_MODEL = "deepseek-r1:1.5b"

@login_required
def doctor_chat(request):
    answer = ""
    if request.method == "POST":
        question = request.POST.get("question", "").strip()
        if question:
            payload = {
                "model": OLLAMA_MODEL,
                "messages": [{"role": "user", "content": question}]
            }
            try:
                response = requests.post(OLLAMA_URL, json=payload)
                response.raise_for_status()
                data = response.json()
                raw_answer = data.get("choices", [{}])[0].get("message", {}).get("content", "No answer")
                answer = re.sub(r'<think>.*?</think>', '', raw_answer, flags=re.DOTALL).strip()
            except Exception as e:
                answer = f"Error: {str(e)}"
    return render(request, "chatbot/doctor_chat.html", {"answer": answer})

def home(request):
    return render(request,'home.html')

def about(request):
    return render(request,'about.html')


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            error_message = 'Invalid signup - Please try again later'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)

@login_required
def edit_profile(request):
    profile = request.user.profile
    
    if request.method == "POST":
        form = ProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'main_app/edit_profile.html', {'form': form})

@login_required
def profile_view(request):
    return render(request, 'main_app/profile.html', {'profile': request.user.profile})

@login_required
def patients_index(request):
    query = request.GET.get("q")
    if query:
        patients = Patient.objects.filter(
            Q(national_id__icontains=query) | Q(patient_name__icontains=query)
        )
    else:
        patients = Patient.objects.all()
    return render(request, 'patients/index.html', {'patients': patients, 'query': query})

@login_required
def patient_detail(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
    appointment_form = AppointmentForm()
    return render(request,'patients/detail.html', {'patient': patient, 'appointment_form':appointment_form})

class PatientCreate(LoginRequiredMixin, CreateView):
    model = Patient
    fields = ['patient_name', 'national_id','date_of_birth', 'gender', 'phone','address', 'image']
    
class PatientUpdate(LoginRequiredMixin, UpdateView):
    model = Patient
    fields = ['patient_name','national_id', 'date_of_birth', 'gender', 'phone','address'] 
    
class PatientDelete(LoginRequiredMixin, DeleteView):
    model = Patient
    success_url = '/patients/' 
    
@login_required
def add_appointment(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
    form = AppointmentForm(request.POST)
    if form.is_valid():
        new_appointment = form.save(commit=False)
        new_appointment.patient = patient
        new_appointment.save()
        return redirect('detail', patient_id=patient_id)

    return render(request, 'detail.html', {'appointment_form': form,'patient': patient})

@login_required
def appointment_detail(request, appointment_id):
    vitalsign_form = VitalSignForm()
    doctornote_form = DoctorNoteForm()
    prescription_form = PrescriptionForm()
    lab_form = LabForm()
    diagnosis_form = DiagnosisForm()
    appointment = Appointment.objects.get(id=appointment_id)
    patient = appointment.patient
    return render(request, 'appointment/appointment_detail.html', {
        'appointment': appointment,
        'patient': patient,
        'vitalsign_form': vitalsign_form,
        'doctornote_form': doctornote_form,
        'prescription_form': prescription_form,
        'lab_form': lab_form,
        'diagnosis_form': diagnosis_form
    })
    
class AppointmentDelete(LoginRequiredMixin, DeleteView):
    model = Appointment

    def get_success_url(self):
        return reverse('detail', kwargs={'patient_id': self.object.patient.id})
    
@login_required    
def add_vitals(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    form = VitalSignForm(request.POST)
    if form.is_valid():
        vitals = form.save(commit=False)
        vitals.appointment = appointment
        vitals.save()
    return redirect(f"{reverse('appointment_detail', args=[appointment.id])}#vitals")

class VitalSignDelete(LoginRequiredMixin, DeleteView):
    model = VitalSign

    def get_success_url(self):
        return reverse('appointment_detail', kwargs={'appointment_id': self.object.appointment.id}) + "#vitals"
    
class VitalSignUpdate(LoginRequiredMixin, UpdateView):
    model = VitalSign
    form_class = VitalSignForm
    template_name = 'appointment/vital_update.html'

    def get_success_url(self):
        return reverse('appointment_detail', kwargs={'appointment_id': self.object.appointment.id}) + "#vitals"

@login_required    
def add_notes(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    form = DoctorNoteForm(request.POST)
    if form.is_valid():
        notes = form.save(commit=False)
        notes.appointment = appointment
        notes.save()
    return redirect(f"{reverse('appointment_detail', args=[appointment.id])}#notes")

class DoctorNoteDelete(LoginRequiredMixin, DeleteView):
    model = DoctorNote

    def get_success_url(self):
        return reverse('appointment_detail', kwargs={'appointment_id': self.object.appointment.id}) + "#notes"

class DoctorNoteUpdate(LoginRequiredMixin, UpdateView):
    model = DoctorNote
    form_class = DoctorNoteForm
    template_name = 'appointment/doctornote_update.html'

    def get_success_url(self):
        return reverse('appointment_detail', kwargs={'appointment_id': self.object.appointment.id}) + "#notes"

@login_required    
def add_prescriptions(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    form = PrescriptionForm(request.POST)
    if form.is_valid():
        prescriptions = form.save(commit=False)
        prescriptions.appointment = appointment
        prescriptions.save()
    return redirect(f"{reverse('appointment_detail', args=[appointment.id])}#prescriptions")

class PrescriptionDelete(LoginRequiredMixin, DeleteView):
    model = Prescription

    def get_success_url(self):
        return reverse('appointment_detail', kwargs={'appointment_id': self.object.appointment.id}) + "#prescriptions"

class PrescriptionUpdate(LoginRequiredMixin, UpdateView):
    model = Prescription
    form_class = PrescriptionForm
    template_name = 'appointment/prescription_update.html'

    def get_success_url(self):
        return reverse('appointment_detail', kwargs={'appointment_id': self.object.appointment.id}) + "#prescriptions"

@login_required    
def add_lab(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    form = LabForm(request.POST)
    if form.is_valid():
        labs = form.save(commit=False)
        labs.appointment = appointment
        labs.save()
    return redirect(f"{reverse('appointment_detail', args=[appointment.id])}#labs")

class LabDelete(LoginRequiredMixin, DeleteView):
    model = Lab

    def get_success_url(self):
        return reverse('appointment_detail', kwargs={'appointment_id': self.object.appointment.id}) + "#labs"

class LabUpdate(LoginRequiredMixin, UpdateView):
    model = Lab
    form_class = LabForm
    template_name = 'appointment/lab_update.html'

    def get_success_url(self):
        return reverse('appointment_detail', kwargs={'appointment_id': self.object.appointment.id}) + "#labs"

@login_required    
def add_diagnosis(request, appointment_id):
    appointment = Appointment.objects.get(id=appointment_id)
    form = DiagnosisForm(request.POST)
    if form.is_valid():
        diagnosis = form.save(commit=False)
        diagnosis.appointment = appointment
        diagnosis.save()
    return redirect(f"{reverse('appointment_detail', args=[appointment.id])}#diagnosis")

class DiagnosisDelete(LoginRequiredMixin, DeleteView):
    model = Diagnosis

    def get_success_url(self):
        return reverse('appointment_detail', kwargs={'appointment_id': self.object.appointment.id}) + "#diagnosis"

class DiagnosisUpdate(LoginRequiredMixin, UpdateView):
    model = Diagnosis
    form_class = DiagnosisForm
    template_name = 'appointment/diagnosis_update.html'

    def get_success_url(self):
        return reverse('appointment_detail', kwargs={'appointment_id': self.object.appointment.id}) + "#diagnosis"

@login_required    
def patient_summary(request, patient_id):
    patient = Patient.objects.get(id=patient_id)
    
    appointments = patient.appointment_set.all()
    vitals = VitalSign.objects.filter(appointment__patient=patient)
    notes = DoctorNote.objects.filter(appointment__patient=patient)
    prescriptions = Prescription.objects.filter(appointment__patient=patient)
    labs = Lab.objects.filter(appointment__patient=patient)
    diagnosis = Diagnosis.objects.filter(appointment__patient=patient)

    context = {
        "patient": patient,
        "appointments": appointments,
        "vitals": vitals,
        "notes": notes,
        "prescriptions": prescriptions,
        "labs": labs,
        "diagnosis": diagnosis
    }
    return render(request, "patients/patient_summary.html", context)

@login_required
def user_list(request):
    users = User.objects.exclude(is_superuser=True)
    return render(request, 'users/user_list.html', {'users': users})

@login_required
def update_user(request, user_id):
    user_obj = User.objects.get(id=user_id)
    profile_obj = Profile.objects.get(user=user_obj)
    if request.method == "POST":
        user_form = UserUpdateForm(request.POST)
        profile_form = ProfileUpdateForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user_list')
    else:
        user_form = UserUpdateForm(instance=user_obj)
        profile_form = ProfileUpdateForm(instance=profile_obj)
    return render(request, 'users/update_user.html', {
        'user_form': user_form,
        'profile_form': profile_form,
        'user_obj': user_obj
    })
    
@login_required
def todays_appointments(request):
    today = now().date()
    doctor_profile = request.user.profile
    appointments = Appointment.objects.filter(
        doctor_code = doctor_profile,
        appointment_date = today
    ).select_related('patient')
    return render(request, "appointment/todays_appointments.html",{
        'appointments': appointments,
        'today': today
    })