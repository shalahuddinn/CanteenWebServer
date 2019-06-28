from django.core.management.base import BaseCommand, CommandError
from webserver import models
from django.utils import timezone


class Command(BaseCommand):
    help = 'Marking Placed Order Older Than 10 Minutes'

    def handle(self, *args, **options):
        # timeNow = timezone.now()
        timeAgo = timezone.now() - timezone.timedelta(minutes=1)
        orders = models.Order.objects.filter(orderStatus="placed").filter(orderTime__lte=timeAgo)
        for order in orders:
            order.orderStatus="expired"
            order.save()
        self.stdout.write('Marked Placed Order Older Than 10 Minutes')
