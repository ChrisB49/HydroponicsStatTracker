from django.contrib import admin
from .models import MeasurementDevice, PHReading, ECReading

# Register your models here.
admin.site.register(MeasurementDevice)
admin.site.register(PHReading)
admin.site.register(ECReading)
