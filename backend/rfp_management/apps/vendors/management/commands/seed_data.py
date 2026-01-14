"""
Django management command to seed the database with sample data.
Usage: python manage.py seed_data
"""
from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from rfp_management.apps.vendors.models import Vendor
from rfp_management.apps.rfps.models import RFP
from rfp_management.apps.proposals.models import Proposal


class Command(BaseCommand):
    help = 'Seed the database with sample vendors, RFPs, and proposals'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting data seeding...'))

        # Clear existing data
        Vendor.objects.all().delete()
        RFP.objects.all().delete()
        Proposal.objects.all().delete()
        self.stdout.write('Cleared existing data')

        # Create 5 Vendors
        vendors_data = [
            {
                'name': 'TechCorp Solutions',
                'email': 'contact@techcorp.com',
                'contact_person': 'John Anderson',
                'phone': '+1-555-0101',
                'address': '123 Tech Street',
                'city': 'San Francisco',
                'country': 'USA',
                'website': 'https://techcorp.com',
                'notes': 'Leading cloud infrastructure provider',
            },
            {
                'name': 'DataSystems Global',
                'email': 'sales@datasystems.com',
                'contact_person': 'Sarah Johnson',
                'phone': '+1-555-0102',
                'address': '456 Data Avenue',
                'city': 'New York',
                'country': 'USA',
                'website': 'https://datasystems.com',
                'notes': 'Enterprise data management specialists',
            },
            {
                'name': 'CloudFirst Innovations',
                'email': 'info@cloudfirst.com',
                'contact_person': 'Michael Chen',
                'phone': '+1-555-0103',
                'address': '789 Cloud Lane',
                'city': 'Seattle',
                'country': 'USA',
                'website': 'https://cloudfirst.com',
                'notes': 'AWS and Azure certified partners',
            },
            {
                'name': 'DevOps Experts Inc',
                'email': 'support@devopsexperts.com',
                'contact_person': 'Emily Rodriguez',
                'phone': '+1-555-0104',
                'address': '321 Deploy Street',
                'city': 'Austin',
                'country': 'USA',
                'website': 'https://devopsexperts.com',
                'notes': 'Kubernetes and containerization experts',
            },
            {
                'name': 'SecureNet Solutions',
                'email': 'hello@securenet.com',
                'contact_person': 'David Kumar',
                'phone': '+1-555-0105',
                'address': '654 Security Drive',
                'city': 'Boston',
                'country': 'USA',
                'website': 'https://securenet.com',
                'notes': 'Cybersecurity and compliance specialists',
            },
        ]

        vendors = []
        for vendor_data in vendors_data:
            vendor = Vendor.objects.create(**vendor_data)
            vendors.append(vendor)
            self.stdout.write(f'Created vendor: {vendor.name}')

        # Create 5 RFPs
        rfps_data = [
            {
                'title': 'Cloud Infrastructure Migration',
                'description': 'We need to migrate our legacy on-premise infrastructure to cloud. The project includes database migration, application deployment, and infrastructure monitoring setup.',
                'budget': '500000.00',
                'deadline': timezone.now() + timedelta(days=90),
                'status': 'SENT',
                'natural_language_input': 'Migrate to cloud with database and monitoring',
                'requirements': {
                    'infrastructure': 'AWS or Azure cloud platform',
                    'database': 'PostgreSQL or MySQL migration',
                    'monitoring': 'CloudWatch or DataDog integration',
                    'security': 'SSL/TLS encryption required',
                    'timeline': '3 months'
                },
                'selected_vendors': [1, 2, 3],
            },
            {
                'title': 'Big Data Analytics Platform',
                'description': 'We require a modern big data analytics platform capable of processing terabytes of data daily. The solution should support real-time analytics and machine learning integration.',
                'budget': '750000.00',
                'deadline': timezone.now() + timedelta(days=120),
                'status': 'SENT',
                'natural_language_input': 'Big data analytics with ML capabilities',
                'requirements': {
                    'platform': 'Hadoop, Spark, or Elasticsearch',
                    'processing': 'Real-time stream processing',
                    'storage': 'Distributed storage (S3, HDFS)',
                    'ml_integration': 'TensorFlow or PyTorch support',
                    'scalability': '10000+ concurrent users'
                },
                'selected_vendors': [2, 4, 5],
            },
            {
                'title': 'Kubernetes Cluster Setup',
                'description': 'Design and implement a highly available Kubernetes cluster for our microservices architecture. Include load balancing, auto-scaling, and disaster recovery.',
                'budget': '300000.00',
                'deadline': timezone.now() + timedelta(days=60),
                'status': 'SENT',
                'natural_language_input': 'Setup Kubernetes cluster with HA and auto-scaling',
                'requirements': {
                    'platform': 'Kubernetes 1.28+',
                    'ha': 'Multi-node cluster with 99.9% uptime SLA',
                    'autoscaling': 'Horizontal and vertical pod autoscaling',
                    'networking': 'Service mesh (Istio) implementation',
                    'monitoring': 'Prometheus and Grafana stack'
                },
                'selected_vendors': [1, 3, 4],
            },
            {
                'title': 'Enterprise Security Framework',
                'description': 'Implement comprehensive enterprise security framework including network security, identity management, threat detection, and compliance auditing.',
                'budget': '400000.00',
                'deadline': timezone.now() + timedelta(days=75),
                'status': 'DRAFT',
                'natural_language_input': 'Enterprise security with identity and threat detection',
                'requirements': {
                    'identity': 'Active Directory or Okta integration',
                    'threat_detection': 'SIEM with AI-powered anomaly detection',
                    'compliance': 'GDPR, HIPAA, and SOC 2 certified',
                    'firewall': 'Next-generation firewall with DPI',
                    'audit': 'Complete audit logging and reporting'
                },
                'selected_vendors': [3, 5],
            },
            {
                'title': 'AI-Powered Customer Analytics',
                'description': 'Develop an AI-powered customer analytics platform that provides real-time insights into customer behavior, churn prediction, and personalization recommendations.',
                'budget': '600000.00',
                'deadline': timezone.now() + timedelta(days=100),
                'status': 'DRAFT',
                'natural_language_input': 'AI customer analytics with churn prediction',
                'requirements': {
                    'ai_framework': 'TensorFlow, PyTorch, or scikit-learn',
                    'predictions': 'Churn, LTV, and propensity models',
                    'realtime': 'Sub-second prediction latency',
                    'integration': 'CRM and marketing automation tools',
                    'visualization': 'Interactive dashboards with Tableau'
                },
                'selected_vendors': [2, 4],
            },
        ]

        rfps = []
        for rfp_data in rfps_data:
            rfp = RFP.objects.create(**rfp_data)
            rfps.append(rfp)
            self.stdout.write(f'Created RFP: {rfp.title}')

        # Create 5 Proposals
        proposals_data = [
            {
                'rfp_id': rfps[0].id,
                'vendor_id': vendors[0].id,
                'vendor_name': vendors[0].name,
                'proposal_content': 'We propose a comprehensive AWS migration solution with 99.99% uptime SLA. Our team has 15+ years of cloud infrastructure experience.',
                'parsed_data': {
                    'proposal_summary': 'AWS migration with 99.99% uptime SLA',
                    'key_benefits': ['High availability', 'Cost optimization', 'Security']
                },
                'price': '450000.00',
                'delivery_time': '90 days',
                'warranty': '1 year',
                'payment_terms': '30% upfront, 40% mid-project, 30% completion',
                'status': 'EVALUATED',
                'score': 92.5,
                'evaluation': {
                    'technical_score': 95,
                    'cost_score': 90,
                    'timeline_score': 90,
                    'experience_score': 95,
                    'recommendation': 'Highly recommended - Best fit for requirements'
                }
            },
            {
                'rfp_id': rfps[0].id,
                'vendor_id': vendors[1].id,
                'vendor_name': vendors[1].name,
                'proposal_content': 'We offer Azure cloud migration with enterprise-grade security. Implementation includes hybrid cloud strategy.',
                'parsed_data': {
                    'proposal_summary': 'Azure migration with hybrid cloud strategy',
                    'key_benefits': ['Flexibility', 'Enterprise security', 'Hybrid support']
                },
                'price': '480000.00',
                'delivery_time': '100 days',
                'warranty': '2 years',
                'payment_terms': '25% upfront, 50% mid-project, 25% completion',
                'status': 'EVALUATED',
                'score': 88.0,
                'evaluation': {
                    'technical_score': 88,
                    'cost_score': 85,
                    'timeline_score': 85,
                    'experience_score': 90,
                    'recommendation': 'Recommended - Good alternative option'
                }
            },
            {
                'rfp_id': rfps[1].id,
                'vendor_id': vendors[1].id,
                'vendor_name': vendors[1].name,
                'proposal_content': 'Enterprise big data platform using Hadoop and Spark with 24/7 support. We guarantee 99.95% availability.',
                'parsed_data': {
                    'proposal_summary': 'Hadoop/Spark big data platform with ML',
                    'key_benefits': ['Real-time processing', 'ML integration', 'Enterprise support']
                },
                'price': '720000.00',
                'delivery_time': '120 days',
                'warranty': '2 years',
                'payment_terms': '20% upfront, 60% mid-project, 20% completion',
                'status': 'EVALUATED',
                'score': 91.0,
                'evaluation': {
                    'technical_score': 93,
                    'cost_score': 90,
                    'timeline_score': 90,
                    'experience_score': 92,
                    'recommendation': 'Highly recommended - Top choice'
                }
            },
            {
                'rfp_id': rfps[2].id,
                'vendor_id': vendors[3].id,
                'vendor_name': vendors[3].name,
                'proposal_content': 'Complete Kubernetes cluster setup with full HA configuration. Includes CI/CD pipeline, monitoring, and disaster recovery.',
                'parsed_data': {
                    'proposal_summary': 'Kubernetes cluster with HA and CI/CD',
                    'key_benefits': ['High availability', 'Auto-scaling', 'Complete monitoring']
                },
                'price': '280000.00',
                'delivery_time': '60 days',
                'warranty': '1 year',
                'payment_terms': '30% upfront, 40% mid-project, 30% completion',
                'status': 'EVALUATED',
                'score': 94.5,
                'evaluation': {
                    'technical_score': 96,
                    'cost_score': 93,
                    'timeline_score': 94,
                    'experience_score': 95,
                    'recommendation': 'Highly recommended - Best value'
                }
            },
            {
                'rfp_id': rfps[3].id,
                'vendor_id': vendors[4].id,
                'vendor_name': vendors[4].name,
                'proposal_content': 'Comprehensive enterprise security solution with GDPR compliance, threat detection, and SOC 2 certification included.',
                'parsed_data': {
                    'proposal_summary': 'Enterprise security with compliance certifications',
                    'key_benefits': ['GDPR compliant', 'AI threat detection', 'SOC 2 certified']
                },
                'price': '380000.00',
                'delivery_time': '75 days',
                'warranty': '3 years',
                'payment_terms': '25% upfront, 50% mid-project, 25% completion',
                'status': 'EVALUATED',
                'score': 93.0,
                'evaluation': {
                    'technical_score': 94,
                    'cost_score': 92,
                    'timeline_score': 93,
                    'experience_score': 94,
                    'recommendation': 'Highly recommended - Excellent security posture'
                }
            },
        ]

        for proposal_data in proposals_data:
            proposal = Proposal.objects.create(**proposal_data)
            self.stdout.write(f'Created proposal from {proposal.vendor_name} for RFP {proposal.rfp_id}')

        self.stdout.write(self.style.SUCCESS('✅ Successfully seeded database with:'))
        self.stdout.write(self.style.SUCCESS(f'  • 5 Vendors'))
        self.stdout.write(self.style.SUCCESS(f'  • 5 RFPs'))
        self.stdout.write(self.style.SUCCESS(f'  • 5 Proposals'))
        self.stdout.write(self.style.SUCCESS('Data seeding completed!'))
