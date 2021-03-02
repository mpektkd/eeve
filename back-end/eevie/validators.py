from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
import datetime

def validate_year(value):
    if((value < 2010) or (value > datetime.datetime.now().year)):
        raise ValidationError(
            _('%(value)s is not a valid release year.'),
            params={'value': value},
        )

def validate_percentage(value):
    if(value > 100):
        raise ValidationError(
            _('%(value)s is not a valid percentage for battery size.'),
            params={'value': value},
        )
