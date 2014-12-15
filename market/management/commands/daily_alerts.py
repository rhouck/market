from django.core.management.base import BaseCommand
from market.utils import daily_work

class Command(BaseCommand):
	help = "Sends email alerts when customers have purchased new blocks or requested profile builds."

	def handle(self, *args, **options):
		# don't send emails if test = True
		test = True if 'test' in args else False
		daily_work(test=test)
		self.stdout.write("Successfully checked for customer product updates.")