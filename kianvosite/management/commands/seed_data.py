from django.core.management.base import BaseCommand
from kianvosite.models import (
    ProjectCategory, Project, Service, CompanyStat,
    BlogCategory, BlogPost, Testimonial
)


class Command(BaseCommand):
    help = 'Seed the database with initial KianvoSoft data'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')

        # Create Project Categories
        categories = [
            {'name': 'Healthcare', 'slug': 'healthcare', 'icon_class': 'flaticon-consultant', 'order': 1},
            {'name': 'Retail & POS', 'slug': 'retail-pos', 'icon_class': 'flaticon-software-development', 'order': 2},
            {'name': 'Transport', 'slug': 'transport', 'icon_class': 'flaticon-mobile-phone-1', 'order': 3},
            {'name': 'Agriculture', 'slug': 'agriculture', 'icon_class': 'flaticon-web-research', 'order': 4},
            {'name': 'Education', 'slug': 'education', 'icon_class': 'flaticon-data-scientist', 'order': 5},
            {'name': 'Hospitality', 'slug': 'hospitality', 'icon_class': 'flaticon-cyber-security', 'order': 6},
            {'name': 'Real Estate', 'slug': 'real-estate', 'icon_class': 'flaticon-computer-mouse', 'order': 7},
        ]

        for cat_data in categories:
            ProjectCategory.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
        self.stdout.write(self.style.SUCCESS(f'Created {len(categories)} project categories'))

        # Create Projects
        projects = [
            {
                'name': 'Imforia',
                'slug': 'imforia',
                'tagline': 'Pharmacy Management System',
                'description': 'Complete solution for pharmacy inventory, sales, prescription management, and reporting. Streamlines pharmacy operations with automated stock tracking and sales analytics.',
                'full_description': '''Imforia is a comprehensive Pharmacy Management System designed to streamline all aspects of pharmacy operations.

Key capabilities include:
- Complete inventory management with automated stock alerts
- Prescription management and tracking
- Point of Sale (POS) with receipt printing
- Customer management and purchase history
- Supplier management and purchase orders
- Expiry date tracking and alerts
- Comprehensive sales and inventory reports
- Multi-branch support
- User role management and access control''',
                'category_slug': 'healthcare',
                'technologies': 'Django, React, PostgreSQL, REST API',
                'features': '''Inventory Management\nPrescription Tracking\nPOS System\nCustomer Management\nSupplier Management\nExpiry Alerts\nSales Reports\nMulti-branch Support''',
                'icon_class': 'flaticon-consultant',
                'status': 'completed',
                'is_featured': True,
                'order': 1,
            },
            {
                'name': 'MjenziPOS',
                'slug': 'mjenzipos',
                'tagline': 'Hardware Shop Management System',
                'description': 'POS and inventory tracking system designed specifically for hardware stores. Manages sales, inventory, and provides detailed analytics for hardware retail businesses.',
                'full_description': '''MjenziPOS is a specialized Point of Sale and inventory management system built for hardware shops and building material stores.

Features include:
- Quick product search and barcode scanning
- Inventory management with unit conversions
- Credit sales and customer accounts
- Supplier management
- Purchase order generation
- Daily, weekly, and monthly reports
- Profit margin analysis
- Low stock alerts
- Multi-user support with role-based access''',
                'category_slug': 'retail-pos',
                'technologies': 'Django, Vue.js, MySQL, Bootstrap',
                'features': '''Point of Sale\nBarcode Scanning\nInventory Tracking\nCredit Sales\nCustomer Accounts\nPurchase Orders\nSales Analytics\nLow Stock Alerts''',
                'icon_class': 'flaticon-software-development',
                'status': 'completed',
                'is_featured': True,
                'order': 2,
            },
            {
                'name': 'Transit',
                'slug': 'transit',
                'tagline': 'Transit Company Operations & Maintenance System',
                'description': 'Fleet management and maintenance scheduling system for transit companies. Tracks vehicles, schedules maintenance, and optimizes routes for efficient operations.',
                'full_description': '''Transit is a comprehensive fleet management system designed for bus companies and transit operators.

System capabilities:
- Vehicle fleet management
- Driver management and scheduling
- Route planning and optimization
- Maintenance scheduling and tracking
- Fuel consumption monitoring
- Trip logging and reporting
- Revenue tracking per route/vehicle
- Real-time vehicle status
- Accident and incident reporting''',
                'category_slug': 'transport',
                'technologies': 'Python, Flutter, Firebase, Google Maps API',
                'features': '''Fleet Management\nDriver Scheduling\nRoute Optimization\nMaintenance Tracking\nFuel Monitoring\nTrip Logging\nRevenue Reports\nIncident Reporting''',
                'icon_class': 'flaticon-mobile-phone-1',
                'status': 'completed',
                'is_featured': True,
                'order': 3,
            },
            {
                'name': 'Land Allocation System',
                'slug': 'land-allocation-system',
                'tagline': 'Land Plot & Farmer Data Management',
                'description': 'Track land plots and manage farmer/applicant data for agricultural departments. Includes mapping, allocation tracking, and comprehensive reporting.',
                'full_description': '''The Land Allocation System helps agricultural departments manage land distribution and farmer data efficiently.

Key features:
- Land plot registration and mapping
- Farmer/applicant registration
- Application processing workflow
- Land allocation tracking
- Document management
- GIS integration for plot visualization
- Allocation history and audit trail
- Comprehensive reporting
- Multi-district support''',
                'category_slug': 'agriculture',
                'technologies': 'Django, React, PostGIS, Leaflet',
                'features': '''Plot Registration\nFarmer Management\nApplication Workflow\nGIS Mapping\nDocument Storage\nAllocation Tracking\nAudit Trail\nReporting Dashboard''',
                'icon_class': 'flaticon-web-research',
                'status': 'completed',
                'is_featured': False,
                'order': 4,
            },
            {
                'name': 'Asset Management System',
                'slug': 'asset-management-system',
                'tagline': 'University Indoor Asset Management',
                'description': 'Manage university indoor assets including tracking, maintenance scheduling, and inventory control for educational institutions.',
                'full_description': '''A comprehensive asset management system designed for universities to track and manage their indoor assets.

Capabilities include:
- Asset registration and tagging
- Location tracking by building/room
- Maintenance scheduling
- Asset condition monitoring
- Depreciation calculation
- Asset transfer between departments
- Disposal management
- Barcode/QR code integration
- Audit and inventory reports''',
                'category_slug': 'education',
                'technologies': 'Django, Bootstrap, SQLite, jQuery',
                'features': '''Asset Registration\nLocation Tracking\nMaintenance Scheduling\nCondition Monitoring\nDepreciation Tracking\nAsset Transfers\nBarcode Support\nInventory Reports''',
                'icon_class': 'flaticon-database',
                'status': 'completed',
                'is_featured': False,
                'order': 5,
            },
            {
                'name': 'Mashfly',
                'slug': 'mashfly',
                'tagline': 'Restaurant Management System',
                'description': 'Complete restaurant management solution including orders, kitchen display, inventory control, and detailed business reporting.',
                'full_description': '''Mashfly is an all-in-one restaurant management system that streamlines operations from order taking to kitchen management.

Features:
- Table management and reservations
- Order management (dine-in, takeaway, delivery)
- Kitchen Display System (KDS)
- Inventory and recipe management
- Menu management with modifiers
- Split bills and payment processing
- Staff management and shifts
- Sales and inventory reports
- Customer loyalty program''',
                'category_slug': 'hospitality',
                'technologies': 'Node.js, React, MongoDB, Socket.io',
                'features': '''Table Management\nOrder System\nKitchen Display\nInventory Control\nMenu Management\nSplit Bills\nStaff Management\nLoyalty Program''',
                'icon_class': 'flaticon-cyber-security',
                'status': 'completed',
                'is_featured': True,
                'order': 6,
            },
            {
                'name': 'NyumbaYangu',
                'slug': 'nyumbayangu',
                'tagline': 'Tenant & Landlord Management System',
                'description': 'Platform linking tenants and landlords for property rentals. Manages listings, applications, rent collection, and maintenance requests.',
                'full_description': '''NyumbaYangu is a comprehensive property rental management platform connecting tenants and landlords.

Platform features:
- Property listing and search
- Tenant application processing
- Lease agreement management
- Rent payment tracking and reminders
- Maintenance request handling
- Communication portal
- Document storage
- Payment history and receipts
- Property inspection scheduling''',
                'category_slug': 'real-estate',
                'technologies': 'Django, React Native, PostgreSQL, Stripe',
                'features': '''Property Listings\nTenant Applications\nLease Management\nRent Collection\nMaintenance Requests\nMessaging Portal\nPayment Tracking\nMobile Apps''',
                'icon_class': 'flaticon-computer-mouse',
                'status': 'completed',
                'is_featured': True,
                'order': 7,
            },
            {
                'name': 'SPARKS',
                'slug': 'sparks',
                'tagline': 'Student Progress & Academic Records System',
                'description': 'Comprehensive academic management system for universities and colleges. Tracks student progress, grades, and academic records.',
                'full_description': '''SPARKS (Student Progress and Academic Records Keeping System) is designed for higher education institutions.

System modules:
- Student registration and enrollment
- Course management
- Class scheduling
- Grade entry and GPA calculation
- Academic transcript generation
- Attendance tracking
- Fee management integration
- Student portal
- Faculty portal
- Administrative dashboard''',
                'category_slug': 'education',
                'technologies': 'Django, Vue.js, PostgreSQL, Celery',
                'features': '''Student Registration\nCourse Management\nGrade Tracking\nTranscript Generation\nAttendance System\nStudent Portal\nFaculty Portal\nFee Integration''',
                'icon_class': 'flaticon-data-scientist',
                'status': 'completed',
                'is_featured': True,
                'order': 8,
            },
            {
                'name': 'eLearning',
                'slug': 'elearning',
                'tagline': 'University Virtual Learning System',
                'description': 'Online learning platform for universities featuring courses, assessments, virtual classrooms, and student engagement tools.',
                'full_description': '''A comprehensive eLearning platform designed for university virtual education.

Platform capabilities:
- Course content management
- Video lectures and live streaming
- Online assessments and quizzes
- Assignment submission and grading
- Discussion forums
- Virtual classroom integration
- Progress tracking
- Certificate generation
- Mobile-responsive design
- Analytics dashboard''',
                'category_slug': 'education',
                'technologies': 'Django, React, AWS, WebRTC',
                'features': '''Course Management\nVideo Lectures\nOnline Assessments\nAssignment Submission\nDiscussion Forums\nVirtual Classrooms\nProgress Tracking\nCertificates''',
                'icon_class': 'flaticon-cloud-computing',
                'status': 'completed',
                'is_featured': True,
                'order': 9,
            },
        ]

        for proj_data in projects:
            category_slug = proj_data.pop('category_slug')
            category = ProjectCategory.objects.filter(slug=category_slug).first()

            Project.objects.get_or_create(
                slug=proj_data['slug'],
                defaults={**proj_data, 'category': category}
            )
        self.stdout.write(self.style.SUCCESS(f'Created {len(projects)} projects'))

        # Create Services
        services = [
            {
                'name': 'Custom Software Development',
                'slug': 'custom-software-development',
                'short_description': 'Build scalable, secure software tailored to your business needs.',
                'description': 'We develop custom software solutions that address your unique business challenges. From enterprise systems to desktop applications, we deliver high-quality, maintainable code.',
                'icon_class': 'flaticon-software-development',
                'features': 'Enterprise Software\nDesktop Applications\nDatabase Solutions\nAPI Development\nSystem Integration',
                'technologies': 'Python, Django, .NET, Java, C++',
                'is_featured': True,
                'order': 1,
            },
            {
                'name': 'Web Application Development',
                'slug': 'web-application-development',
                'short_description': 'Modern, responsive web applications using latest technologies.',
                'description': 'We create powerful web applications with intuitive user interfaces. Our solutions are responsive, secure, and optimized for performance.',
                'icon_class': 'flaticon-web-research',
                'features': 'Frontend Development\nBackend Development\nE-commerce Solutions\nProgressive Web Apps\nCMS Development',
                'technologies': 'React, Vue.js, Django, Node.js, PHP',
                'is_featured': True,
                'order': 2,
            },
            {
                'name': 'Mobile App Development',
                'slug': 'mobile-app-development',
                'short_description': 'Native and cross-platform apps for Android and iOS.',
                'description': 'We build mobile applications that deliver exceptional user experiences. Whether native or cross-platform, our apps are fast, reliable, and user-friendly.',
                'icon_class': 'flaticon-mobile-phone-1',
                'features': 'Android Apps\niOS Apps\nCross-Platform Apps\nApp Maintenance\nApp Store Optimization',
                'technologies': 'Flutter, React Native, Kotlin, Swift',
                'is_featured': True,
                'order': 3,
            },
            {
                'name': 'AI & Machine Learning',
                'slug': 'ai-machine-learning',
                'short_description': 'Intelligent solutions powered by AI and ML algorithms.',
                'description': 'Leverage artificial intelligence to automate processes and gain insights. We develop custom AI solutions including predictive analytics, NLP, and computer vision.',
                'icon_class': 'flaticon-data-scientist',
                'features': 'Predictive Analytics\nNatural Language Processing\nComputer Vision\nRecommendation Systems\nChatbots',
                'technologies': 'Python, TensorFlow, PyTorch, Scikit-learn',
                'is_featured': True,
                'order': 4,
            },
            {
                'name': 'Automation Systems',
                'slug': 'automation-systems',
                'short_description': 'Streamline operations with intelligent automation.',
                'description': 'We help businesses automate repetitive tasks and optimize workflows. Our automation solutions reduce manual work and minimize errors.',
                'icon_class': 'flaticon-computer-mouse',
                'features': 'Business Process Automation\nWorkflow Optimization\nRPA Solutions\nIntegration Services\nReport Automation',
                'technologies': 'Python, Selenium, Power Automate, REST APIs',
                'is_featured': True,
                'order': 5,
            },
            {
                'name': 'IT Consulting & Support',
                'slug': 'it-consulting-support',
                'short_description': 'Expert guidance for your technology decisions.',
                'description': 'Our IT consulting services help you make informed technology decisions. We provide strategic planning, security assessments, and ongoing technical support.',
                'icon_class': 'flaticon-consultant',
                'features': 'Technology Strategy\nSecurity Assessment\nTechnical Support\nSystem Audits\nTraining',
                'technologies': 'Various technologies based on client needs',
                'is_featured': True,
                'order': 6,
            },
        ]

        for svc_data in services:
            Service.objects.get_or_create(
                slug=svc_data['slug'],
                defaults=svc_data
            )
        self.stdout.write(self.style.SUCCESS(f'Created {len(services)} services'))

        # Create Company Statistics
        stats = [
            {'name': 'Projects Completed', 'value': 50, 'suffix': '+', 'order': 1},
            {'name': 'Happy Clients', 'value': 30, 'suffix': '+', 'order': 2},
            {'name': 'Client Satisfaction', 'value': 95, 'suffix': '%', 'order': 3},
            {'name': 'Years Experience', 'value': 5, 'suffix': '+', 'order': 4},
        ]

        for stat_data in stats:
            CompanyStat.objects.get_or_create(
                name=stat_data['name'],
                defaults=stat_data
            )
        self.stdout.write(self.style.SUCCESS(f'Created {len(stats)} company statistics'))

        # Create Blog Categories
        blog_categories = [
            {'name': 'AI & Technology', 'slug': 'ai-technology', 'icon_class': 'flaticon-data-scientist'},
            {'name': 'Web Development', 'slug': 'web-development', 'icon_class': 'flaticon-web-research'},
            {'name': 'Mobile Development', 'slug': 'mobile-development', 'icon_class': 'flaticon-mobile-phone-1'},
            {'name': 'Cloud & DevOps', 'slug': 'cloud-devops', 'icon_class': 'flaticon-cloud-computing'},
            {'name': 'Security', 'slug': 'security', 'icon_class': 'flaticon-cyber-security'},
        ]

        for cat_data in blog_categories:
            BlogCategory.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
        self.stdout.write(self.style.SUCCESS(f'Created {len(blog_categories)} blog categories'))

        self.stdout.write(self.style.SUCCESS('Database seeding completed successfully!'))
