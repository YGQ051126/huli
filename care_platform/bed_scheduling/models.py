from django.db import models
from django.conf import settings
from rooms.models import Room
from patients.models import Patient

class BedAssignment(models.Model):
    """Bed Assignment Model"""
    elderly = models.ForeignKey(Patient, on_delete=models.CASCADE, verbose_name="Elderly")
    room = models.ForeignKey(Room, on_delete=models.CASCADE, verbose_name="Room")
    bed_number = models.CharField(max_length=10, verbose_name="Bed Number")
    
    assigned_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, verbose_name="Assigned By")
    assign_date = models.DateTimeField(verbose_name="Assign Date")
    release_date = models.DateTimeField(null=True, blank=True, verbose_name="Release Date")
    
    status = models.CharField(
        max_length=20,
        choices=[
            ('active', 'Active'),
            ('completed', 'Completed'),
            ('cancelled', 'Cancelled'),
        ],
        default='active',
        verbose_name="Status"
    )
    
    notes = models.TextField(blank=True, verbose_name="Notes")
    cleaning_notified = models.BooleanField(default=False, verbose_name="Cleaning Notified")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Bed Assignment"
        verbose_name_plural = "Bed Assignments"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.elderly.name} - {self.room.room_number}-{self.bed_number}"
