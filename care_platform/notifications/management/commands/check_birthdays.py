# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from django.utils import timezone
from patients.models import Patient
from notifications.models import Notification
from users.models import FamilyUser, StaffUser
from datetime import datetime

class Command(BaseCommand):
    help = 'Check patient birthdays and send notifications'

    def handle(self, *args, **options):
        self.stdout.write('Checking birthdays...')
        
        today = timezone.now().date()
        patients = Patient.objects.filter(status='active')
        
        count = 0
        
        for patient in patients:
            # Check if today is birthday
            # Assuming id_card has birthday or there is a birthday field?
            # Patient model has 'age' but not 'birthday'.
            # It has 'id_card'. We can extract birthday from ID card.
            
            birthday = None
            if patient.id_card and len(patient.id_card) == 18:
                try:
                    birth_str = patient.id_card[6:14]
                    birthday = datetime.strptime(birth_str, '%Y%m%d').date()
                except ValueError:
                    pass
            
            if birthday:
                if birthday.month == today.month and birthday.day == today.day:
                    self.send_birthday_notification(patient)
                    count += 1
        
        self.stdout.write(self.style.SUCCESS(f'Sent {count} birthday notifications'))

    def send_birthday_notification(self, patient):
        # Notify Family
        family_users = FamilyUser.objects.filter(patient=patient)
        for fu in family_users:
            Notification.objects.create(
                user=fu.user,
                type='care',
                title='生日提醒',
                content=f'今天是您的家属 {patient.name} 的生日，祝他/她生日快乐！',
                related_id=patient.id,
                related_type='patient_birthday'
            )
            
        # Notify Staff
        # If patient has primary nurse, notify them
        if patient.primary_nurse:
            Notification.objects.create(
                user=patient.primary_nurse,
                type='care',
                title='院民生日提醒',
                content=f'今天是您负责的院民 {patient.name} 的生日，请关注。',
                related_id=patient.id,
                related_type='patient_birthday'
            )
