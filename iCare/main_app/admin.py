from django.contrib import admin
from . models import Patient, Appointment, VitalSign, DoctorNote, Prescription, Lab, Diagnosis

admin.site.register(Patient)
admin.site.register(Appointment)
admin.site.register(VitalSign)
admin.site.register(DoctorNote)
admin.site.register(Prescription)
admin.site.register(Lab)
admin.site.register(Diagnosis)