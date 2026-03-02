from django.core.management.base import BaseCommand
from kianvosite.models import (
    ProjectCategory, Project, Service, CompanyStat,
    BlogCategory, BlogPost, Testimonial
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

        # Blog Posts — HTML content (CKEditor-compatible)
        blog_posts = [
            {
                'title': 'How AI is Revolutionizing Business Operations in 2026',
                'slug': 'how-ai-is-revolutionizing-business-operations-2026',
                'excerpt': 'Discover how artificial intelligence is transforming the way businesses operate, from automation to decision-making.',
                'category_slug': 'ai-technology',
                'author': 'KianvoSoft',
                'is_featured': True,
                'is_published': True,
                'content': """<p>Artificial Intelligence (AI) has moved from a buzzword to a business necessity. In 2026, companies that have embraced AI are operating more efficiently, making smarter decisions, and outpacing their competitors. Here&rsquo;s how AI is reshaping modern business operations.</p>

<h2>1. Intelligent Process Automation</h2>
<p>Gone are the days when automation simply meant running scripts. Today&rsquo;s AI-powered automation understands context, learns from patterns, and handles exceptions intelligently. From accounts payable processing to HR onboarding workflows, AI is eliminating repetitive work and freeing teams to focus on higher-value activities.</p>
<p>At KianvoSoft, we&rsquo;ve implemented AI-driven automation for clients that reduced data entry errors by <strong>90%</strong> and processing time by <strong>75%</strong>.</p>

<h2>2. Predictive Analytics &amp; Smarter Decision-Making</h2>
<p>Businesses no longer need to rely purely on gut feeling. AI systems can process thousands of data points in seconds and surface actionable insights &mdash; whether it&rsquo;s forecasting demand, detecting fraud, or predicting when equipment will fail.</p>
<p>Our custom analytics solutions help businesses move from reactive to proactive decision-making.</p>

<h2>3. Natural Language Processing in Customer Service</h2>
<p>AI chatbots and virtual assistants have matured significantly. Modern NLP models understand context, sentiment, and even regional dialects. Businesses are deploying these tools to handle <strong>70&ndash;80%</strong> of routine customer queries automatically, improving response time from hours to seconds.</p>

<h2>4. AI in Supply Chain &amp; Inventory</h2>
<p>AI models optimize inventory levels by predicting demand based on historical data, seasonality, and external factors like weather or market events. This prevents overstocking and stockouts &mdash; both of which cost businesses money.</p>

<h2>5. Personalization at Scale</h2>
<p>Whether it&rsquo;s e-commerce recommendations or personalized marketing messages, AI enables businesses to treat every customer as an individual &mdash; at scale. This drives higher conversion rates, better customer retention, and increased lifetime value.</p>

<h2>Key Takeaways</h2>
<ul>
    <li>AI is not just for large corporations &mdash; SMEs are benefiting enormously</li>
    <li>Start small: identify one repetitive process and automate it</li>
    <li>Data quality matters &mdash; AI is only as good as the data you feed it</li>
    <li>Partner with experts to implement AI responsibly and effectively</li>
</ul>

<p>At KianvoSoft, we specialize in building custom AI solutions tailored to your business. <a href="/contact/">Contact us</a> to explore how AI can transform your operations.</p>""",
            },
            {
                'title': 'Top Web Development Trends to Watch in 2026',
                'slug': 'top-web-development-trends-2026',
                'excerpt': 'From Progressive Web Apps to AI-powered interfaces, explore the trends shaping modern web development.',
                'category_slug': 'web-development',
                'author': 'KianvoSoft',
                'is_featured': True,
                'is_published': True,
                'content': """<p>The web development landscape evolves rapidly. Staying ahead of these trends ensures you build products that are fast, secure, and user-friendly. Here are the top web development trends defining 2026.</p>

<h2>1. Progressive Web Apps (PWAs) Are the New Standard</h2>
<p>PWAs combine the best of web and mobile apps. They load instantly, work offline, send push notifications, and can be installed on any device without an app store. In 2026, PWAs are becoming the default choice for businesses that want broad reach without the cost of native app development.</p>

<h2>2. Server-Side Rendering (SSR) &amp; Next.js Dominance</h2>
<p>Next.js continues to dominate the React ecosystem. With server-side rendering, static site generation, and incremental static regeneration, Next.js delivers exceptional performance and SEO. At KianvoSoft, it&rsquo;s our go-to framework for content-heavy and e-commerce web applications.</p>

<h2>3. AI-Powered User Interfaces</h2>
<p>AI is entering the UI layer. From intelligent search with semantic understanding to personalized layouts that adapt to user behavior, the web is getting smarter. Tools like GitHub Copilot are accelerating development, while AI-driven design tools help prototype faster.</p>

<h2>4. WebAssembly (WASM) for High-Performance Web Apps</h2>
<p>WebAssembly allows code written in C, C++, or Rust to run in the browser at near-native speed. This is opening doors for complex applications &mdash; video editors, 3D engines, and data processing tools &mdash; that previously required desktop software.</p>

<h2>5. API-First &amp; Headless Architecture</h2>
<p>Businesses are decoupling their frontend from the backend using headless CMS and API-first approaches. This gives teams the flexibility to deliver content to any channel &mdash; websites, mobile apps, smartwatches, or IoT devices &mdash; from a single backend.</p>

<h2>6. Web Security &amp; Zero Trust Architecture</h2>
<p>With cyber threats escalating, modern web development must bake security in from day one. Zero Trust principles, HTTPS everywhere, Content Security Policies, and OAuth 2.0 are now baseline requirements.</p>

<h2>7. Edge Computing &amp; CDNs</h2>
<p>Deploying code to the edge &mdash; as close to the user as possible &mdash; dramatically reduces latency. Platforms like Vercel Edge, Cloudflare Workers, and AWS CloudFront are enabling sub-100ms response times globally.</p>

<h2>Final Thoughts</h2>
<p>The best web applications in 2026 are fast, secure, accessible, and AI-enhanced. At KianvoSoft, we build web applications that combine technical excellence with exceptional user experience. <a href="/contact/">Talk to our team</a> about your next web project.</p>""",
            },
            {
                'title': 'Flutter vs React Native: Which to Choose in 2026?',
                'slug': 'flutter-vs-react-native-2026',
                'excerpt': 'A comprehensive comparison of the two leading cross-platform mobile development frameworks to help you make the right choice.',
                'category_slug': 'mobile-development',
                'author': 'KianvoSoft',
                'is_featured': False,
                'is_published': True,
                'content': """<p>Choosing between Flutter and React Native is one of the most common decisions teams face when starting a mobile project. Both are excellent frameworks &mdash; but they have different strengths. Here&rsquo;s our 2026 comparison to help you decide.</p>

<h2>Overview</h2>
<p><strong>Flutter</strong> is Google&rsquo;s UI toolkit for building natively compiled apps from a single codebase. It uses the Dart programming language and renders UI using its own engine (Skia / Impeller).</p>
<p><strong>React Native</strong> is Meta&rsquo;s framework that uses JavaScript/TypeScript and React to build mobile apps. It bridges to native components, meaning UI looks and feels native on each platform.</p>

<h2>Performance</h2>
<p><strong>Flutter</strong> has an edge in raw performance because it doesn&rsquo;t rely on a JavaScript bridge. The Flutter engine renders directly to the canvas, resulting in consistent 60/120fps animations.</p>
<p><strong>React Native</strong> has improved significantly with the new architecture (JSI + Fabric), removing the old bridge bottleneck. For most business apps, the performance difference is negligible.</p>
<p><strong>Winner: Flutter</strong> (slightly, for graphically intensive apps)</p>

<h2>Developer Experience</h2>
<p><strong>Flutter</strong> uses Dart, which is relatively easy to learn. Hot reload is excellent, and the widget system is powerful and consistent. However, the Dart ecosystem is smaller than JavaScript&rsquo;s.</p>
<p><strong>React Native</strong> uses JavaScript/TypeScript &mdash; the most widely known language. If your team already knows React, the learning curve is minimal. The npm ecosystem gives access to thousands of packages.</p>
<p><strong>Winner: React Native</strong> (for teams with existing JavaScript knowledge)</p>

<h2>UI Consistency vs. Native Feel</h2>
<p><strong>Flutter</strong> gives you pixel-perfect UI that looks identical on Android and iOS. Ideal for brand consistency, but may feel slightly &ldquo;non-native&rdquo; to users.</p>
<p><strong>React Native</strong> renders native components, so the app feels at home on each platform.</p>

<h2>Our Recommendation</h2>
<table>
    <thead>
        <tr><th>Use Case</th><th>Recommended Framework</th></tr>
    </thead>
    <tbody>
        <tr><td>Highly visual / branded app</td><td>Flutter</td></tr>
        <tr><td>Team knows JavaScript / React</td><td>React Native</td></tr>
        <tr><td>Games &amp; animations</td><td>Flutter</td></tr>
        <tr><td>Enterprise business app</td><td>Either (both excellent)</td></tr>
        <tr><td>Tight deadline with JS team</td><td>React Native</td></tr>
        <tr><td>Long-term cross-platform</td><td>Flutter</td></tr>
    </tbody>
</table>

<p>At KianvoSoft, we build with both frameworks. <a href="/contact/">Contact us</a> to discuss which is right for your project.</p>""",
            },
            {
                'title': 'Essential Cybersecurity Practices for Small Businesses',
                'slug': 'essential-cybersecurity-practices-small-businesses',
                'excerpt': 'Protect your business from cyber threats with these essential security measures and best practices every business must implement.',
                'category_slug': 'security',
                'author': 'KianvoSoft',
                'is_featured': False,
                'is_published': True,
                'content': """<p>Small businesses are increasingly targeted by cybercriminals &mdash; often because they have weaker defenses than large corporations. Yet a single breach can be devastating. Here are the essential cybersecurity practices every small business must implement in 2026.</p>

<h2>1. Use Strong, Unique Passwords &amp; a Password Manager</h2>
<p>Weak and reused passwords remain the #1 cause of breaches. Every account should have a unique, complex password. Use a password manager like Bitwarden, 1Password, or Dashlane to generate and store them securely.</p>
<p><strong>Action:</strong> Set a company policy requiring passwords of 16+ characters with mixed characters.</p>

<h2>2. Enable Multi-Factor Authentication (MFA) Everywhere</h2>
<p>MFA adds a second layer of protection. Even if a password is stolen, the attacker can&rsquo;t access the account without the second factor. Enable MFA on:</p>
<ul>
    <li>Email accounts (Gmail, Outlook)</li>
    <li>Cloud services (AWS, DigitalOcean)</li>
    <li>Social media business accounts</li>
    <li>Financial accounts</li>
</ul>

<h2>3. Keep Software &amp; Systems Updated</h2>
<p>Unpatched software is a goldmine for hackers. Enable automatic updates for operating systems, browsers, and applications. Schedule regular patching cycles for servers.</p>

<h2>4. Train Your Team &mdash; Humans Are the Weakest Link</h2>
<p>Phishing attacks trick employees into clicking malicious links or sharing credentials. Regular security awareness training dramatically reduces this risk. Topics to cover:</p>
<ul>
    <li>Recognizing phishing emails</li>
    <li>Safe browsing habits</li>
    <li>What to do if you suspect a breach</li>
    <li>Social engineering attacks</li>
</ul>

<h2>5. Back Up Your Data &mdash; The 3-2-1 Rule</h2>
<p>Follow the <strong>3-2-1 backup rule</strong>:</p>
<ul>
    <li><strong>3</strong> copies of your data</li>
    <li><strong>2</strong> different storage types (local + cloud)</li>
    <li><strong>1</strong> copy offsite or air-gapped</li>
</ul>
<p>Test your backups regularly. A backup you&rsquo;ve never tested is a backup you can&rsquo;t trust.</p>

<h2>6. Secure Your Wi-Fi Network</h2>
<ul>
    <li>Use WPA3 encryption</li>
    <li>Create a separate guest network for visitors</li>
    <li>Hide your SSID</li>
    <li>Change default router credentials</li>
</ul>

<h2>7. Have an Incident Response Plan</h2>
<p>When (not if) a breach happens, having a clear plan reduces panic and damage. Your plan should include:</p>
<ul>
    <li>Who to contact (IT, legal, affected clients)</li>
    <li>How to contain the breach</li>
    <li>Steps to recover systems</li>
    <li>Communication plan</li>
</ul>

<p>Cybersecurity doesn&rsquo;t have to be overwhelming. Start with the basics, build good habits, and layer your defenses over time. At KianvoSoft, we offer IT security assessments and consulting. <a href="/contact/">Get in touch</a> to learn more.</p>""",
            },
            {
                'title': 'Cloud Migration: A Step-by-Step Guide for Businesses',
                'slug': 'cloud-migration-step-by-step-guide',
                'excerpt': 'Learn how to successfully migrate your infrastructure to the cloud with our comprehensive, actionable guide.',
                'category_slug': 'cloud-devops',
                'author': 'KianvoSoft',
                'is_featured': False,
                'is_published': True,
                'content': """<p>Migrating to the cloud is one of the most impactful technology decisions a business can make. When done right, it reduces infrastructure costs, improves reliability, and enables your team to scale quickly. Here&rsquo;s a step-by-step guide to a successful cloud migration.</p>

<h2>Phase 1: Assessment &amp; Planning</h2>
<h3>Audit Your Current Infrastructure</h3>
<p>Before moving anything, catalog what you have: applications and their dependencies, databases and data volumes, current hardware and licenses, and traffic patterns and peak loads.</p>

<h3>Choose Your Cloud Provider</h3>
<ul>
    <li><strong>AWS</strong> &mdash; Most mature, largest feature set</li>
    <li><strong>Google Cloud (GCP)</strong> &mdash; Strong in data/AI services</li>
    <li><strong>DigitalOcean / Hetzner</strong> &mdash; Cost-effective for SMEs</li>
    <li><strong>Azure</strong> &mdash; Best for Microsoft-heavy environments</li>
</ul>

<h2>Phase 2: Choose Your Migration Strategy (The 6 R&rsquo;s)</h2>
<ol>
    <li><strong>Rehost (Lift &amp; Shift)</strong> &mdash; Move as-is. Fastest, least optimization.</li>
    <li><strong>Replatform</strong> &mdash; Minor tweaks to take advantage of cloud (e.g., managed DB).</li>
    <li><strong>Refactor</strong> &mdash; Redesign the app for cloud-native architecture.</li>
    <li><strong>Repurchase</strong> &mdash; Switch to a SaaS product instead.</li>
    <li><strong>Retain</strong> &mdash; Keep on-premise (some systems don&rsquo;t need to move).</li>
    <li><strong>Retire</strong> &mdash; Decommission unused systems.</li>
</ol>

<h2>Phase 3: Migrate in Stages</h2>
<p>Never move everything at once. Use this order:</p>
<ol>
    <li><strong>Development/test environments first</strong> &mdash; Low risk, validates your process</li>
    <li><strong>Non-critical production workloads</strong> &mdash; Build confidence</li>
    <li><strong>Core production systems</strong> &mdash; With rollback plans ready</li>
</ol>

<h2>Phase 4: Optimize &amp; Secure</h2>
<ul>
    <li>Right-size your instances (don&rsquo;t over-provision)</li>
    <li>Enable auto-scaling for variable workloads</li>
    <li>Set up automated backups and snapshots</li>
    <li>Implement cloud security best practices (encryption, access controls)</li>
    <li>Review your bill &mdash; cloud waste is real</li>
</ul>

<h2>Common Pitfalls to Avoid</h2>
<ul>
    <li><strong>Migrating without a rollback plan</strong> &mdash; Always have one</li>
    <li><strong>Ignoring data transfer costs</strong> &mdash; Egress fees add up</li>
    <li><strong>Poor IAM configuration</strong> &mdash; Over-privileged accounts are a risk</li>
    <li><strong>Skipping the test phase</strong> &mdash; Test everything before cutover</li>
</ul>

<p>KianvoSoft helps businesses plan and execute cloud migrations of all sizes. <a href="/contact/">Contact our team</a> for a free consultation.</p>""",
            },
            {
                'title': 'Turning Data into Business Intelligence: A Practical Guide',
                'slug': 'turning-data-into-business-intelligence',
                'excerpt': 'Discover how to leverage your business data for actionable insights and better decision-making with this practical BI guide.',
                'category_slug': 'ai-technology',
                'author': 'KianvoSoft',
                'is_featured': False,
                'is_published': True,
                'content': """<p>Every business generates data &mdash; transactions, customer interactions, website visits, inventory movements. But most of that data sits unused. Business Intelligence (BI) transforms raw data into meaningful insights that drive smarter decisions. Here&rsquo;s how to get started.</p>

<h2>What is Business Intelligence?</h2>
<p>Business Intelligence is the set of technologies, processes, and tools used to collect, integrate, analyze, and present business data. The goal is simple: turn data into actionable information that leaders can use to make better decisions faster.</p>

<h2>Step 1: Identify the Questions You Need to Answer</h2>
<p>BI starts with business questions, not data. Ask yourself:</p>
<ul>
    <li>Which products/services are most profitable?</li>
    <li>What are our peak sales periods?</li>
    <li>Which customers are at risk of churning?</li>
    <li>Where are the bottlenecks in our operations?</li>
    <li>What does our cash flow look like over the next 90 days?</li>
</ul>

<h2>Step 2: Audit Your Data Sources</h2>
<p>Common data sources include:</p>
<ul>
    <li><strong>Accounting software</strong> &mdash; Revenue, expenses, invoices</li>
    <li><strong>POS / Sales systems</strong> &mdash; Transaction data, product performance</li>
    <li><strong>CRM</strong> &mdash; Customer interactions, pipeline, churn</li>
    <li><strong>Website analytics</strong> &mdash; Traffic, conversions, behavior</li>
    <li><strong>Spreadsheets</strong> &mdash; Often contain critical data not in any system</li>
</ul>

<h2>Step 3: Build Your Data Pipeline</h2>
<p>Data needs to flow from source systems to a central location where it can be analyzed. This typically involves:</p>
<ol>
    <li><strong>Extract</strong> &mdash; Pull data from source systems</li>
    <li><strong>Transform</strong> &mdash; Clean, normalize, and structure it</li>
    <li><strong>Load</strong> &mdash; Store it in a data warehouse or data lake</li>
</ol>

<h2>Step 4: Choose Your Visualization Tool</h2>
<ul>
    <li><strong>Power BI</strong> &mdash; Best for Microsoft environments</li>
    <li><strong>Tableau</strong> &mdash; Powerful, great for complex visualizations</li>
    <li><strong>Metabase</strong> &mdash; Open-source, excellent for SMEs</li>
    <li><strong>Google Looker Studio</strong> &mdash; Free, integrates with Google products</li>
</ul>

<h2>Step 5: Build Your Key Dashboards</h2>
<h3>Executive Dashboard</h3>
<ul>
    <li>Revenue vs. target</li>
    <li>Key expense categories</li>
    <li>Net profit margin</li>
    <li>Customer acquisition cost</li>
</ul>
<h3>Operations Dashboard</h3>
<ul>
    <li>Order fulfillment rates</li>
    <li>Inventory levels</li>
    <li>Staff productivity metrics</li>
</ul>

<h2>Common Mistakes to Avoid</h2>
<ul>
    <li><strong>Collecting everything</strong> &mdash; Focus on data that answers real questions</li>
    <li><strong>Trusting dirty data</strong> &mdash; Invest in data quality upfront</li>
    <li><strong>Building dashboards nobody uses</strong> &mdash; Involve end users in the design</li>
</ul>

<p>We build custom BI solutions tailored to your industry and business model &mdash; from data pipelines and warehouses to interactive dashboards. <a href="/contact/">Contact us</a> to discuss your data analytics needs.</p>""",
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

        self.stdout.write(self.style.SUCCESS('Database seeding completed successfully!'))
