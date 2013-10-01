#encoding:utf-8
from django.core.exceptions import ValidationError
from apps.process_admin.models import UserProfile

def validate_dni(dni):
    if UserProfile.objects.get_or_none(dni=dni):
        raise ValidationError("Ya existe un usuario con esta cédula")