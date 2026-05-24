from django.core.management.base import BaseCommand
from django.utils import timezone
from kianvosite.models import (
    ProjectCategory, Project, Service, CompanyStat,
    BlogCategory, BlogPost, Testimonial, TeamMember,
    Announcement, GalleryCategory, Partner, RoadmapMilestone,
    SocialLink
)


class Command(BaseCommand):
    help = 'Seed the database with initial KianvoSoft data'

    def add_arguments(self, parser):
        parser.add_argument(
            '--refresh-blog',
            action='store_true',
            help='Delete existing blog posts and re-seed with fresh HTML content',
        )

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')

        # Create Project Categories
        categories = [
            {'name': 'Education Technology', 'slug': 'edtech', 'icon_class': 'flaticon-database', 'order': 1},
            {'name': 'Healthcare', 'slug': 'healthcare', 'icon_class': 'flaticon-consultant', 'order': 2},
            {'name': 'Retail & POS', 'slug': 'retail-pos', 'icon_class': 'flaticon-software-development', 'order': 3},
            {'name': 'Transport & Logistics', 'slug': 'transport-logistics', 'icon_class': 'flaticon-mobile-phone-1', 'order': 4},
            {'name': 'Business & SME', 'slug': 'business-sme', 'icon_class': 'flaticon-web-research', 'order': 5},
            {'name': 'AI & Research', 'slug': 'ai-research', 'icon_class': 'flaticon-data-scientist', 'order': 6},
            {'name': 'Social Impact', 'slug': 'social-impact', 'icon_class': 'flaticon-cyber-security', 'order': 7},
        ]

        for cat_data in categories:
            ProjectCategory.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
        self.stdout.write(self.style.SUCCESS(f'Created {len(categories)} project categories'))

        # Create Projects (actual KianvoSoft products from the company profile)
        projects = [
            {
                'name': 'Imforia',
                'slug': 'imforia',
                'tagline': 'Pharmacy Management System — Live in Tanzanian Pharmacies',
                'description': 'A pharmacy management system designed to streamline stock, sales, and dispensing operations. Currently in live use by pharmacies in Tanzania.',
                'full_description': '''Imforia is a comprehensive Pharmacy Management System designed to streamline all aspects of pharmacy operations. Currently deployed and in active use by pharmacies across Tanzania.

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
                'name': 'Mjenzi',
                'slug': 'mjenzi',
                'tagline': 'POS & Inventory Management for Hardware Retailers',
                'description': 'A point-of-sale and inventory management system tailored for hardware and construction-supply retailers.',
                'full_description': '''Mjenzi is a specialized Point of Sale and inventory management system built for hardware shops and building material stores.

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
                'name': 'ShopManagerPro',
                'slug': 'shopmanagerpro',
                'tagline': 'Business Management System for SMEs',
                'description': 'A business management system tailored to the operational needs of small and medium-sized shops.',
                'full_description': '''ShopManagerPro is a comprehensive business management system designed for small and medium-sized shops.

Features include:
- Sales and purchase management
- Inventory tracking and stock alerts
- Customer management and loyalty
- Supplier and purchase order management
- Sales analytics and reports
- Expense tracking
- Multi-user access
- Receipt printing and invoicing''',
                'category_slug': 'business-sme',
                'technologies': 'Django, React, PostgreSQL',
                'features': '''Sales Management\nInventory Tracking\nCustomer Management\nSupplier Management\nSales Analytics\nExpense Tracking\nInvoicing\nMulti-user Access''',
                'icon_class': 'flaticon-web-research',
                'status': 'completed',
                'is_featured': True,
                'order': 3,
            },
            {
                'name': 'FleetLink',
                'slug': 'fleetlink',
                'tagline': 'Cargo Transport & Fleet Management System',
                'description': 'A cargo transport management system that supports logistics operators in coordinating fleets, consignments, and deliveries.',
                'full_description': '''FleetLink is a comprehensive cargo transport management system designed for logistics operators.

System capabilities:
- Fleet vehicle management
- Consignment and shipment tracking
- Driver management and scheduling
- Route planning and optimization
- Delivery confirmation and proof of delivery
- Fuel consumption monitoring
- Revenue tracking per vehicle/route
- Customer portal for shipment tracking
- Incident reporting''',
                'category_slug': 'transport-logistics',
                'technologies': 'Python, Flutter, Firebase, Google Maps API',
                'features': '''Fleet Management\nConsignment Tracking\nDriver Scheduling\nRoute Optimization\nDelivery Confirmation\nFuel Monitoring\nRevenue Reports\nCustomer Portal''',
                'icon_class': 'flaticon-mobile-phone-1',
                'status': 'completed',
                'is_featured': True,
                'order': 4,
            },
            {
                'name': 'Kianvo Meet',
                'slug': 'kianvo-meet',
                'tagline': 'Video Conferencing for East African Institutions',
                'description': 'A video conferencing platform purpose-built to support online learning, collaboration, and professional meetings within East African institutions.',
                'full_description': '''Kianvo Meet is a video conferencing platform purpose-built for the East African context.

Platform features:
- HD video and audio conferencing
- Virtual classrooms with screen sharing
- Meeting recording and playback
- Chat and collaboration tools
- Breakout rooms for group work
- Mobile-friendly interface
- Optimized for lower bandwidth environments
- Swahili language interface option
- No credit card required for basic use''',
                'category_slug': 'edtech',
                'technologies': 'WebRTC, React, Python, Docker',
                'features': '''HD Video Conferencing\nVirtual Classrooms\nScreen Sharing\nMeeting Recording\nBreakout Rooms\nChat Tools\nMobile Support\nLow Bandwidth Optimization''',
                'icon_class': 'flaticon-database',
                'status': 'completed',
                'is_featured': True,
                'order': 5,
            },
            {
                'name': 'Kianvo Classroom',
                'slug': 'kianvo-classroom',
                'tagline': 'Learning Management System for Universities',
                'description': 'A Learning Management System designed for East African universities, enabling course delivery, student engagement, assignments, and online assessment.',
                'full_description': '''Kianvo Classroom is a comprehensive Learning Management System built for East African higher education.

Platform capabilities:
- Course creation and content management
- Video lectures and multimedia support
- Online assessments and quizzes
- Assignment submission and grading
- Discussion forums and messaging
- Student progress tracking
- Gradebook and reporting
- Mobile-responsive design
- Integration with Kianvo Meet for live classes''',
                'category_slug': 'edtech',
                'technologies': 'Django, React, PostgreSQL, AWS',
                'features': '''Course Management\nVideo Lectures\nOnline Assessments\nAssignment Submission\nDiscussion Forums\nProgress Tracking\nGradebook\nMobile Responsive''',
                'icon_class': 'flaticon-cloud-computing',
                'status': 'completed',
                'is_featured': True,
                'order': 6,
            },
            {
                'name': 'HELP',
                'slug': 'help',
                'tagline': 'Health Education Learning Portal',
                'description': 'An online learning platform focused on widening access to quality health education and continuing professional development for healthcare workers.',
                'full_description': '''HELP (Health Education Learning Portal) is an online learning platform designed for healthcare professionals.

Features:
- CPD-accredited health education courses
- Interactive learning modules
- Video lectures from medical experts
- Self-assessment quizzes
- Progress tracking and certificates
- Mobile-friendly access
- Offline learning capability
- Discussion forums for peer learning''',
                'category_slug': 'edtech',
                'technologies': 'Django, React, PostgreSQL, WebRTC',
                'features': '''Health Education Courses\nCPD Accreditation\nInteractive Modules\nVideo Lectures\nSelf-assessment\nProgress Tracking\nCertificates\nMobile Access''',
                'icon_class': 'flaticon-data-scientist',
                'status': 'completed',
                'is_featured': True,
                'order': 7,
            },
            {
                'name': 'IMS',
                'slug': 'ims',
                'tagline': 'Impact Management System',
                'description': 'A platform that helps organisations plan, monitor, and report on the social and developmental impact of their work.',
                'full_description': '''IMS (Impact Management System) is a platform designed for organisations to manage their social impact.

Platform capabilities:
- Impact goal setting and planning
- Indicator tracking and monitoring
- Beneficiary data management
- Survey and feedback collection
- Impact reporting and dashboards
- Grant and project management
- Stakeholder engagement tools
- Data visualization and export''',
                'category_slug': 'social-impact',
                'technologies': 'Django, Vue.js, PostgreSQL, Chart.js',
                'features': '''Impact Planning\nIndicator Tracking\nBeneficiary Management\nSurvey Collection\nImpact Reporting\nGrant Management\nDashboards\nData Export''',
                'icon_class': 'flaticon-cyber-security',
                'status': 'completed',
                'is_featured': True,
                'order': 8,
            },
            {
                'name': 'Brain Stroke Lesion Detection',
                'slug': 'brain-stroke-lesion-detection',
                'tagline': 'AI-Powered Stroke Diagnosis from Medical Imaging',
                'description': 'An active research project applying artificial intelligence to support faster and more accessible stroke diagnosis in low-resource hospital settings.',
                'full_description': '''Brain Stroke Lesion Detection is an active applied research project that uses artificial intelligence to analyze medical imaging and support faster stroke diagnosis.

Research focus:
- Deep learning models for CT/MRI lesion segmentation
- Automated detection of ischemic and hemorrhagic strokes
- Low-resource hospital deployment strategy
- Integration with existing medical imaging workflows
- Collaboration with Tanzanian healthcare facilities
- Published findings in peer-reviewed venues

Long-term goal: Reduce diagnosis time and improve outcomes for stroke patients in rural and low-resource settings across East Africa.''',
                'category_slug': 'ai-research',
                'technologies': 'Python, TensorFlow, PyTorch, OpenCV, Medical Imaging',
                'features': '''CT/MRI Analysis\nLesion Segmentation\nDeep Learning Models\nLow-resource Focus\nClinical Collaboration\nPeer-reviewed Publication''',
                'icon_class': 'flaticon-web-research',
                'status': 'in_progress',
                'is_featured': True,
                'order': 9,
            },
            {
                'name': 'Automated Malaria Detection',
                'slug': 'automated-malaria-detection',
                'tagline': 'AI-Powered Malaria Parasite Identification',
                'description': 'Applied research on the automated identification of malaria parasites in blood samples using AI-powered image analysis.',
                'full_description': '''Automated Malaria Detection is an applied research project using computer vision and AI to identify malaria parasites in blood smear images.

Research focus:
- Computer vision models for parasite detection
- Classification of malaria species and stages
- Parasitemia quantification
- Mobile microscopy integration
- Deployment in rural health facilities
- Partnership with Tanzanian health institutions

Long-term goal: Strengthen diagnostic capacity in rural health facilities where access to trained microscopists is limited.''',
                'category_slug': 'ai-research',
                'technologies': 'Python, TensorFlow, PyTorch, OpenCV, Flask',
                'features': '''Parasite Detection\nSpecies Classification\nParasitemia Quantification\nMobile Microscopy\nRural Health Focus\nResearch Partnership''',
                'icon_class': 'flaticon-consultant',
                'status': 'in_progress',
                'is_featured': True,
                'order': 10,
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

        # Future Vision Services
        future_visions = [
            {
                'name': 'KianvoSoft Academy',
                'slug': 'academy',
                'service_type': 'future',
                'short_description': 'A fully-fledged technology academy offering certified diploma programmes.',
                'description': 'Our medium-term goal is to establish the KianvoSoft Academy — a fully-fledged technology training institution offering certified diploma programmes in software engineering, AI, and data science.',
                'icon_class': 'flaticon-database',
                'features': 'Certified Diploma Programmes\nSoftware Engineering Track\nAI & Data Science Track\nIndustry-aligned Curriculum\nInternship Placements\nSwahili & English Instruction',
                'technologies': 'Comprehensive technology curriculum',
                'timeline_text': '2027–2028',
                'is_featured': True,
                'order': 5,
            },
            {
                'name': 'SaaS Product Suite',
                'slug': 'saas-products',
                'service_type': 'future',
                'short_description': 'Subscription-based software products for East African businesses.',
                'description': 'We are building towards a suite of subscription-based SaaS products that will make enterprise-grade software accessible and affordable for East African SMEs.',
                'icon_class': 'flaticon-cloud-computing',
                'features': 'Subscription-based Pricing\nCloud-hosted Platforms\nAutomatic Updates\nCustomer Support Included\nScalable Infrastructure\nEast Africa Focus',
                'technologies': 'Cloud infrastructure, scalable microservices',
                'timeline_text': '2028–2029',
                'is_featured': True,
                'order': 6,
            },
        ]

        for vision_data in future_visions:
            Service.objects.get_or_create(
                slug=vision_data['slug'],
                defaults=vision_data
            )
        self.stdout.write(self.style.SUCCESS(f'Created {len(future_visions)} future vision services'))

        # Create Team Members
        team_members = [
            {
                'name': 'Datius Rweyemamu Daud',
                'role': 'Director of Research & AI',
                'bio': 'Leads applied AI research, academic partnerships with MUST and other institutions, publications, and training programme design. Also handles research ethics and data governance.',
                'icon_class': 'fas fa-user-graduate',
                'order': 1,
            },
            {
                'name': 'Akila Body Joseph',
                'role': 'Director of Product & Engineering',
                'bio': 'Leads product management, software engineering, quality assurance, technical infrastructure, and client technical support. Oversees development of all KianvoSoft products.',
                'icon_class': 'fas fa-laptop-code',
                'order': 2,
            },
            {
                'name': 'Aneth Alphonce Seleli',
                'role': 'Director of Business & Operations',
                'bio': 'Leads business development, finance, HR, marketing, legal and compliance, and institutional relationships with CITT, MUST, and government bodies.',
                'icon_class': 'fas fa-chart-line',
                'order': 3,
            },
        ]

        for tm_data in team_members:
            TeamMember.objects.get_or_create(
                name=tm_data['name'],
                defaults=tm_data
            )
        self.stdout.write(self.style.SUCCESS(f'Created {len(team_members)} team members'))

        # Create Services (Four Pillars — Current)
        services = [
            {
                'name': 'Software Product Development',
                'slug': 'software',
                'service_type': 'current',
                'short_description': 'Designing and deploying software products for education, healthcare, and business.',
                'description': 'We design and deploy software products that solve real problems for institutions, businesses, and communities. Our current focus includes education technology platforms (Kianvo Meet, Kianvo Classroom, HELP), healthcare systems (Imforia), and business tools (Mjenzi, ShopManagerPro, FleetLink, IMS).',
                'icon_class': 'flaticon-software-development',
                'features': 'Education Technology Platforms\nHealthcare Management Systems\nBusiness & Operations Software\nPOS & Inventory Solutions\nLogistics & Transport Systems\nImpact Management Platforms',
                'technologies': 'React, Django, Flutter, Python, Node.js, PostgreSQL',
                'is_featured': True,
                'order': 1,
            },
            {
                'name': 'Technical Training & Capacity Building',
                'slug': 'training',
                'service_type': 'current',
                'short_description': 'Short courses, bootcamps, and coding camps in modern technologies.',
                'description': 'We deliver short courses, bootcamps, and coding camps in modern programming languages, frameworks, and emerging technologies for students and working professionals. Training is delivered in Swahili and English.',
                'icon_class': 'flaticon-consultant',
                'features': 'Programming Fundamentals\nWeb & Mobile Development Bootcamps\nAI & Machine Learning Workshops\nShort Courses for Professionals\nSwahili & English Delivery\nProject-based Learning',
                'technologies': 'Python, JavaScript, Dart, Flutter, React, Django',
                'is_featured': True,
                'order': 2,
            },
            {
                'name': 'Applied AI Research',
                'slug': 'research',
                'service_type': 'current',
                'short_description': 'Active research in AI for health, business, and the environment.',
                'description': 'We conduct applied AI research with practical contributions to challenges in health, business, and the environment affecting the East African region. Active projects include brain stroke lesion detection and automated malaria detection.',
                'icon_class': 'flaticon-data-scientist',
                'features': 'Medical Imaging AI (Stroke Detection)\nComputer Vision (Malaria Detection)\nAcademic Research Partnerships\nPeer-reviewed Publications\nResearch Ethics & Data Governance',
                'technologies': 'Python, TensorFlow, PyTorch, OpenCV, Medical Imaging',
                'is_featured': True,
                'order': 3,
            },
            {
                'name': 'Technology Consultancy & Outreach',
                'slug': 'consulting',
                'service_type': 'current',
                'short_description': 'Consultancy for SMEs, NGOs, and institutions undertaking digital transformation.',
                'description': 'We offer consultancy services to SMEs, NGOs, and institutions undertaking digital transformation, and run outreach programmes to inspire the next generation of African technologists.',
                'icon_class': 'flaticon-satellite-signal',
                'features': 'Digital Transformation Strategy\nTechnology Needs Assessment\nSystem Integration & Modernisation\nIT Infrastructure Advisory\nCommunity Outreach Programmes\nUniversity & Innovation Partnerships',
                'technologies': 'Various technologies based on client needs',
                'is_featured': True,
                'order': 4,
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

        # Blog Posts — HTML content (CKEditor-compatible) — focused on KianvoSoft's mission
        blog_posts = [
            {
                'title': 'How Tanzanian Startups Are Leading Africa\'s AI Revolution',
                'slug': 'tanzanian-startups-ai-revolution',
                'excerpt': 'Discover how Tanzanian technology ventures are driving AI innovation in health, agriculture, and business across East Africa.',
                'category_slug': 'ai-technology',
                'author': 'Datius Rweyemamu Daud',
                'is_featured': True,
                'is_published': True,
                'content': """<p>Tanzania is emerging as a surprising hub for artificial intelligence innovation. While global attention focuses on Nairobi, Lagos, and Cape Town, a new generation of Tanzanian technologists is building AI solutions tailored to local challenges. Here&rsquo;s how Tanzanian startups are leading Africa&rsquo;s AI revolution.</p>

<h2>AI for Healthcare in Low-Resource Settings</h2>
<p>One of the most impactful areas of AI research in Tanzania is healthcare. With a doctor-to-patient ratio of less than 1:10,000 in rural areas, AI-powered diagnostic tools are not a luxury &mdash; they are a necessity.</p>
<p>At KianvoSoft, our research projects in brain stroke lesion detection and automated malaria detection are examples of how AI can be applied to strengthen diagnostic capacity where it&rsquo;s needed most. By training deep learning models on medical imaging data, we aim to reduce diagnosis time and improve outcomes for patients in low-resource hospital settings.</p>

<h2>Agriculture AI for Smallholder Farmers</h2>
<p>Agriculture employs over 65% of Tanzania&rsquo;s workforce. AI applications in this sector include crop disease detection using computer vision, weather prediction models for planting decisions, and market price optimization for smallholder farmers.</p>

<h2>Swahili Language AI</h2>
<p>One of the most exciting frontiers is Swahili-language AI. With over 200 million speakers across East Africa, there is enormous potential for NLP models that understand Swahili. Tanzanian startups are beginning to build chatbots, voice assistants, and translation tools that work in Swahili &mdash; reaching populations that English-only technology cannot serve.</p>

<h2>The University Pipeline</h2>
<p>Institutions like the Mbeya University of Science and Technology (MUST) are producing a growing pipeline of AI talent. KianvoSoft itself was founded by MUST computer engineering students who identified the gap between academic research and real-world deployment.</p>

<h2>Challenges &amp; Opportunities</h2>
<ul>
    <li><strong>Data availability</strong> &mdash; Limited structured datasets for training AI models</li>
    <li><strong>Computing infrastructure</strong> &mdash; Access to GPUs and cloud computing remains expensive</li>
    <li><strong>Talent retention</strong> &mdash; Keeping skilled AI researchers in Tanzania</li>
    <li><strong>Funding</strong> &mdash; Early-stage AI research needs more local investment</li>
</ul>

<h2>The Future</h2>
<p>Tanzania&rsquo;s AI ecosystem is small but growing fast. With the right investment in data infrastructure, computing resources, and talent development, Tanzanian startups are well-positioned to lead Africa&rsquo;s next wave of AI innovation.</p>

<p>At KianvoSoft, we&rsquo;re proud to contribute to this movement. <a href="/contact/">Contact us</a> to learn more about our AI research initiatives.</p>""",
            },
            {
                'title': 'Building EdTech for East Africa: Lessons from Mbeya',
                'slug': 'building-edtech-east-africa-mbeya',
                'excerpt': 'What we learned building Kianvo Classroom, Kianvo Meet, and HELP for East African educational institutions.',
                'category_slug': 'web-development',
                'author': 'Akila Body Joseph',
                'is_featured': True,
                'is_published': True,
                'content': """<p>When we set out to build education technology platforms at KianvoSoft, we quickly realised that importing solutions built for Western contexts simply doesn&rsquo;t work in East Africa. Here are the key lessons from building Kianvo Classroom, Kianvo Meet, and HELP from Mbeya, Tanzania.</p>

<h2>Lesson 1: Bandwidth Is Still a Constraint</h2>
<p>While internet penetration in Tanzania has grown significantly, many universities and students still face unreliable connectivity. Our platforms are designed to work with low bandwidth, including offline-capable features, compressed video streaming, and progressive loading. We optimise for 3G connections, not just fibre.</p>

<h2>Lesson 2: Mobile-First Is Non-Negotiable</h2>
<p>In East Africa, most users access the internet through smartphones. Our platforms are built mobile-first, with intuitive touch interfaces and data-light designs. We test on mid-range Android devices because that&rsquo;s what most students and teachers actually use.</p>

<h2>Lesson 3: Swahili Matters</h2>
<p>While English is the official language of instruction in Tanzanian universities, many students and teachers are more comfortable in Swahili. Kianvo Classroom and Kianvo Meet offer Swahili-language interfaces, making technology more accessible to a wider population.</p>

<h2>Lesson 4: Assessment Needs to Work Offline</h2>
<p>During exams, network congestion can be catastrophic. Our assessment modules allow students to download questions, complete answers offline, and sync when connectivity returns. This simple feature has been a game-changer for our university partners.</p>

<h2>Lesson 5: Local Support Is Essential</h2>
<p>Having a support team that understands the local context, speaks the language, and can visit institutions in person is irreplaceable. Being based in Mbeya means we can provide hands-on support that international EdTech platforms cannot match.</p>

<h2>Our EdTech Portfolio</h2>
<ul>
    <li><strong>Kianvo Classroom</strong> &mdash; Learning Management System for universities</li>
    <li><strong>Kianvo Meet</strong> &mdash; Video conferencing for education</li>
    <li><strong>HELP</strong> &mdash; Health Education Learning Portal for CPD</li>
</ul>
<p>Each platform is built for East Africa, by East Africans.</p>

<p>Interested in our EdTech solutions? <a href="/contact/">Get in touch</a> to discuss your institution&rsquo;s needs.</p>""",
            },
            {
                'title': 'AI-Powered Malaria Detection: A Tanzanian Research Journey',
                'slug': 'ai-malaria-detection-tanzania',
                'excerpt': 'How we are applying computer vision to strengthen malaria diagnostic capacity in rural Tanzanian health facilities.',
                'category_slug': 'ai-technology',
                'author': 'Datius Rweyemamu Daud',
                'is_featured': True,
                'is_published': True,
                'content': """<p>Malaria remains one of Tanzania&rsquo;s most persistent public health challenges, with over 10 million cases reported annually. While diagnosis traditionally relies on microscopy, many rural health facilities lack trained microscopists. Our applied AI research project aims to change that.</p>

<h2>The Problem</h2>
<p>In rural Tanzanian health facilities, malaria diagnosis typically relies on rapid diagnostic tests (RDTs) or microscopy. RDTs are quick but can miss low-density infections. Microscopy is more accurate but requires trained personnel who are often unavailable in rural areas. The result: misdiagnosis, delayed treatment, and poor patient outcomes.</p>

<h2>Our Approach</h2>
<p>We are developing a computer vision system that can automatically identify malaria parasites in blood smear images. Using deep learning models trained on thousands of labelled microscopy images, our system can:</p>
<ul>
    <li>Detect the presence of malaria parasites</li>
    <li>Classify the species (P. falciparum, P. vivax, etc.)</li>
    <li>Quantify parasitemia (parasite density)</li>
    <li>Identify the stage of infection</li>
</ul>

<h2>Technical Challenges</h2>
<ul>
    <li><strong>Data acquisition</strong> &mdash; Collecting high-quality labelled microscopy images from Tanzanian health facilities</li>
    <li><strong>Variable image quality</strong> &mdash; Models must work with images from basic microscopes and phone cameras</li>
    <li><strong>Class imbalance</strong> &mdash; Negative samples vastly outnumber positive ones</li>
    <li><strong>Deployment</strong> &mdash; Models must run on low-cost hardware available in rural settings</li>
</ul>

<h2>Progress So Far</h2>
<p>Our initial models have achieved promising accuracy in detecting P. falciparum &mdash; the most common malaria species in Tanzania. We are now working on improving sensitivity for low-density infections and expanding our dataset with samples from multiple health facilities.</p>

<h2>Partnerships</h2>
<p>This research is conducted in collaboration with academic partners at Mbeya University of Science and Technology (MUST) and supported by the Centre for Innovation Technology Transfer (CITT). We welcome collaboration from health institutions and research partners.</p>

<p>Interested in our AI for Health research? <a href="/contact/">Contact us</a> to learn more or collaborate.</p>""",
            },
            {
                'title': 'Imforia: How We Built a Pharmacy System for Tanzanian Pharmacies',
                'slug': 'imforia-pharmacy-system-tanzania',
                'excerpt': 'The story behind Imforia, our pharmacy management system now in live use by pharmacies across Tanzania.',
                'category_slug': 'web-development',
                'author': 'Akila Body Joseph',
                'is_featured': False,
                'is_published': True,
                'content': """<p>Imforia started with a simple observation: Tanzanian pharmacies were using paper ledgers, basic spreadsheets, or expensive imported software that didn&rsquo;t fit local workflows. We built a solution that works for Tanzania. Here&rsquo;s the story.</p>

<h2>Why Existing Systems Fail</h2>
<p>Most pharmacy management systems are built for Western markets &mdash; they assume reliable internet, advanced hardware, and standardised regulatory environments. In Tanzania, pharmacies face:</p>
<ul>
    <li>Unreliable internet connectivity</li>
    <li>Power interruptions</li>
    <li>Tanzania FDA (TFDA) reporting requirements</li>
    <li>Swahili-speaking staff and customers</li>
    <li>Complex inventory with expiry tracking across multiple suppliers</li>
</ul>

<h2>Key Features Designed for Tanzania</h2>
<ul>
    <li><strong>Offline-first architecture</strong> &mdash; Works without internet, syncs when connected</li>
    <li><strong>Expiry date management</strong> &mdash; Automated alerts for soon-to-expire stock</li>
    <li><strong>TFDA-compliant reporting</strong> &mdash; Generates regulatory reports automatically</li>
    <li><strong>Swahili interface option</strong> &mdash; Staff can work in their preferred language</li>
    <li><strong>Low-bandwidth operation</strong> &mdash; Optimised for 3G networks</li>
</ul>

<h2>Real-World Impact</h2>
<p>Since deployment, pharmacies using Imforia have reported:</p>
<ul>
    <li>Reduced stockouts by over 60%</li>
    <li>Improved expiry date management</li>
    <li>Faster checkout and dispensing</li>
    <li>Better financial visibility</li>
</ul>

<h2>What&rsquo;s Next</h2>
<p>We&rsquo;re expanding Imforia with prescription management, multi-branch support, and integration with TFDA&rsquo;s digital systems. We&rsquo;re also building a mobile app for pharmacy assistants.</p>

<p>Interested in Imforia for your pharmacy? <a href="/contact/">Contact us</a> for a demo.</p>""",
            },
            {
                'title': 'Mjenzi: Building POS & Inventory for Tanzania\'s Hardware Retailers',
                'slug': 'mjenzi-pos-hardware-tanzania',
                'excerpt': 'How Mjenzi helps hardware and construction-supply retailers manage inventory, sales, and customer accounts efficiently.',
                'category_slug': 'mobile-development',
                'author': 'Akila Body Joseph',
                'is_featured': False,
                'is_published': True,
                'content': """<p>Hardware retail in Tanzania is uniquely complex. With thousands of SKUs, unit conversions between kilograms, metres, pieces, and litres, and a mix of cash and credit sales, generic POS systems simply don&rsquo;t work. That&rsquo;s why we built Mjenzi.</p>

<h2>The Hardware Challenge</h2>
<p>Walking into a Tanzanian hardware store, you&rsquo;ll find cement sold by the bag, rebar by the kilogram, paint by the litre, and nails by the piece &mdash; each with different pricing and unit conversion rules. Managing this manually leads to errors, lost sales, and frustrated customers.</p>

<h2>How Mjenzi Solves It</h2>
<ul>
    <li><strong>Multi-unit inventory</strong> &mdash; Track stock in any unit with automatic conversions</li>
    <li><strong>Credit sales management</strong> &mdash; Many hardware sales are on credit to contractors</li>
    <li><strong>Barcode scanning</strong> &mdash; Quick lookup for fast-moving items</li>
    <li><strong>Supplier management</strong> &mdash; Track purchase orders and supplier performance</li>
    <li><strong>Profit analytics</strong> &mdash; Know which products are actually making money</li>
</ul>

<h2>Built for Local Conditions</h2>
<p>Mjenzi runs smoothly on basic hardware, works with intermittent internet, and can be used in Swahili. It&rsquo;s POS software designed for Tanzania.</p>

<p>Want to see Mjenzi in action? <a href="/contact/">Request a demo</a>.</p>""",
            },
            {
                'title': 'From Campus to Company: The KianvoSoft Founding Story',
                'slug': 'kianvosoft-founding-story',
                'excerpt': 'How three Computer Engineering students at MUST turned their shared vision into a technology venture.',
                'category_slug': 'security',
                'author': 'Aneth Alphonce Seleli',
                'is_featured': True,
                'is_published': True,
                'content': """<p>Every company has an origin story. KianvoSoft&rsquo;s begins in the lecture halls and computer labs of Mbeya University of Science and Technology (MUST), where three Computer Engineering students discovered a shared frustration &mdash; and a shared vision.</p>

<h2>The Spark</h2>
<p>As final-year students, Datius, Akila, and Aneth noticed something: most of the technology they studied was built elsewhere, for markets very different from their own. The software their professors demonstrated was expensive, English-only, and designed for workflows that didn&rsquo;t exist in Tanzania.</p>
<p>Meanwhile, local businesses, pharmacies, schools, and government offices were struggling with paper-based systems or clunky imported software that didn&rsquo;t serve their needs. There was a gap &mdash; and no one was filling it.</p>

<h2>The Decision</h2>
<p>Rather than pursue separate careers after graduation, the three friends decided to build together. They pooled their skills &mdash; engineering, product thinking, and business strategy &mdash; and founded KianvoSoft in Mbeya.</p>

<h2>The Name</h2>
<p>&ldquo;Kianvo&rdquo; is derived from a concept of unity and shared purpose. The name reflects our belief that technology innovation in Africa requires collaboration &mdash; among founders, with universities, and within communities.</p>

<h2>Early Days</h2>
<p>Like most startups, our early days were lean. We built our first products while still completing coursework, using university computers and whatever resources we could find. Our first client was a local pharmacy that needed a better system &mdash; that became Imforia.</p>

<h2>Today</h2>
<p>We have designed, built, and deployed a portfolio of products spanning education technology, healthcare, retail, logistics, and social impact. We conduct applied AI research in partnership with MUST. And we train the next generation of Tanzanian developers through bootcamps and coding camps.</p>

<h2>Our Governance</h2>
<p>KianvoSoft is governed by three equal co-founders, each leading a Directorate: Datius leads Research &amp; AI, Akila leads Product &amp; Engineering, and Aneth leads Business &amp; Operations. Decisions are made collaboratively, with a clear framework for routine, joint, and strategic decisions.</p>

<p>We are KianvoSoft &mdash; innovating Africa&rsquo;s digital future from Mbeya, Tanzania.</p>

<p><a href="/about/">Learn more about us</a> or <a href="/contact/">get in touch</a>.</p>""",
            },
        ]

        if options.get('refresh_blog'):
            BlogPost.objects.all().delete()
            self.stdout.write('Deleted existing blog posts for refresh.')

        created_count = 0
        for post_data in blog_posts:
            category_slug = post_data.pop('category_slug')
            category = BlogCategory.objects.filter(slug=category_slug).first()
            _, created = BlogPost.objects.get_or_create(
                slug=post_data['slug'],
                defaults={**post_data, 'category': category}
            )
            if created:
                created_count += 1
        self.stdout.write(self.style.SUCCESS(f'Created {created_count} blog posts'))

        # Create Gallery Categories
        gallery_cats = [
            {'name': 'Bootcamps', 'slug': 'bootcamps', 'description': 'Photos from our coding bootcamps and intensive training sessions.', 'icon_class': 'fas fa-laptop-code', 'order': 1},
            {'name': 'Trainings', 'slug': 'trainings', 'description': 'Moments from our technical training programmes.', 'icon_class': 'fas fa-chalkboard-teacher', 'order': 2},
            {'name': 'Community Outreach', 'slug': 'outreach', 'description': 'Community engagement and outreach events.', 'icon_class': 'fas fa-hands-helping', 'order': 3},
        ]
        for gc_data in gallery_cats:
            GalleryCategory.objects.get_or_create(slug=gc_data['slug'], defaults=gc_data)
        self.stdout.write(self.style.SUCCESS(f'Created {len(gallery_cats)} gallery categories'))

        # Create Sample Announcements
        today = timezone.now().date()
        announcements_data = [
            {
                'title': 'Python Programming Bootcamp 2026',
                'slug': 'python-bootcamp-2026',
                'announcement_type': 'bootcamp',
                'short_description': 'An intensive 4-week Python programming bootcamp for beginners. Learn Python from scratch and build real-world projects.',
                'description': '<p>Join us for an intensive 4-week Python programming bootcamp designed for absolute beginners. You will go from zero to building real-world applications.</p><h2>What You Will Learn</h2><ul><li>Python fundamentals (variables, data types, control flow)</li><li>Functions and modules</li><li>Object-oriented programming</li><li>File handling and data processing</li><li>Introduction to web development with Django</li><li>Capstone project</li></ul><h2>Who Should Apply</h2><p>This bootcamp is ideal for university students, recent graduates, and professionals looking to start a career in software development. No prior programming experience is required.</p><h2>Why Join?</h2><p>All our instructors are experienced software engineers actively building products. You will learn by doing — building real projects that go into your portfolio.</p>',
                'start_date': today + timezone.timedelta(days=30),
                'end_date': today + timezone.timedelta(days=58),
                'application_deadline': today + timezone.timedelta(days=25),
                'venue': 'Mbeya, Tanzania (Hybrid: In-person & Online)',
                'mode': 'Hybrid',
                'fee': 'TZS 150,000',
                'capacity': 30,
                'prerequisites': 'No prior programming experience required. You need your own laptop and a willingness to learn.',
                'contact_email': 'training@kianvosoft.com',
                'contact_phone': '0749 909 819',
                'collect_applications': True,
                'application_fields': 'Current Occupation|text|required\nEducation Level|select:Secondary,Diploma,Bachelor,Masters,PhD|required\nHow did you hear about us?|text',
                'status': 'open',
                'is_featured': True,
                'is_active': True,
                'order': 1,
            },
            {
                'title': 'Mobile App Development with Flutter',
                'slug': 'flutter-development-training',
                'announcement_type': 'training',
                'short_description': 'A 6-week training programme on building cross-platform mobile applications using Flutter and Dart.',
                'description': '<p>Learn to build beautiful, cross-platform mobile applications using Flutter and Dart. This 6-week programme covers everything from the basics to advanced app architecture.</p><h2>Curriculum</h2><ul><li>Introduction to Dart programming</li><li>Flutter widgets and layouts</li><li>State management (Provider, Riverpod)</li><li>Working with APIs and databases</li><li>Firebase integration</li><li>App deployment to Play Store</li></ul>',
                'start_date': today + timezone.timedelta(days=45),
                'end_date': today + timezone.timedelta(days=87),
                'application_deadline': today + timezone.timedelta(days=40),
                'venue': 'Online',
                'mode': 'Online',
                'fee': 'TZS 200,000',
                'capacity': 25,
                'prerequisites': 'Basic programming knowledge required. Familiarity with any programming language is sufficient.',
                'contact_email': 'training@kianvosoft.com',
                'contact_phone': '0753 177 709',
                'collect_applications': True,
                'application_fields': 'Programming Experience|select:None,Beginner,Intermediate,Advanced|required\nCurrent Occupation|text|required',
                'status': 'open',
                'is_featured': True,
                'is_active': True,
                'order': 2,
            },
            {
                'title': 'Web Development with Django & React',
                'slug': 'django-react-web-dev',
                'announcement_type': 'training',
                'short_description': 'Full-stack web development training covering Django REST Framework and React for building modern web applications.',
                'description': '<p>Master full-stack web development with Django and React in this comprehensive training programme.</p><h2>What You Will Learn</h2><ul><li>Django models, views, and templates</li><li>Django REST Framework for APIs</li><li>React fundamentals and hooks</li><li>State management and routing</li><li>Authentication and authorization</li><li>Deployment and DevOps basics</li></ul>',
                'start_date': today + timezone.timedelta(days=60),
                'end_date': today + timezone.timedelta(days=102),
                'application_deadline': today + timezone.timedelta(days=55),
                'venue': 'Mbeya, Tanzania',
                'mode': 'In-Person',
                'fee': 'TZS 250,000',
                'capacity': 20,
                'prerequisites': 'Basic knowledge of Python and JavaScript. Some familiarity with web concepts (HTML, CSS) is expected.',
                'contact_email': 'training@kianvosoft.com',
                'contact_phone': '0749 909 819',
                'collect_applications': True,
                'application_fields': 'Python Experience|select:None,Beginner,Intermediate,Advanced|required\nJavaScript Experience|select:None,Beginner,Intermediate,Advanced|required',
                'status': 'open',
                'is_featured': False,
                'is_active': True,
                'order': 3,
            },
        ]

        for ann_data in announcements_data:
            Announcement.objects.get_or_create(
                slug=ann_data['slug'],
                defaults=ann_data
            )
        self.stdout.write(self.style.SUCCESS(f'Created {len(announcements_data)} announcements'))

        # Create Testimonials
        testimonials_data = [
            {
                'client_name': 'Dr. Sarah Mwambene',
                'client_position': 'Head of Pharmacy',
                'client_company': 'City Health Pharmacy, Mbeya',
                'content': 'Imforia has transformed how we manage our pharmacy operations. The inventory tracking, expiry alerts, and sales reports have given us visibility we never had before. Our team took to it quickly and we have seen a major reduction in stockouts.',
                'rating': 5,
                'is_featured': True,
                'is_active': True,
                'order': 1,
            },
            {
                'client_name': 'Joseph Kalinga',
                'client_position': 'Owner',
                'client_company': 'Kalinga Hardware, Mbeya',
                'content': 'Mjenzi solved the problem of managing different units and credit sales for our hardware business. It is easy to use, works in Swahili, and the support team responds quickly. Highly recommended for any hardware shop.',
                'rating': 5,
                'is_featured': True,
                'is_active': True,
                'order': 2,
            },
            {
                'client_name': 'Dr. Happiness Mwaipopo',
                'client_position': 'Dean, Faculty of Engineering',
                'client_company': 'Mbeya University of Science and Technology',
                'content': 'Kianvo Classroom and Kianvo Meet have been invaluable for our blended learning programmes. The platforms are built with local needs in mind — offline assessments, mobile support, and Swahili interface. A truly Tanzanian EdTech solution.',
                'rating': 5,
                'is_featured': True,
                'is_active': True,
                'order': 3,
            },
            {
                'client_name': 'Amina Salum',
                'client_position': 'Programme Manager',
                'client_company': 'Tanzania Digital Health Initiative',
                'content': 'The AI research team at KianvoSoft is doing important work in applying machine learning to healthcare challenges. Their malaria detection project has the potential to strengthen diagnostic capacity in some of our most underserved rural facilities.',
                'rating': 4,
                'is_featured': False,
                'is_active': True,
                'order': 4,
            },
            {
                'client_name': 'David Mushi',
                'client_position': 'Student',
                'client_company': 'Python Bootcamp Graduate',
                'content': 'I joined the Python Bootcamp with zero programming experience. By the end of 4 weeks, I had built my first web app. The instructors were patient, practical, and taught in a way that made sense. I am now working as a junior developer.',
                'rating': 5,
                'is_featured': True,
                'is_active': True,
                'order': 5,
            },
        ]
        created_testimonials = 0
        for t_data in testimonials_data:
            _, created = Testimonial.objects.get_or_create(
                client_name=t_data['client_name'],
                defaults=t_data
            )
            if created:
                created_testimonials += 1
        self.stdout.write(self.style.SUCCESS(f'Created {created_testimonials} testimonials'))

        # Create Partners
        partners_data = [
            {'name': 'Mbeya University of Science and Technology', 'website_url': 'https://www.must.ac.tz', 'order': 1, 'is_active': True},
            {'name': 'Centre for Innovation Technology Transfer', 'website_url': '', 'order': 2, 'is_active': True},
            {'name': 'Tanzania Commission for Science and Technology', 'website_url': 'https://www.costech.go.tz', 'order': 3, 'is_active': True},
            {'name': 'City Health Pharmacy', 'website_url': '', 'order': 4, 'is_active': True},
            {'name': 'Kalinga Hardware Supplies', 'website_url': '', 'order': 5, 'is_active': True},
        ]
        created_partners = 0
        for p_data in partners_data:
            _, created = Partner.objects.get_or_create(
                name=p_data['name'],
                defaults=p_data
            )
            if created:
                created_partners += 1
        self.stdout.write(self.style.SUCCESS(f'Created {created_partners} partners'))

        # Create Roadmap Milestones
        milestones_data = [
            {'year': '2025', 'title': 'Foundation', 'description': 'Formalise governance. Deploy Imforia, Mjenzi, and ShopManagerPro with active clients. Launch short courses and bootcamps. Establish academic partnerships with MUST and CITT.', 'order': 1, 'is_active': True},
            {'year': '2026', 'title': 'Growth', 'description': 'Expand product portfolio with Kianvo Classroom, Kianvo Meet, and HELP. Grow client base. Publish first AI research papers. Train 100+ students through bootcamps and coding camps.', 'order': 2, 'is_active': True},
            {'year': '2027', 'title': 'Expansion', 'description': 'Scale SaaS deployments. Launch FleetLink and IMS. Expand training to 8+ programmes. Enter Dar es Salaam, Dodoma, and Arusha markets. Hire additional engineering and research staff.', 'order': 3, 'is_active': True},
            {'year': '2028', 'title': 'Scaling', 'description': 'AI research unit fully operational. Brain stroke and malaria detection projects in clinical pilot phase. Staff of 12+. Explore Kenya, Uganda, and Rwanda markets.', 'order': 4, 'is_active': True},
            {'year': '2029–2030', 'title': 'Leadership', 'description': 'East Africa\'s best-known homegrown technology company. 1,000+ students trained. 200+ active clients. Pan-African digital reach. Recognised for excellence in software, training, and AI research.', 'order': 5, 'is_active': True},
        ]
        created_milestones = 0
        for m_data in milestones_data:
            _, created = RoadmapMilestone.objects.get_or_create(
                year=m_data['year'],
                title=m_data['title'],
                defaults=m_data
            )
            if created:
                created_milestones += 1
        self.stdout.write(self.style.SUCCESS(f'Created {created_milestones} roadmap milestones'))

        # Create Company Social Links
        social_links = [
            {'platform': 'Facebook', 'icon_class': 'fab fa-facebook-f', 'url': 'https://facebook.com/kianvosoft', 'order': 1, 'is_active': True},
            {'platform': 'Instagram', 'icon_class': 'fab fa-instagram', 'url': 'https://instagram.com/kianvosoft', 'order': 2, 'is_active': True},
            {'platform': 'TikTok', 'icon_class': 'fab fa-tiktok', 'url': 'https://tiktok.com/@kianvosoft', 'order': 3, 'is_active': True},
            {'platform': 'YouTube', 'icon_class': 'fab fa-youtube', 'url': 'https://youtube.com/@kianvosoft', 'order': 4, 'is_active': True},
        ]
        created_links = 0
        for sl_data in social_links:
            _, created = SocialLink.objects.get_or_create(
                platform=sl_data['platform'],
                defaults=sl_data
            )
            if created:
                created_links += 1
        self.stdout.write(self.style.SUCCESS(f'Created {created_links} social links'))

        self.stdout.write(self.style.SUCCESS('Database seeding completed successfully!'))
