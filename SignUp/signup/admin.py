from django.contrib import admin

from .models import Participant

# Register your models here.
class ParticipantAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'school_id', 'qq_number', 'faculty', 'remark']


admin.site.register(Participant, ParticipantAdmin)
