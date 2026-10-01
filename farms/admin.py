from django.contrib import admin
from .models import Farm, Bot, Reading, House
# Register your models here.
admin.site.register(Farm)
admin.site.register(Bot)
admin.site.register(Reading)
admin.site.register(House)