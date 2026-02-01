from django.core.management.base import BaseCommand
from users.models import User

class Command(BaseCommand):
    help = "Ensure admin user exists with username 'admin' and password 'admin123'"

    def handle(self, *args, **options):
        try:
            admin, created = User.objects.get_or_create(
                username='admin',
                defaults={
                    'password': 'admin123',
                    'real_name': 'System Admin',
                    'phone': '13800000000',
                    'email': 'admin@huli.com',
                    'role': 'admin',
                    'status': 'active',
                    'is_staff': True,
                    'is_superuser': True,
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS("Created admin user: admin / admin123"))
            else:
                admin.password = 'admin123'
                admin.role = 'admin'
                admin.status = 'active'
                admin.is_staff = True
                admin.is_superuser = True
                admin.save()
                self.stdout.write(self.style.SUCCESS("Reset admin user password to 'admin123'"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to ensure admin user: {e}"))
