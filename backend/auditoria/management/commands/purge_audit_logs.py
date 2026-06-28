from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from auditoria.models import AuditLog


class Command(BaseCommand):
    help = 'Purge audit logs older than specified days (default 365, i.e., 12 months)'

    def add_arguments(self, parser):
        parser.add_argument(
            '--days',
            type=int,
            default=365,
            help='Number of days to retain (default: 365)',
        )

    def handle(self, *args, **options):
        days = options['days']
        cutoff_date = timezone.now() - timedelta(days=days)

        deleted_count, _ = AuditLog.objects.filter(data_hora__lt=cutoff_date).delete()

        self.stdout.write(
            self.style.SUCCESS(
                f'✓ Deleted {deleted_count} audit logs older than {days} days '
                f'(before {cutoff_date.date()})'
            )
        )
