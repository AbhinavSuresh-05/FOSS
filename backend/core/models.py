from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class EquipmentBatch(models.Model):
    """Stores metadata for an upload batch."""
    uploaded_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    filename = models.CharField(max_length=255, default='')
    
    class Meta:
        ordering = ['-uploaded_at']
        verbose_name_plural = 'Equipment Batches'
    
    def __str__(self):
        return f"Batch {self.id} - {self.uploaded_at.strftime('%Y-%m-%d %H:%M')}"


class EquipmentData(models.Model):
    """Stores the actual row data linked to a batch."""
    equipment_name = models.CharField(max_length=255)
    type = models.CharField(max_length=100)
    flowrate = models.FloatField()
    pressure = models.FloatField()
    temperature = models.FloatField()
    batch = models.ForeignKey(
        EquipmentBatch, 
        on_delete=models.CASCADE, 
        related_name='equipment_data'
    )
    
    class Meta:
        verbose_name_plural = 'Equipment Data'
    
    def __str__(self):
        return f"{self.equipment_name} ({self.type})"


@receiver(post_save, sender=EquipmentBatch)
def enforce_batch_limit(sender, instance, created, **kwargs):
    """Ensure only the last 5 batches are kept PER USER."""
    if created and instance.user:
        batches = EquipmentBatch.objects.filter(user=instance.user).order_by('-uploaded_at')
        if batches.count() > 5:
            # Get batches to delete (all beyond the 5 most recent)
            batches_to_delete = batches[5:]
            for batch in batches_to_delete:
                batch.delete()  # This will cascade delete related EquipmentDat
