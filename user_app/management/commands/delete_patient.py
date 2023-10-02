# user_app/management/commands/delete_patient.py

from django.core.management.base import BaseCommand
from user_app.models import Patient

class Command(BaseCommand):
    help = 'Deletes the Patient record with id = 6 or creates it if not exists.'

    def handle(self, *args, **options):
        try:
            # Try to get the existing patient
            patient = Patient.objects.get(id=6)
            patient.delete()
            self.stdout.write(self.style.SUCCESS(f"Patient with id = 6 deleted: {patient}"))
        except Patient.DoesNotExist:
            # If patient doesn't exist, create a new one
            new_patient = Patient(
                id=6,
                firstName="John",
                lastName="okoth",
                email="john.okoth@example.com",
                phoneNo="1234567890",
                sex="M",
            )
            new_patient.save()
            self.stdout.write(self.style.SUCCESS(f"Patient with id = 6 created: {new_patient}"))
