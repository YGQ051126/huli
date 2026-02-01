# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.utils import timezone
from patients.models import Patient
from care_records.models import CareTemplate
from tasks.models import Task
from users.models import StaffUser
from datetime import timedelta

class Command(BaseCommand):
    help = 'Generate daily care tasks for patients based on their care level'

    def handle(self, *args, **options):
        self.stdout.write('Starting daily task generation...')
        
        today = timezone.now().date()
        active_patients = Patient.objects.filter(status='active')
        
        tasks_created = 0
        
        for patient in active_patients:
            if not patient.care_level:
                continue
                
            # Find applicable template
            template = CareTemplate.objects.filter(
                care_level=patient.care_level,
                is_active=True
            ).first()
            
            if not template:
                continue
                
            # Parse tasks from template content
            # Assuming template_content has a 'tasks' list
            # Format: {'tasks': [{'title': '...', 'description': '...', 'time': '08:00'}]}
            content = template.template_content or {}
            if isinstance(content, dict):
                routine_tasks = content.get('tasks', [])
            else:
                routine_tasks = []
            
            # If no explicit tasks, maybe generate a generic one based on fields?
            if not routine_tasks and isinstance(content, dict):
                fields = content.get('fields', [])
                if fields:
                    routine_tasks.append({
                        'title': '日常护理记录',
                        'description': '完成每日护理记录填报',
                        'priority': 'medium',
                        'due_time': '18:00'
                    })
            
            for task_info in routine_tasks:
                title = task_info.get('title')
                description = task_info.get('description', '')
                priority = task_info.get('priority', 'medium')
                due_time_str = task_info.get('time') or task_info.get('due_time')
                
                due_date = today
                # You might want to combine date and time if Task model supports datetime
                # Task model usually has due_date as Date or DateTime
                
                # Assign to primary nurse if available
                assigned_staff = None
                if patient.primary_nurse:
                    try:
                        # patient.primary_nurse is a User (due to my change), need StaffUser
                        assigned_staff = StaffUser.objects.get(user=patient.primary_nurse)
                    except StaffUser.DoesNotExist:
                        pass
                
                # Check if task already exists to avoid duplicates
                if not Task.objects.filter(
                    patient=patient,
                    title=title,
                    due_date=due_date
                ).exists():
                    Task.objects.create(
                        title=title,
                        description=description,
                        patient=patient,
                        staff=assigned_staff,
                        priority=priority,
                        due_date=due_date,
                        status='pending'
                    )
                    tasks_created += 1
        
        self.stdout.write(self.style.SUCCESS(f'Successfully generated {tasks_created} tasks for {today}'))
