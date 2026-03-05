from django.core.management.base import BaseCommand
from kenyan_counties.core import get_all_counties
from kenyan_counties.models import County, Constituency, Ward
from django.db import transaction

class Command(BaseCommand):
    help = "Loads all Kenyan counties, constituencies, and wards into the database."

    def handle(self, *args, **options):
        self.stdout.write("Starting to load Kenya counties data...")

        counties_data = get_all_counties()
        
        with transaction.atomic():
            for c_data in counties_data:
                # Get or Create County
                county, created = County.objects.get_or_create(
                    code=c_data.code,
                    defaults={'name': c_data.name}
                )
                if not created and county.name != c_data.name:
                    county.name = c_data.name
                    county.save()
                    
                for const_data in c_data.constituencies:
                    # Get or Create Constituency
                    constituency, created = Constituency.objects.get_or_create(
                        county=county,
                        name=const_data.name
                    )

                    for ward_data in const_data.wards:
                        # Get or Create Ward
                        Ward.objects.get_or_create(
                            constituency=constituency,
                            name=ward_data.name
                        )

        self.stdout.write(self.style.SUCCESS("Successfully loaded all Kenyan counties, constituencies, and wards!"))
