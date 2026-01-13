"""Django management command to populate seed data"""
from django.core.management.base import BaseCommand
from rfp_management.apps.vendors.models import Vendor


class Command(BaseCommand):
    help = 'Populate database with sample vendor data'

    def handle(self, *args, **options):
        vendors = [
            {
                'name': 'Tech Solutions Inc',
                'email': 'sales@techsolutions.com',
                'contact_person': 'John Smith',
                'phone': '555-0101',
                'address': '123 Tech Street',
                'city': 'San Francisco',
                'country': 'USA',
                'website': 'https://techsolutions.com',
                'notes': 'Preferred vendor for IT equipment',
                'active': True
            },
            {
                'name': 'Global Hardware Ltd',
                'email': 'procurement@globalhw.com',
                'contact_person': 'Sarah Johnson',
                'phone': '555-0102',
                'address': '456 Hardware Ave',
                'city': 'New York',
                'country': 'USA',
                'website': 'https://globalhw.com',
                'notes': 'Reliable supplier with good pricing',
                'active': True
            },
            {
                'name': 'Prime Equipment Supply',
                'email': 'sales@primeequip.com',
                'contact_person': 'Mike Chen',
                'phone': '555-0103',
                'address': '789 Supply Road',
                'city': 'Chicago',
                'country': 'USA',
                'website': 'https://primeequip.com',
                'notes': 'Fast delivery capability',
                'active': True
            },
            {
                'name': 'Enterprise Solutions Group',
                'email': 'quote@esg.com',
                'contact_person': 'Linda Davis',
                'phone': '555-0104',
                'address': '321 Enterprise Blvd',
                'city': 'Boston',
                'country': 'USA',
                'website': 'https://esgservices.com',
                'notes': 'High-end enterprise solutions',
                'active': True
            }
        ]

        for vendor_data in vendors:
            vendor, created = Vendor.objects.get_or_create(
                email=vendor_data['email'],
                defaults=vendor_data
            )
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Created vendor: {vendor.name}')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Vendor already exists: {vendor.name}')
                )

        self.stdout.write(self.style.SUCCESS('Successfully populated vendors'))
