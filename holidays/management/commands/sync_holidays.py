from workalendar.europe import Hungary, Austria
from django.core.management.base import BaseCommand
from datetime import date
from holidays.models import Holiday

class Command(BaseCommand):
    help = 'Egymásba fűzi (szinkronizálja) a megadott évre az osztrák és magyar naptárak hivatalos ünnepeit az adatbázisunkkal.'

    def add_arguments(self, parser):
        parser.add_argument('year', type=int, help='A naptári év, amelynek az ünnepeit be kell tölteni.')

    def handle(self, *args, **kwargs):
        year = kwargs['year']

        calendars = {
            'hu': Hungary(),
            'at': Austria(),
        }

        created_count = 0

        for cal_code, cal_obj in calendars.items():
            self.stdout.write(f'--- {cal_code.upper()} naptár ({year}) feldolgozása ---')
            
            holidays_list = cal_obj.holidays(year)
            
            for hol_date, hol_name in holidays_list:
                obj, created = Holiday.objects.update_or_create(
                    calendar=cal_code,
                    date=hol_date,
                    defaults={'description': hol_name, 'is_working_day': False}
                )
                if created:
                    created_count += 1
                    self.stdout.write(self.style.SUCCESS(f"Hozzáadva: {hol_date} - {hol_name} ({cal_code})"))
                else:
                    self.stdout.write(f"Már létezik: {hol_date} - {hol_name} ({cal_code})")

        self.stdout.write(self.style.SUCCESS(f'Sikeresen feldolgozva. Újonnan felvett ünnepek: {created_count} db.'))