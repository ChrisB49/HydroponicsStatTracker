from django.db import models
from django.utils import timezone


class VolumeMeasurementUnit(models.TextChoices):
    LITER = "L", "Liter"
    MILLILITER = "mL", "Milliliter"
    GALLON = "gal", "Gallon"
    FLUID_OUNCE = "fl oz", "Fluid Ounce"
    PINT = "pt", "Pint"
    QUART = "qt", "Quart"
    CUP = "cup", "Cup"
    TABLESPOON = "tbsp", "Tablespoon"
    TEASPOON = "tsp", "Teaspoon"


class GrowthStage(models.TextChoices):
    CUTTINGS_SEEDLINGS = "Cuttings/Seedlings", "Cuttings/Seedlings"
    VEGETATIVE = "Vegetative", "Vegetative"
    TRANSITIONING = "Transitioning", "Transitioning"
    FLOWERING = "Flowering", "Flowering"
    FRUITING = "Fruiting", "Fruiting"


class NutrientProduct(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name


class DosingGuide(models.Model):
    nutrient_product = models.ForeignKey(
        NutrientProduct, on_delete=models.CASCADE, related_name="dosing_guides"
    )
    stage_of_growth = models.CharField(max_length=50, choices=GrowthStage.choices)
    title = models.CharField(max_length=100)
    dosing_amount = models.DecimalField(max_digits=5, decimal_places=2)
    dosing_amount_unit = models.CharField(
        max_length=10,
        choices=VolumeMeasurementUnit.choices,
        default=VolumeMeasurementUnit.MILLILITER,
    )
    dosing_per_volume = models.DecimalField(max_digits=5, decimal_places=2)
    dosing_volume_unit = models.CharField(
        max_length=10,
        choices=VolumeMeasurementUnit.choices,
        default=VolumeMeasurementUnit.GALLON,
    )

    def __str__(self):
        return f"{self.nutrient_product.name} - {self.stage_of_growth} - {self.title}"


class FeedingSchedule(models.Model):
    grow = models.ForeignKey(
        "Grow", on_delete=models.CASCADE, related_name="feeding_schedules"
    )
    name = models.CharField(
        max_length=100
    )  # e.g., 'Early Vegetative', 'Late Flowering', etc.
    dosing_guides = models.ManyToManyField(
        DosingGuide, related_name="feeding_schedules"
    )
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Feeding Schedule: {self.name} for {self.grow.name}"


class Dosing(models.Model):
    reservoir = models.ForeignKey(
        "Reservoir", on_delete=models.CASCADE, related_name="dosings"
    )
    feeding_schedule = models.ForeignKey(
        "FeedingSchedule",
        on_delete=models.SET_NULL,
        null=True,
        related_name="dosings",
        blank=True,
    )
    date = models.DateTimeField(default=timezone.now)
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = "Dosing"
        verbose_name_plural = "Dosings"

    def __str__(self):
        return f"Dosing for {self.reservoir.name} on {self.date.strftime('%Y-%m-%d')} - Schedule: {self.feeding_schedule.name if self.feeding_schedule else 'N/A'}"


class Grow(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField(default=timezone.now)
    end_date = models.DateField(null=True, blank=True)
    description = models.TextField(blank=True)
    stage = models.CharField(
        max_length=50, choices=GrowthStage.choices, default=GrowthStage.VEGETATIVE
    )

    class Meta:
        verbose_name = "Grow"
        verbose_name_plural = "Grows"

    def __str__(self):
        return f"{self.name} (Start: {self.start_date.strftime('%Y-%m-%d')})"


class Reservoir(models.Model):
    class ReservoirType(models.TextChoices):
        HYDROPONIC = "HYDRO", "Hydroponic"
        NUTRIENT = "NUTRIENT", "Nutrient"
        WATER_STORAGE = "WATER", "Water Storage"
        OTHER = "OTHER", "Other"

    grow = models.ForeignKey(
        "Grow", on_delete=models.CASCADE, related_name="reservoirs"
    )
    name = models.CharField(max_length=100)
    reservoir_type = models.CharField(
        max_length=20,
        choices=ReservoirType.choices,
        default=ReservoirType.OTHER,
    )
    description = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)
    creation_date = models.DateField(default=timezone.now)

    class Meta:
        verbose_name = "Reservoir"
        verbose_name_plural = "Reservoirs"

    def __str__(self):
        return f"{self.name} ({self.get_reservoir_type_display()}) - {self.location}"


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
    last_calibration_date = models.DateField(default=timezone.now)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Measurement Device"
        verbose_name_plural = "Measurement Devices"

    def __str__(self):
        return f"{self.brand} {self.model} - {self.serial_number}"


class Reading(models.Model):
    class ReadingType(models.TextChoices):
        PH = "PH", "pH"
        EC = "EC", "EC"

    class ECUnitChoices(models.TextChoices):
        MS_CM = "mS/cm", "Millisiemens per centimeter (mS/cm)"
        US_CM = "µS/cm", "Microsiemens per centimeter (µS/cm)"
        TDS_PPM = "ppm", "Parts per million (ppm)"

    reservoir = models.ForeignKey(
        "Reservoir", on_delete=models.CASCADE, related_name="readings"
    )
    reading_type = models.CharField(
        max_length=10,
        choices=ReadingType.choices,
        default=ReadingType.PH,
    )
    reading = models.DecimalField(max_digits=5, decimal_places=2)
    unit = models.CharField(
        max_length=10,
        choices=ECUnitChoices.choices,
        blank=True,
        null=True,  # Only relevant for EC readings
    )
    date = models.DateTimeField(default=timezone.now)
    device = models.ForeignKey(
        "MeasurementDevice", on_delete=models.PROTECT, related_name="device_readings"
    )

    class Meta:
        verbose_name = "Reading"
        verbose_name_plural = "Readings"
        unique_together = ["date", "device", "reservoir"]

    def __str__(self):
        return f"{self.reservoir.name} - {self.reading_type} - {self.date.strftime('%Y-%m-%d %H:%M')}"
