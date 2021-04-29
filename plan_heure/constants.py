from django.utils.translation import gettext_lazy as _


MAN = 'M'
WOMAN = 'W'
UNDEFINED = 'U'
GENDERS = (
    (MAN, _('Mr')),
    (WOMAN, _('Mme')),
    (UNDEFINED, _('Non défini')),
)
