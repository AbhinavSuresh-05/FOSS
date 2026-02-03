from django.contrib import admin
from .models import EquipmentBatch, EquipmentData


class EquipmentDataInline(admin.TabularInline):
    model = EquipmentData
    extra = 0
    readonly_fields = ['equipment_name', 'type', 'flowrate', 'pressure', 'temperature']


@admin.register(EquipmentBatch)
class EquipmentBatchAdmin(admin.ModelAdmin):
    list_display = ['id', 'filename', 'uploaded_at', 'user', 'data_count']
    list_filter = ['uploaded_at', 'user']
    readonly_fields = ['uploaded_at']
    inlines = [EquipmentDataInline]
    
    def data_count(self, obj):
        return obj.equipment_data.count()
    data_count.short_description = 'Records'


@admin.register(EquipmentData)
class EquipmentDataAdmin(admin.ModelAdmin):
    list_display = ['equipment_name', 'type', 'flowrate', 'pressure', 'temperature', 'batch']
    list_filter = ['type', 'batch']
    search_fields = ['equipment_name', 'type']
