from django.utils.translation import ngettext
from django.core.exceptions import ValidationError
import re

class MyCustomPasswordValidator(object):
    def __init__(self, min_length=6):  # put default min_length here
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                ngettext(
                    # silly, I know, but if your min length is one, put your message here
                    "This password is too short. It must contain at least %(min_length)d character.",
                    # if it's more than one (which it probably is) put your message here
                    "This password is too short. It must contain at least %(min_length)d characters.",
                    self.min_length
                ),
                code='password_too_short',
                params={'min_length': self.min_length},
            )

        else:
            # Minimum six characters, Maximum 20 Characters, at least one Uppercase and Lowecase letter and one number:
            password_regex = (
                "(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$")

            password_regex_compile = re.compile(password_regex)

            if (re.search(password_regex_compile, password)):
                password_validation = True

        return password_validation

    def get_help_text(self):
        return ngettext(
            # you can also change the help text to whatever you want for use in the templates (password.help_text)
            "Your password must contain at least %(min_length)d character.",
            "Your password must contain at least %(min_length)d characters.",
            self.min_length
        ) % {'min_length': self.min_length}
