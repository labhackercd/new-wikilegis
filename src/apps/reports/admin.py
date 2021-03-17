from django.contrib import admin
from apps.reports.models import (NewUsersReport, VotesReport, OpinionReport,
                                 DocumentReport)


class NewUsersAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'period', 'new_users', 'created')
    list_filter = ['start_date', 'period']


class VotesReportAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'period', 'votes', 'created')
    list_filter = ['start_date', 'period']


class OpinionReportAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'period', 'opinions', 'created')
    list_filter = ['start_date', 'period']


class DocumentReportAdmin(admin.ModelAdmin):
    list_display = ('start_date', 'period', 'documents', 'created')
    list_filter = ['start_date', 'period']


admin.site.register(NewUsersReport, NewUsersAdmin)
admin.site.register(VotesReport, VotesReportAdmin)
admin.site.register(OpinionReport, OpinionReportAdmin)
admin.site.register(DocumentReport, DocumentReportAdmin)
