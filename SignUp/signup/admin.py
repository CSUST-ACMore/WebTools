from django.contrib import admin

from .models import Participant, Team, Contest, Code


admin.site.site_header = 'ACMore'
admin.site.site_title = 'ACMore'


class ParticipantInline(admin.TabularInline):
    model = Participant
    raw_id_fields = ['team']


class ContestAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'start_time', 'end_time', 'contest_time', 'type']
    list_display_links = ('id', 'name',)


class TeamListFilter(admin.SimpleListFilter):
    title = '审核状态'
    parameter_name = 'remark'

    def lookups(self, request, model_admin):
        return (
            (0, "Accepted"),
            (1, "Rejected"),
            (2, "No Response"),
            (3, "Waiting Judge"),
            (4, "UnRating"),
            (5, "Skipped"),
            (6, "Cancelled"),
            (7, "Deleted"),
        )

    def queryset(self, request, queryset):
        if self.value() is None:
            return queryset
        return Team.objects.filter(pk__in=[tm.pk for tm in queryset if tm.remark == int(self.value())])


class TeamAdmin(admin.ModelAdmin):
    list_display = ['id', 'name',  'get_remark_display']
    list_display_links = ('id', 'name',)
    list_filter = ('contest__name', TeamListFilter)
    search_fields = ('name', )
    inlines = [ParticipantInline]


class ParticipantAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'school_id', 'qq_number', 'faculty', 'remark']
    list_display_links = ('id', 'name',)
    list_filter = ('contest__name', 'remark')
    search_fields = ('name',)
    actions = ['all_ac', 'all_reject']

    def all_ac(self, request, queryset):
        queryset.update(remark=0)

    def all_reject(self, request, queryset):
        queryset.update(remark=1)

    all_ac.short_description = "全部Accept"
    all_reject.short_description = "全部Reject"


class CodeAdmin(admin.ModelAdmin):
    list_display = ['id', 'team', 'pw', 'printed']
    list_filter = ('contest__name', 'printed')


admin.site.register(Contest, ContestAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Participant, ParticipantAdmin)
admin.site.register(Code, CodeAdmin)

