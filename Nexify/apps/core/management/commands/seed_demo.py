"""
seed_demo — ساخت داده‌ی نمونه (پروژه‌ها، مقالات، سوالات متداول).

استفاده: python manage.py seed_demo
"""
from django.core.management.base import BaseCommand

from apps.blog.models import BlogPost
from apps.contact.models import FAQ
from apps.panel.models import Testimonial
from apps.projects.models import Project

GITHUB = "https://github.com/amirrezahajiabadi"

PROJECTS = [
    {
        "order": 1,
        "title": "وب‌سایت شرکتی",
        "icon": "🌐",
        "categories": "web",
        "category_label": "طراحی سایت",
        "short_description": "طراحی و توسعه وب‌سایت کامل شرکتی با پنل مدیریت و سیستم احراز هویت",
        "description": "طراحی و توسعه یک وب‌سایت کامل شرکتی با پنل مدیریت اختصاصی.",
        "tags": ["React", "Django", "PostgreSQL", "Docker"],
        "duration": "۶ هفته",
        "role": "Full-Stack",
        "status": "تکمیل شده",
        "github_url": GITHUB,
        "gradient": "135deg,#1e1b4b,#312e81",
    },
    {
        "order": 2,
        "title": "دستیار هوشمند پشتیبانی",
        "icon": "🤖",
        "categories": "ai",
        "category_label": "Agent AI",
        "short_description": "ساخت Agent مبتنی بر LLM با قابلیت RAG برای پاسخگویی به مشتریان",
        "description": "یک Agent هوشمند مبتنی بر LLM با قابلیت RAG.",
        "tags": ["LangChain", "OpenAI", "ChromaDB", "FastAPI"],
        "duration": "۸ هفته",
        "role": "AI Engineer",
        "status": "در حال بهبود",
        "github_url": GITHUB,
        "gradient": "135deg,#1e3a5f,#2563eb",
    },
    {
        "order": 3,
        "title": "Pipeline استقرار مدل",
        "icon": "⚙️",
        "categories": "mlops",
        "category_label": "MLOps",
        "short_description": "استقرار خودکار مدل‌های ML با Docker و GitHub Actions روی AWS",
        "description": "پیاده‌سازی CI/CD Pipeline خودکار برای استقرار مدل‌های ML.",
        "tags": ["Docker", "GitHub Actions", "MLflow", "AWS"],
        "duration": "۴ هفته",
        "role": "MLOps Engineer",
        "status": "تکمیل شده",
        "github_url": GITHUB,
        "gradient": "135deg,#1b4332,#059669",
    },
    {
        "order": 4,
        "title": "اپلیکیشن مدیریت وظایف",
        "icon": "📱",
        "categories": "app",
        "category_label": "اپلیکیشن",
        "short_description": "اپلیکیشن Cross-Platform با همگام‌سازی بلادرنگ و نوتیفیکیشن",
        "description": "اپلیکیشن Cross-Platform برای مدیریت وظایف تیمی.",
        "tags": ["Flutter", "Django", "WebSocket", "Firebase"],
        "duration": "۱۰ هفته",
        "role": "Mobile Developer",
        "status": "تکمیل شده",
        "github_url": GITHUB,
        "gradient": "135deg,#4a1942,#be185d",
    },
    {
        "order": 5,
        "title": "داشبورد تحلیل داده",
        "icon": "📊",
        "categories": "web ai",
        "category_label": "Web App",
        "short_description": "Web App تعاملی برای تحلیل داده و پیش‌بینی روندها با ML",
        "description": "وب اپلیکیشن تعاملی برای تحلیل و مصورسازی داده.",
        "tags": ["Next.js", "FastAPI", "Scikit-learn", "Pandas"],
        "duration": "۶ هفته",
        "role": "Full-Stack + ML",
        "status": "تکمیل شده",
        "github_url": GITHUB,
        "gradient": "135deg,#1a1a2e,#6d28d9",
    },
    {
        "order": 6,
        "title": "پلتفرم چت هوشمند",
        "icon": "💬",
        "categories": "ai web",
        "category_label": "AI Platform",
        "short_description": "پلتفرم تحت وب برای ساخت و مدیریت چت‌بات‌های هوشمند",
        "description": "پلتفرم تحت وب برای ساخت و مدیریت چت‌بات‌های هوشمند.",
        "tags": ["FastAPI", "WebSocket", "LangChain", "Redis"],
        "duration": "۱۲ هفته",
        "role": "AI + Backend",
        "status": "در حال توسعه",
        "github_url": GITHUB,
        "gradient": "135deg,#1e1b4b,#7c3aed",
    },
]

