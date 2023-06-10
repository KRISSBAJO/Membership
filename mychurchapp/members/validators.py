from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation
from django.contrib.auth.hashers import check_password
from django.utils.translation import gettext as _

class NoReusePasswordValidator:
    def validate(self, password, user=None):
        if user is not None and user.check_password(password):
            raise ValidationError(
                _("Your new password cannot be the same as your old password."),
                code='password_no_change',
            )

    def get_help_text(self):
        return _("Your new password cannot be the same as your old password.")
