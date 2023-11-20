from django.contrib import admin
from .models import (
    MeasurementDevice,
    Reading,
    NutrientProduct,
    DosingGuide,
    FeedingSchedule,
    Dosing,
    Grow,
    Reservoir,
)

# Register your models here.
admin.site.register(MeasurementDevice)
admin.site.register(Reading)
admin.site.register(NutrientProduct)
admin.site.register(DosingGuide)
admin.site.register(Dosing)
admin.site.register(Grow)
admin.site.register(Reservoir)
admin.site.register(FeedingSchedule)
