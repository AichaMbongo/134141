# management/commands/create_custom_superuser.py

from django.core.management.base import BaseCommand
from user_app.models import User  # Import your custom User model
from django.utils.crypto import get_random_string
from django.contrib.auth.hashers import make_password

class Command(BaseCommand):
    help = 'Create a custom superuser'

    def handle(self, *args, **options):
        email = input('Enter email address: ')
        password = None
        while not password:
            # Prompt for password and confirmation
            password = input('Enter password: ')
            confirm_password = input('Confirm password: ')
            if password != confirm_password:
                self.stdout.write(self.style.ERROR("Passwords don't match. Please try again."))
                password = None

        # Check if the user already exists
        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.ERROR('User with this email address already exists'))
            return

        # Create the custom superuser
        user = User.objects.create_user(email=email, password=make_password(password), is_superuser=True)
        user.is_active = True
        user.is_staff = True
        user.save()

        self.stdout.write(self.style.SUCCESS('Superuser created successfully'))
