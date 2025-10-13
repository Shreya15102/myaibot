from django.db import models


class Phone(models.Model):
    brand_name = models.CharField(max_length=50)
    model = models.CharField(max_length=100)
    price = models.IntegerField(null=True, blank=True)
    avg_rating = models.FloatField(null=True, blank=True)

    # Hardware / Specs
    is_5g = models.BooleanField(default=False)
    processor_brand = models.CharField(max_length=50, null=True, blank=True)
    num_cores = models.IntegerField(null=True, blank=True)
    processor_speed = models.FloatField(null=True, blank=True, help_text="in GHz")

    # Battery
    battery_capacity = models.IntegerField(null=True, blank=True, help_text="in mAh")
    fast_charging_available = models.BooleanField(default=False)
    fast_charging = models.CharField(max_length=50, null=True, blank=True)

    # Memory
    ram_capacity = models.IntegerField(null=True, blank=True, help_text="in GB")
    internal_memory = models.IntegerField(null=True, blank=True, help_text="in GB")
    extended_memory_available = models.BooleanField(default=False)

    # Display
    screen_size = models.FloatField(null=True, blank=True, help_text="in inches")
    refresh_rate = models.IntegerField(null=True, blank=True, help_text="in Hz")
    resolution_height = models.IntegerField(null=True, blank=True)
    resolution_width = models.IntegerField(null=True, blank=True)

    # Camera
    num_rear_cameras = models.IntegerField(null=True, blank=True)
    primary_camera_rear = models.IntegerField(null=True, blank=True)
    primary_camera_front = models.IntegerField(null=True, blank=True)

    os = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"{self.brand_name} {self.model}"