from django.contrib import admin

from .models import Participant

# Register your models here.


class ParticipantAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'school_id', 'qq_number', 'faculty', 'remark']
    actions = ['all_ac']

    def all_ac(self, request, queryset):
        queryset.update(remark=0)
    all_ac.short_description = "全部AC"


admin.site.register(Participant, ParticipantAdmin)
