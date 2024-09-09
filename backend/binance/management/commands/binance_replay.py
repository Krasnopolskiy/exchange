from django.core.management import BaseCommand

from backend.binance.tasks import replay


class Command(BaseCommand):
    help = "Replays data fetched from Binance."

    def handle(self, *args, **options):
        replay.delay()
