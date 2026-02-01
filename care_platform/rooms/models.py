from django.db import models


class Room(models.Model):
    """Room Model"""
    
    class Meta:
        db_table = 'rooms'
        verbose_name = 'Room Info'
        verbose_name_plural = 'Room Info'
    
    room_number = models.CharField(
        max_length=20,
        unique=True,
        verbose_name='Room Number',
        help_text='Room Number, e.g. 101, 102'
    )
    
    bed1 = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Bed 1 ID',
        help_text='Bed 1 ID'
    )
    
    bed2 = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Bed 2 ID',
        help_text='Bed 2 ID'
    )
    
    bed3 = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Bed 3 ID',
        help_text='Bed 3 ID'
    )
    
    bed4 = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Bed 4 ID',
        help_text='Bed 4 ID'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.room_number
    
    def get_available_beds(self):
        """Get available beds"""
        beds = []
        if self.bed1:
            beds.append(self.bed1)
        if self.bed2:
            beds.append(self.bed2)
        if self.bed3:
            beds.append(self.bed3)
        if self.bed4:
            beds.append(self.bed4)
        return beds
    
    def get_bed_count(self):
        """Get total bed count"""
        return len(self.get_available_beds())