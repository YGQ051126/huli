from django.core.management.base import BaseCommand
from django.utils import timezone
from patients.models import Patient
from care_records.models import DailyCareTask
import logging

logger = logging.getLogger(__name__)

class Command(BaseCommand):
    help = 'Generate daily care tasks for all patients'

    def handle(self, *args, **options):
        today = timezone.now().date()
        yesterday = today - timezone.timedelta(days=1)
        
        self.stdout.write(f"Generating tasks for {today}...")
        
        # 1. Clear cache (Conceptual, or if using Redis cache delete keys)
        # For now, we assume no persistent cache keys to clear manually except log it.
        self.stdout.write("Clearing yesterday's cache...")
        
        # 2. Generate Today's Tasks
        patients = Patient.objects.all()
        created_count = 0
        skipped_count = 0
        
        new_tasks = []
        for patient in patients:
            if DailyCareTask.objects.filter(patient=patient, task_date=today).exists():
                skipped_count += 1
                continue
            
            new_tasks.append(DailyCareTask(
                patient=patient,
                task_date=today
            ))
            created_count += 1
        
        if new_tasks:
            DailyCareTask.objects.bulk_create(new_tasks)
            
        self.stdout.write(f"Created {created_count} tasks, Skipped {skipped_count} existing tasks.")
        
        # 3. Simulated WebSocket Push
        self.stdout.write("Pushing WebSocket message to frontend: {type: 'DAILY_TASKS_RESET'}")
        # In a real app with Channels:
        # channel_layer = get_channel_layer()
        # async_to_sync(channel_layer.group_send)("staff_dashboard", {"type": "daily_tasks_reset"})
        
        self.stdout.write(self.style.SUCCESS('Successfully generated daily tasks'))
