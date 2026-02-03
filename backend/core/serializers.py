from rest_framework import serializers
from .models import EquipmentBatch, EquipmentData


class EquipmentDataSerializer(serializers.ModelSerializer):
    """Serializer for equipment data."""
    class Meta:
        model = EquipmentData
        fields = ['id', 'equipment_name', 'type', 'flowrate', 'pressure', 'temperature']


class EquipmentBatchSerializer(serializers.ModelSerializer):
    """Serializer for equipment batch with nested data."""
    equipment_data = EquipmentDataSerializer(many=True, read_only=True)
    
    class Meta:
        model = EquipmentBatch
        fields = ['id', 'uploaded_at', 'filename', 'equipment_data']


class CSVUploadSerializer(serializers.Serializer):
    """Serializer for CSV file upload."""
    file = serializers.FileField()
    
    def validate_file(self, value):
        if not value.name.endswith('.csv'):
            raise serializers.ValidationError("Only CSV files are allowed.")
        return value


class DashboardStatsSerializer(serializers.Serializer):
    """Serializer for dashboard statistics."""
    total_count = serializers.IntegerField()
    average_values = serializers.DictField()
    type_distribution = serializers.DictField()
