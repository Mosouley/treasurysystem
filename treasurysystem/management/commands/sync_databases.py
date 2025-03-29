
from django.core.management.base import BaseCommand
from django.core import management
from treasurysystem.db_router import is_online

class Command(BaseCommand):
    help = 'Synchronize local database with Supabase when coming back online'

    def handle(self, *args, **options):
        if is_online():
            # Create temporary dump from Supabase
            management.call_command('dumpdata', '--database=supabase', '--output=temp_dump.json')
            
            # Load into local database
            management.call_command('loaddata', 'temp_dump.json', '--database=default')
            
            self.stdout.write(self.style.SUCCESS('Successfully synchronized databases'))
        else:
            self.stdout.write(self.style.ERROR('Cannot sync - offline mode'))
