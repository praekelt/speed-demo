from django.conf import settings

SETTINGS = {}
try:
    SETTINGS.update(settings.SPEED)
except AttributeError:
    # No overrides
    pass
