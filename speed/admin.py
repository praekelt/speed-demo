from django.contrib import admin

from jmbo.admin import ModelBaseAdmin
from speed.models import TrivialContent, Car, Container


admin.site.register(TrivialContent, ModelBaseAdmin)
admin.site.register(Car, admin.ModelAdmin)
admin.site.register(Container, admin.ModelAdmin)
