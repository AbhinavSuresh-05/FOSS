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


class BatchHistorySerializer(serializers.ModelSerializer):
    """Serializer for batch history with summary stats."""
    total_records = serializers.IntegerField(read_only=True)
    avg_flowrate = serializers.FloatField(read_only=True)
    avg_pressure = serializers.FloatField(read_only=True)
    avg_temperature = serializers.FloatField(read_only=True)
    
    class Meta:
        model = EquipmentBatch
        fields = ['id', 'uploaded_at', 'filename', 'total_records', 'avg_flowrate', 'avg_pressure', 'avg_temperature']



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


class UserRegistrationSerializer(serializers.Serializer):
    """Serializer for user registration with password validation."""
    username = serializers.CharField(min_length=3, max_length=150)
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True, min_length=8)
    
    def validate_username(self, value):
        from django.contrib.auth.models import User
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("Username already exists.")
        return value
    
    def validate_password(self, value):
        import re
        # Check for at least one letter
        if not re.search(r'[a-zA-Z]', value):
            raise serializers.ValidationError("Password must contain at least one letter.")
        # Check for at least one number
        if not re.search(r'\d', value):
            raise serializers.ValidationError("Password must contain at least one number.")
        # Check for at least one special character
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', value):
            raise serializers.ValidationError("Password must contain at least one special character.")
        return value
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password_confirm": "Passwords do not match."})
        return data
    
    def create(self, validated_data):
        from django.contrib.auth.models import User
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user

