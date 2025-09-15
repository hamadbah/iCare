from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

# Create your models here.
user_role = [
    ('clerk', 'Clerk'),
    ('doctor', 'Doctor'),
    ('nurse', 'Nurse')
]

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    role = models.CharField(max_length=15, choices=user_role, blank=True, null=True)
    fullname = models.CharField(max_length=75, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.fullname} ({self.user.username})"
    
gender_choices = [('male', 'Male'), ('female', 'Female')]

class Patient(models.Model):
    patient_name = models.CharField(max_length=100)
    national_id = models.CharField(max_length=20, unique=True)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=gender_choices)
    phone = models.CharField(max_length=20)
    address = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='main_app/static/uploads', default='')
    
    def __str__(self):
        return f"{self.patient_name}"
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'patient_id': self.id})
    
appointment_status_choices = [
    ('Scheduled', 'Scheduled'), 
    ('Cancelled', 'Cancelled'),
]

infection_type_choices = [
    ('hepatitis_b', 'Hepatitis B'),
    ('hepatitis_c', 'Hepatitis C'),
    ('hiv', 'HIV'),
    ('tuberculosis', 'Tuberculosis'),
    ('covid19', 'COVID-19'),
]

alert_status_choices = [
    ('active', 'Active'),
    ('resolved', 'Resolved'),
]

class Alert(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    infection_type = models.CharField(max_length=50, choices=infection_type_choices)
    alert_status = models.CharField(max_length=20, choices=alert_status_choices)
    alert_note = models.TextField()

    def __str__(self):
        return f"{self.infection_type} alert for {self.patient.patient_name}"

    def get_absolute_url(self):
        return reverse('alert_detail', kwargs={'alert_id': self.id})
    
allergy_severity_choices = [
    ('mild', 'Mild'),
    ('moderate', 'Moderate'),
    ('severe', 'Severe'),
]

allergy_status_choices = [
    ('active', 'Active'),
    ('resolved', 'Resolved'),
]

class Allergy(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    allergy_name = models.CharField(max_length=100)
    severity = models.CharField(max_length=20, choices=allergy_severity_choices)
    allergy_status = models.CharField(max_length=20, choices=allergy_status_choices)

    def __str__(self):
        return f"{self.allerg_name} ({self.severity}) - {self.patient.patient_name}"

    def get_absolute_url(self):
        return reverse('allergy_detail', kwargs={'allergy_id': self.id})

visit_type_choices = [
    ('first', 'First Visit'),
    ('follow_up', 'Follow Up'),
]

class Appointment(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    doctor_code = models.ForeignKey(Profile, limit_choices_to={'role': 'doctor'}, on_delete=models.SET_NULL, null=True, related_name='appointments')
    visit_type = models.CharField(max_length=20, choices=visit_type_choices)
    status = models.CharField(max_length=20, choices=appointment_status_choices)

    def __str__(self):
        return f"{self.patient.patient_name} - {self.appointment_date} {self.appointment_time}"

    def get_absolute_url(self):
        return reverse('appointment_detail', kwargs={'appointment_id': self.id})
    
class VitalSign(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    temperature = models.DecimalField(max_digits=4, decimal_places=1, null=True, blank=True)
    heart_rate = models.PositiveIntegerField(null=True, blank=True)
    respiratory_rate = models.PositiveIntegerField(null=True, blank=True)
    systolic_bp = models.PositiveIntegerField(null=True, blank=True)
    diastolic_bp = models.PositiveIntegerField(null=True, blank=True)
    oxygen_saturation = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True)

    def __str__(self):
        return f"Vitals for {self.appointment.patient.patient_name} (Appt {self.appointment.id})"
    
class DoctorNote(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    subjective = models.TextField()
    objective = models.TextField()
    plan = models.TextField()

    def __str__(self):
        return f"{self.subjective} for {self.appointment.patient.patient_name}"
    
class Prescription(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    drug_name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=50)
    frequency = models.CharField(max_length=50)
    duration = models.CharField(max_length=50)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.drug_name} for {self.appointment.patient.patient_name} (Appt {self.appointment.id})"
    
lab_status_choices = [
    ('pending', 'Pending'),
    ('completed', 'Completed')
]

class Lab(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    test_name = models.CharField(max_length=100)
    test_date = models.DateField()
    result = models.TextField(blank=True, null=True)
    lab_status = models.CharField(max_length=20, choices=lab_status_choices, default='pending')

    def __str__(self):
        return f"{self.test_name} for {self.appointment.patient.patient_name} ({self.status})"

    def get_absolute_url(self):
        return reverse('lab_detail', kwargs={'lab_id': self.id})
    
status_choices = [
        ('initial', 'Initial'),
        ('confirm', 'Confirm')
    ]

class Diagnosis(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    diagnosis_name = models.CharField(max_length=200)
    diagnosis_date = models.DateField()
    diagnosis_status = models.CharField(max_length=20, choices=status_choices)

    def __str__(self):
        return f"{self.diagnosis_name} for {self.appointment.patient.patient_name} ({self.diagnosis_status})"

    def get_absolute_url(self):
        return reverse("diagnosis_detail", kwargs={"diagnosis_id": self.id})
    
class NurseNote(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    note_time = models.TimeField()
    note = models.TextField()

    def __str__(self):
        return f"{self.note} for {self.appointment.patient.patient_name}"

    def get_absolute_url(self):
        return reverse("nurse_note_detail", kwargs={"nursenote_id": self.id})


order_priority_choices = [
    ('routine', 'Routine'), 
    ('urgent', 'Urgent'), 
    ('stat', 'Stat')
    ]

order_status_choices = [
    ('pending', 'Pending'), 
    ('in_progress', 'In Progress'), 
    ('completed', 'Completed')
    ]

class DoctorOrder(models.Model):
    appointment = models.ForeignKey(Appointment, on_delete=models.CASCADE)
    order_date = models.DateField()
    order_type = models.CharField(max_length=100)
    instructions = models.TextField()
    priority = models.CharField(max_length=20,choices=order_priority_choices)
    order_status = models.CharField(max_length=20,choices=order_status_choices)

    def __str__(self):
        return f"Order: {self.order_type} for {self.appointment.patient.patient_name} ({self.order_status})"

    def get_absolute_url(self):
        return reverse("doctor_order_detail", kwargs={"order_id": self.id})
