from django.contrib import admin
from . import models
# Register your models here.
admin.site.register(models.Disaster)
admin.site.register(models.DisasterList)
admin.site.register(models.Volunteer)
admin.site.register(models.Location)
admin.site.register(models.VolunteerAssginment)
admin.site.register(models.Task)
admin.site.register(models.States)