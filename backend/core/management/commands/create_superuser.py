"""
Management command to create a superuser for the Chemical Equipment Visualizer.
Run with: python manage.py create_superuser
"""
import os
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token


class Command(BaseCommand):
    help = 'Creates a superuser with default credentials for development'

    def handle(self, *args, **options):
        username = 'admin'
        email = 'admin@example.com'
        password = 'admin123'
        
        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f'User "{username}" already exists.'))
            user = User.objects.get(username=username)
        else:
            user = User.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" created successfully!'))
        
        # Create or get token
        token, created = Token.objects.get_or_create(user=user)
        
        self.stdout.write('')
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write(self.style.SUCCESS('Default Credentials:'))
        self.stdout.write(self.style.SUCCESS('=' * 50))
        self.stdout.write(f'  Username: {username}')
        self.stdout.write(f'  Password: {password}')
        self.stdout.write(f'  Email: {email}')
        self.stdout.write(f'  API Token: {token.key}')
        self.stdout.write(self.style.SUCCESS('=' * 50))
