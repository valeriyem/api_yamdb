from django.core.exceptions import ValidationError
from django.utils import timezone


def year_validator(year):
    """Проверяет, что год не превышает текущий."""
    if not (0 < year <= timezone.now().year):
        raise ValidationError('Исправьте год произведения.')
