from django.contrib import admin
from . models import Patient, Appointment, VitalSign, DoctorNote, Prescription, Lab, Diagnosis, Profile

admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(VitalSign)
admin.site.register(DoctorNote)
admin.site.register(Prescription)
admin.site.register(Lab)
admin.site.register(Diagnosis)
admin.site.register(Profile)