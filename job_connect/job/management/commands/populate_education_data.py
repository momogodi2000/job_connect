from django.core.management.base import BaseCommand
from job.models import Domain, Specification, EducationalLevel

class Command(BaseCommand):
    help = 'Populate the database with education and work domain data'

    def handle(self, *args, **kwargs):
        self.populate()

    def populate(self):
        data = {
            "Information Technology (IT)": [
                "Software development (web, mobile, desktop)",
                "Network engineering (systems, security)",
                "Database administration",
                "Cybersecurity (threat analysis, incident response)",
                "Cloud computing (infrastructure, platforms, software)",
                "Data analytics (business intelligence, machine learning)",
                "Artificial intelligence (natural language processing, computer vision)",
                "Systems administration (server management, troubleshooting)",
                "Technical support (help desk, customer service)",
                "IT project management"
            ],
            "Healthcare": [
                "Medicine (internal medicine, pediatrics, surgery)",
                "Nursing (registered nurses, licensed practical nurses)",
                "Dentistry",
                "Pharmacy",
                "Physical therapy",
                "Occupational therapy",
                "Speech therapy",
                "Radiology (radiologists, technicians)",
                "Medical laboratory science",
                "Public health (epidemiology, health policy)"
            ],
            "Education": [
                "Teaching (elementary, secondary, higher education)",
                "School administration (principals, counselors)",
                "Curriculum development",
                "Educational psychology",
                "Special education",
                "Educational technology",
                "Adult education",
                "Library science",
                "Early childhood education",
                "Distance education"
            ],
            "Business and Finance": [
                "Accounting (public accounting, corporate accounting)",
                "Finance (investment banking, financial analysis)",
                "Marketing (marketing research, brand management)",
                "Sales (sales management, customer service)",
                "Human resources (recruitment, employee relations)",
                "Management (general management, project management)",
                "Economics",
                "Law (corporate law, tax law)",
                "Business administration",
                "Entrepreneurship"
            ],
            "Engineering": [
                "Civil engineering (structural, transportation)",
                "Mechanical engineering (design, manufacturing)",
                "Electrical engineering (power systems, electronics)",
                "Chemical engineering (process design, materials science)",
                "Industrial engineering (operations management, quality control)",
                "Biomedical engineering",
                "Environmental engineering",
                "Aerospace engineering",
                "Computer engineering",
                "Petroleum engineering"
            ],
            "Law Enforcement and Public Safety": [
                "Law enforcement (police officers, detectives)",
                "Firefighting",
                "Emergency medical services (paramedics)",
                "Corrections (prison guards, probation officers)",
                "Homeland security",
                "Private security",
                "Legal services (attorneys, paralegals)",
                "Forensics (crime scene investigation)",
                "Cybersecurity (digital forensics)",
                "Intelligence analysis"
            ],
            "Arts and Entertainment": [
                "Visual arts (painting, sculpture, photography)",
                "Performing arts (music, theater, dance)",
                "Writing (creative writing, journalism)",
                "Design (graphic design, interior design)",
                "Film and television (production, acting)",
                "Animation",
                "Video game development",
                "Architecture",
                "Event planning",
                "Arts administration"
            ],
            "Government and Public Service": [
                "Public administration",
                "International relations",
                "Diplomacy",
                "Social work",
                "Urban planning",
                "Environmental policy",
                "Education administration",
                "Public health administration",
                "Economic development",
                "Political science"
            ],
            "Science and Research": [
                "Biology (genetics, ecology)",
                "Chemistry",
                "Physics",
                "Mathematics",
                "Geology",
                "Astronomy",
                "Psychology",
                "Sociology",
                "Environmental science",
                "Research administration"
            ]
        }

 # New educational levels to be added
        educational_levels = [
            "A-Level (Advanced Level)",
            "HND",
            "Bachelor's Degree",
            "Common Degrees",
            "Master's Degree",
            "Doctoral Degree",
            "Professor Degree"
        ]

        for domain_name, specifications in data.items():
            domain, created = Domain.objects.get_or_create(name=domain_name)

            for spec in specifications:
                Specification.objects.get_or_create(name=spec, domain=domain)

        self.stdout.write(self.style.SUCCESS('Education and work domains populated successfully'))

 # Populate educational levels
        for level in educational_levels:
            EducationalLevel.objects.get_or_create(level=level)

        self.stdout.write(self.style.SUCCESS('Education and work domains populated successfully, along with educational levels.'))