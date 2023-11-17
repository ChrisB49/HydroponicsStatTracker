from django.db import models


class MeasurementDevice(models.Model):
    class CalibrationFrequencyUnit(models.TextChoices):
        DAYS = "DAYS", "Days"
        WEEKS = "WEEKS", "Weeks"
        MONTHS = "MONTHS", "Months"
        YEARS = "YEARS", "Years"

    brand = models.CharField(max_length=50)
    model = models.CharField(max_length=50)
    serial_number = models.CharField(max_length=50)
    purchase_date = models.DateField()
    calibration_frequency = models.IntegerField(default=3)
    calibration_frequency_unit = models.CharField(
        max_length=50,
        choices=CalibrationFrequencyUnit.choices,
        default=CalibrationFrequencyUnit.MONTHS,
    )


# Create your models here.
class PHReading(models.Model):
    reading = models.DecimalField(decimal_places=3, max_digits=5)
    date = models.DateTimeField(auto_now_add=True)
    device = models.ForeignKey("MeasurementDevice", on_delete=models.PROTECT)


class ECReading(models.Model):
    class ECUnitChoices(models.TextChoices):
        MS_CM = "mS/cm", "Millisiemens per centimeter (mS/cm)"
        US_CM = "µS/cm", "Microsiemens per centimeter (µS/cm)"
        TDS_PPM = "ppm", "Parts per million (ppm)"

    reading = models.DecimalField(max_digits=5, decimal_places=2)
    unit = models.CharField(
        max_length=10,
        choices=ECUnitChoices.choices,
        default=ECUnitChoices.MS_CM,
    )
    date = models.DateTimeField(auto_now_add=True)
    device = models.ForeignKey("MeasurementDevice", on_delete=models.PROTECT)
