from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

def validate_name(name):
    for string in name.split(" "):
        if not string.isalnum():
            raise ValidationError (
            _("Please enter only letters and numbers")
        )