POSTS = [
    {
        "title": "راهنمای کامل FastAPI: از صفر تا deployment",
        "slug": "fastapi-guide",
        "category": "پایتون",
        "icon": "🐍",
        "gradient": "135deg,#1e3a5f,#2563eb",
        "excerpt": "قدم‌به‌قدم یاد بگیرید چطور یک API حرفه‌ای با FastAPI بسازید و با Docker deploy کنید",
        "content": (
            "FastAPI یکی از سریع‌ترین و مدرن‌ترین فریمورک‌های پایتون برای ساخت API است.\n\n"
            "در این مقاله قدم‌به‌قدم یاد می‌گیرید چطور یک API ساده با FastAPI بسازید، آن را با "
            "SQLAlchemy به دیتابیس وصل کنید و در نهایت با Docker کانتینرسازی و deploy کنید.\n\n"
            "نکته‌ی کلیدی: استفاده از async/await در FastAPI باعث می‌شود برنامه‌ی شما بتواند "
            "هزاران درخواست هم‌زمان را مدیریت کند."
        ),
        "read_time": 8,
        "published_at": "2023-08-06",
    },
    {
        "title": "ساخت Agent AI با LangChain و RAG",
        "slug": "langchain-rag-agent",
        "category": "هوش مصنوعی",
        "icon": "🤖",
        "gradient": "135deg,#1b4332,#059669",
        "excerpt": "آموزش عملی ساخت یک Agent هوشمند که می‌تواند با داکیومنت‌های شما کار کند",
        "content": (
            "RAG یا Retrieval-Augmented Generation روشی است که به مدل‌های زبانی اجازه می‌دهد "
            "به دانش اختصاصی شما دسترسی داشته باشند.\n\n"
            "در این آموزش یک Agent می‌سازیم که اسناد شما را ایندکس می‌کند و به سوالات کاربر "
            "بر اساس همان اسناد پاسخ می‌دهد — بدون نیاز به آموزش مجدد مدل."
        ),
        "read_time": 12,
        "published_at": "2023-07-23",
    },
    {
        "title": "Docker برای توسعه‌دهنده‌ها",
        "slug": "docker-for-developers",
        "category": "توسعه",
        "icon": "🐳",
        "gradient": "135deg,#4a1942,#be185d",
        "excerpt": "همه چیز درباره کانتینرسازی - از نصب تا ساخت Dockerfile و docker-compose",
        "content": (
            "Docker به شما اجازه می‌دهد برنامه‌ی خود را همراه با تمام وابستگی‌هایش بسته‌بندی "
            "کنید تا در هر محیطی یکسان اجرا شود.\n\n"
            "در این مقاله یاد می‌گیرید Dockerfile بنویسید، تصویر بسازید و چند سرویس را با "
            "docker-compose کنار هم اجرا کنید."
        ),
        "read_time": 10,
        "published_at": "2023-07-11",
    },
    {
        "title": "CI/CD برای مدل‌های ML با GitHub Actions",
        "slug": "ml-cicd-github-actions",
        "category": "MLOps",
        "icon": "⚙️",
        "gradient": "135deg,#1a1a2e,#6d28d9",
        "excerpt": "راه‌اندازی pipeline خودکار برای تست، اعتبارسنجی و deploy مدل‌های ML",
        "content": (
            "مدل‌های یادگیری ماشین هم مثل نرم‌افزار به تست و استقرار خودکار نیاز دارند.\n\n"
            "با GitHub Actions می‌توانید pipeline ای بسازید که با هر commit، مدل را تست می‌کند، "
            "متریک‌ها را اعتبارسنجی می‌کند و در صورت قبولی، آن را در محیط تولید deploy می‌کند."
        ),
        "read_time": 15,
        "published_at": "2023-06-26",
    },
    {
        "title": "۵ کتابخانه ضروری پایتون برای Data Science",
        "slug": "essential-python-ds-libs",
        "category": "علم داده",
        "icon": "🔥",
        "gradient": "135deg,#1e1b4b,#7c3aed",
        "excerpt": "معرفی Pandas, NumPy, Scikit-learn, Matplotlib و Seaborn",
        "content": (
            "پنج کتابخانه‌ای که هر تحلیلگر داده‌ای باید بلد باشد:\n\n"
            "۱. NumPy برای محاسبات عددی، ۲. Pandas برای کار با داده‌های جدولی، "
            "۳. Scikit-learn برای یادگیری ماشین، ۴. Matplotlib برای رسم نمودار و "
            "۵. Seaborn برای مصورسازی آماری پیشرفته."
        ),
        "read_time": 7,
        "published_at": "2023-06-15",
    },
    {
        "title": "مقایسه React و Next.js",
        "slug": "react-vs-nextjs",
        "category": "طراحی",
        "icon": "🌐",
        "gradient": "135deg,#3b1f1f,#dc2626",
        "excerpt": "بررسی تفاوت‌ها، مزایا و معایب برای پروژه‌های مختلف",
        "content": (
            "React یک کتابخانه برای ساخت رابط کاربری است و Next.js فریمورکی مبتنی بر آن که "
            "قابلیت‌های سرورساید مثل SSR و SSG را اضافه می‌کند.\n\n"
            "اگر به سئو اهمیت می‌دهید یا سایت محتوایی دارید، Next.js انتخاب بهتری است. برای "
            "اپلیکیشن‌های تعاملی کاملاً کلاینت‌ساید، React به تنهایی کافی است."
        ),
        "read_time": 6,
        "published_at": "2023-05-31",
    },
]

