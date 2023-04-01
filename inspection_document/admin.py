from django.contrib import admin
from .models import InspectionDocument


class InspectionDocumentAdmin(admin.ModelAdmin):
    list_display = ('inspection_id', 'comment')


admin.site.register(InspectionDocument, InspectionDocumentAdmin)
