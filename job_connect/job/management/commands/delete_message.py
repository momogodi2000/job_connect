from django.core.management.base import BaseCommand
from job.models import Message
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Deletes messages older than 1 month'

    def handle(self, *args, **kwargs):
        threshold_date = timezone.now() - timedelta(days=30)
        old_messages = Message.objects.filter(created_at__lt=threshold_date)
        old_messages.delete()
        self.stdout.write(f"Deleted {old_messages.count()} old messages.")