TESTIMONIALS = [
    {
        "name": "سارا محمدی",
        "company": "فروشگاه آنلاین دیجی‌استایل",
        "text": "طراحی سایت فروشگاهی‌مون خیلی حرفه‌ای انجام شد؛ سرعت لود و ظاهر سایت دقیقاً همون چیزی بود که می‌خواستیم.",
        "rating": 5,
        "order": 1,
    },
    {
        "name": "رضا کریمی",
        "company": "استارتاپ هوشمند چت‌یار",
        "text": "Agent پشتیبانی مشتری که برامون ساختن، تیکت‌های تکراری رو خودکار جواب می‌ده و تیم پشتیبانی‌مون آزاد شد.",
        "rating": 5,
        "order": 2,
    },
    {
        "name": "مینا احمدی",
        "company": "کلینیک آنلاین سلامت",
        "text": "نقشه راه هوش مصنوعی که گرفتم شفاف و عملی بود؛ حالا دقیقاً می‌دونیم از کجا شروع کنیم و چطور مقیاس بدیم.",
        "rating": 4,
        "order": 3,
    },
    {
        "name": "امیر رضایی",
        "company": "پلتفرم لجستیک سریع‌پی",
        "text": "Pipeline استقرار مدل‌هاشون خطای دستی رو به صفر رسوند؛ دیپلوی‌ها الان کاملاً خودکار و قابل اعتمادن.",
        "rating": 5,
        "order": 4,
    },
    {
        "name": "نگار حسینی",
        "company": "آکادمی آنلاین یادو",
        "text": "پنل مدیریتی که برامون طراحی کردن کار با اون رو برای تیم غیرفنی‌مون فوق‌العاده ساده کرده.",
        "rating": 5,
        "order": 5,
    },
    {
        "name": "حمید نوروزی",
        "company": "شرکت نرم‌افزاری فناوران",
        "text": "مشاوره‌ی معماری که گرفتم باعث شد هزینه‌ی زیرساخت‌مون ۴۰٪ کم بشه. خیلی دقیق و به‌موقع.",
        "rating": 4,
        "order": 6,
    },
]

FAQS = [
    {"question": "💬 هزینه پروژه‌ها چطور محاسبه میشه؟", "answer": "بر اساس scope پروژه، تکنولوژی‌های مورد نیاز و زمان تحویل. یه جلسه مشاوره رایگان داریم تا برآورد شفاف ارائه بدیم.", "order": 1},
    {"question": "⏱ چقدر طول میکشه پروژه آماده بشه؟", "answer": "Landing Page: ۱-۲ هفته، Web App: ۴-۸ هفته، پروژه AI: ۸-۱۲ هفته.", "order": 2},
    {"question": "🛡 آیا پشتیبانی بعد از تحویل دارید؟", "answer": "بله! تمام پروژه‌ها شامل ۳ ماه پشتیبانی رایگان پس از تحویل هستن.", "order": 3},
    {"question": "🌍 پروژه‌های ریموت رو قبول می‌کنید؟", "answer": "حتماً! بیشتر پروژه‌ها رو به صورت ریموت انجام می‌دیم.", "order": 4},
    {"question": "💰 شرایط پرداخت چطوریه؟", "answer": "مرحله‌ای: ۳۰٪ پیش‌پرداخت، ۴۰٪ میانی، ۳۰٪ پس از تحویل نهایی.", "order": 5},
    {"question": "🤖 برای Agent AI چه اطلاعاتی نیاز دارید؟", "answer": "فرآیندهای کسب‌وکار، داکیومنت‌ها و وظایفی که Agent باید انجام بده.", "order": 6},
]


class Command(BaseCommand):
    help = "داده‌ی نمونه (پروژه‌ها، مقالات، سوالات متداول) را می‌سازد"

    def handle(self, *args, **options):
        for data in PROJECTS:
            Project.objects.get_or_create(order=data["order"], defaults=data)
        for data in POSTS:
            BlogPost.objects.update_or_create(
                slug=data["slug"], defaults={**data, "is_published": True}
            )
        for data in FAQS:
            FAQ.objects.get_or_create(question=data["question"], defaults=data)
        for data in TESTIMONIALS:
            Testimonial.objects.get_or_create(name=data["name"], defaults=data)

        self.stdout.write(
            self.style.SUCCESS(
                f"{Project.objects.count()} project, {BlogPost.objects.count()} post, "
                f"{FAQ.objects.count()} faq, {Testimonial.objects.count()} testimonial ready."
            )
        )
