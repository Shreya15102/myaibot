import csv
from django.core.management.base import BaseCommand
from chat.models import Phone  # update app name if different


class Command(BaseCommand):
    help = "Load phone data from Kaggle CSV into the Phone model"

    def add_arguments(self, parser):
        parser.add_argument('--file', type=str, help='Path to CSV file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['file']
        count = 0

        with open(file_path, newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    phone = Phone.objects.create(
                        brand_name=row.get('brand_name') or row.get('Brand') or row.get('brand'),
                        model=row.get('model') or row.get('Model'),
                        price=self.parse_int(row.get('price')),
                        avg_rating=self.parse_float(row.get('avg_rating')),
                        is_5g=self.parse_bool(row.get('5G_or_not')),
                        processor_brand=row.get('processor_brand'),
                        num_cores=self.parse_int(row.get('num_cores')),
                        processor_speed=self.parse_float(row.get('processor_speed')),
                        battery_capacity=self.parse_int(row.get('battery_capacity')),
                        fast_charging_available=self.parse_bool(row.get('fast_charging_available')),
                        fast_charging=row.get('fast_charging'),
                        ram_capacity=self.parse_int(row.get('ram_capacity')),
                        internal_memory=self.parse_int(row.get('internal_memory')),
                        extended_memory_available=self.parse_bool(row.get('extended_memory_available')),
                        screen_size=self.parse_float(row.get('screen_size')),
                        refresh_rate=self.parse_int(row.get('refresh_rate')),
                        num_rear_cameras=self.parse_int(row.get('num_rear_cameras')),
                        os=row.get('os'),
                        primary_camera_rear=self.parse_int(row.get('primary_camera_rear')),
                        primary_camera_front=self.parse_int(row.get('primary_camera_front')),
                        resolution_height=self.parse_int(row.get('resolution_height')),
                        resolution_width=self.parse_int(row.get('resolution_width')),
                    )
                    count += 1
                except Exception as e:
                    self.stdout.write(self.style.WARNING(f"Skipping row due to error: {e}"))

        self.stdout.write(self.style.SUCCESS(f"Successfully loaded {count} phones"))

    # --- Helper methods ---
    def parse_int(self, value):
        try:
            return int(float(value)) if value not in (None, '', 'NA') else None
        except:
            return None

    def parse_float(self, value):
        try:
            return float(value) if value not in (None, '', 'NA') else None
        except:
            return None

    def parse_bool(self, value):
        if str(value).strip().lower() in ['1', 'true', 'yes']:
            return True
        elif str(value).strip().lower() in ['0', 'false', 'no']:
            return False
        return False
