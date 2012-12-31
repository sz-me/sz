from registration import forms as registration_forms
from registration.forms import attrs_dict
from django import forms
from django.utils.translation import ugettext_lazy as _

class RegistrationForm(registration_forms.RegistrationFormUniqueEmail):
    username = forms.RegexField(regex=r'^[A-Za-z]{1}[A-Za-z_0123456789]{2,}$',
        max_length=20,
        widget=forms.TextInput(attrs=attrs_dict),
        label=_("Username"),
        error_messages={'invalid': _("Username may contain only Latin letters, numbers and _ character and must begin with a letter.")})
