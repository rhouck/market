from django.core.management.base import BaseCommand
from market.utils import daily_work

class Command(BaseCommand):
	help = "Sends email alerts when customers have purchased new blocks or requested profile builds."

	def handle(self, *args, **options):
		daily_work()
		self.stdout.write("Successfully checked for customer product updates.")
