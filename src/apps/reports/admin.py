from django.contrib import admin
from apps.reports.models import (NewUsersReport, VotesReport, OpinionsReport,
                                 DocumentsReport, ParticipantsReport)


class NewUsersAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'period', 'new_users', 'created')
    list_filter = ['start_date', 'period']


class VotesReportAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'period', 'votes', 'created')
    list_filter = ['start_date', 'period']


class OpinionsReportAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'period', 'opinions', 'created')
    list_filter = ['start_date', 'period']


class DocumentsReportAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'period', 'documents', 'created')
    list_filter = ['start_date', 'period']


class ParticipantsReportAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'period', 'participants', 'created')
    list_filter = ['start_date', 'period']


admin.site.register(NewUsersReport, NewUsersAdmin)
admin.site.register(VotesReport, VotesReportAdmin)
admin.site.register(OpinionsReport, OpinionsReportAdmin)
admin.site.register(DocumentsReport, DocumentsReportAdmin)
admin.site.register(ParticipantsReport, ParticipantsReportAdmin)
