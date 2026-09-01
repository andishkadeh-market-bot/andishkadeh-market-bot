"""
Marketing Data Layer
Andishkadeh Management & Market

نسخه: Advanced / Professional / 2026

این فایل شامل:
- برنامه جامع آموزش بازاریابی
- درسنامه‌های تخصصی
- مباحث استراتژیک
- بازاریابی دیجیتال
- رفتار مصرف‌کننده
- تحقیقات بازار
- STP
- برند
- قیمت‌گذاری
- فروش
- CRM
- Growth Marketing
- Marketing Analytics
- Performance Marketing
- AI Marketing
- First-party Data
- Privacy-first Marketing
- AEO
- Omnichannel
- Commerce Media
- آزمون‌های تخصصی

APIهای سازگار:
    get_chapters()
    get_chapter()
    get_lessons()
    get_lesson()
    get_quiz_questions()

APIهای تکمیلی:
    get_module_info()
    get_curriculum_statistics()
    search_lessons()
    validate_curriculum()

نکته:
این فایل فقط لایه داده است و نباید Telegram Handler
یا منطق سرویس را مستقیماً مدیریت کند.
"""

from __future__ import annotations

from typing import Any


# ==========================================================
# Module Information
# ==========================================================

MODULE_ID = "marketing"

MODULE_TITLE = "📈 بازاریابی و فروش"

MODULE_DESCRIPTION = (
    "آموزش تخصصی، حرفه‌ای و به‌روز بازاریابی، فروش، "
    "برند، رفتار مصرف‌کننده، بازاریابی دیجیتال، "
    "تحلیل داده، رشد و هوش مصنوعی در بازاریابی."
)

MODULE_VERSION = "2026.1"

MODULE_LEVEL = "Advanced / Professional / Specialist"


# ==========================================================
# Curriculum
# ==========================================================

MARKETING_CURRICULUM: list[dict[str, Any]] = [

    {
        "id": "chapter_01",
        "title": "فصل ۱: مبانی حرفه‌ای و تفکر بازاریابی",
        "description": (
            "شناخت فلسفه بازاریابی، بازارگرایی، ارزش مشتری، "
            "بازار، نیاز، خواسته، تقاضا و منطق ایجاد ارزش."
        ),
        "level": "مقدماتی تا متوسط",
    },

    {
        "id": "chapter_02",
        "title": "فصل ۲: استراتژی بازاریابی",
        "description": (
            "فرآیند تدوین استراتژی، تحلیل محیط، اهداف، "
            "مزیت رقابتی، انتخاب بازار و طراحی برنامه بازاریابی."
        ),
        "level": "پیشرفته",
    },

    {
        "id": "chapter_03",
        "title": "فصل ۳: رفتار مصرف‌کننده و اقتصاد رفتاری",
        "description": (
            "فرآیند تصمیم خرید، عوامل روان‌شناختی، اجتماعی، "
            "فرهنگی و کاربرد اقتصاد رفتاری در بازاریابی."
        ),
        "level": "پیشرفته",
    },

    {
        "id": "chapter_04",
        "title": "فصل ۴: تحقیقات بازار و Customer Insight",
        "description": (
            "طراحی تحقیق، داده اولیه و ثانویه، روش‌های کیفی و کمی، "
            "نمونه‌گیری، پرسشنامه، مصاحبه و استخراج بینش مشتری."
        ),
        "level": "پیشرفته",
    },

    {
        "id": "chapter_05",
        "title": "فصل ۵: STP و بخش‌بندی استراتژیک بازار",
        "description": (
            "Segmentation، Targeting، Positioning و طراحی جایگاه "
            "رقابتی و ارزش پیشنهادی."
        ),
        "level": "پیشرفته",
    },

    {
        "id": "chapter_06",
        "title": "فصل ۶: تحلیل رقابتی و Competitive Intelligence",
        "description": (
            "تحلیل رقبا، نیروهای رقابتی، Benchmarking، "
            "مزیت رقابتی و هوشمندی بازار."
        ),
        "level": "تخصصی",
    },

    {
        "id": "chapter_07",
        "title": "فصل ۷: مدیریت محصول و Product Marketing",
        "description": (
            "Product-Market Fit، ارزش پیشنهادی، چرخه عمر محصول، "
            "Go-to-Market و Product-Led Growth."
        ),
        "level": "تخصصی",
    },

    {
        "id": "chapter_08",
        "title": "فصل ۸: قیمت‌گذاری و Revenue Management",
        "description": (
            "استراتژی قیمت، ارزش ادراک‌شده، کشش تقاضا، "
            "قیمت‌گذاری مبتنی بر ارزش و مدیریت درآمد."
        ),
        "level": "تخصصی",
    },

    {
        "id": "chapter_09",
        "title": "فصل ۹: برندینگ و Brand Equity",
        "description": (
            "هویت برند، تصویر برند، جایگاه، شخصیت، معماری برند، "
            "ارزش ویژه برند و مدیریت تجربه برند."
        ),
        "level": "تخصصی",
    },

    {
        "id": "chapter_10",
        "title": "فصل ۱۰: بازاریابی B2B و Account-Based Marketing",
        "description": (
            "بازاریابی سازمانی، Buying Center، قیف B2B، "
            "ABM، Lead Generation و مدیریت حساب‌های کلیدی."
        ),
        "level": "تخصصی",
    },

    {
        "id": "chapter_11",
        "title": "فصل ۱۱: فروش حرفه‌ای و Sales Enablement",
        "description": (
            "فرآیند فروش، Qualification، Discovery، ارائه ارزش، "
            "اعتراضات، Closing و همکاری بازاریابی و فروش."
        ),
        "level": "تخصصی",
    },

    {
        "id": "chapter_12",
        "title": "فصل ۱۲: CRM، وفاداری و Customer Lifetime Value",
        "description": (
            "مدیریت رابطه مشتری، Retention، Churn، Loyalty، "
            "CLV، NPS و طراحی چرخه عمر مشتری."
        ),
        "level": "پیشرفته",
    },

    {
        "id": "chapter_13",
        "title": "فصل ۱۳: بازاریابی دیجیتال و Performance Marketing",
        "description": (
            "SEO، SEM، تبلیغات دیجیتال، شبکه‌های اجتماعی، "
            "Content Marketing، Conversion و Performance."
        ),
        "level": "پیشرفته",
    },

    {
        "id": "chapter_14",
        "title": "فصل ۱۴: Growth Marketing و Funnel Optimization",
        "description": (
            "قیف رشد، Acquisition، Activation، Retention، Revenue، "
            "Referral و طراحی موتور رشد."
        ),
        "level": "تخصصی",
    },

    {
        "id": "chapter_15",
        "title": "فصل ۱۵: Marketing Analytics و Attribution",
        "description": (
            "KPI، CAC، LTV، ROI، ROAS، Attribution، "
            "Incrementality، Cohort Analysis و داشبورد مدیریتی."
        ),
        "level": "فوق‌تخصصی",
    },

    {
        "id": "chapter_16",
        "title": "فصل ۱۶: AI Marketing و Generative AI",
        "description": (
            "کاربرد هوش مصنوعی، Personalization، Predictive Marketing، "
            "Generative AI، AI Agents و Machine Marketing."
        ),
        "level": "فوق‌تخصصی",
    },

    {
        "id": "chapter_17",
        "title": "فصل ۱۷: داده، Privacy و MarTech",
        "description": (
            "First-party Data، Zero-party Data، CDP، CRM، "
            "Consent، Clean Room، Data Governance و Privacy-first."
        ),
        "level": "فوق‌تخصصی",
    },

    {
        "id": "chapter_18",
        "title": "فصل ۱۸: Omnichannel، AEO و آینده بازاریابی",
        "description": (
            "تجربه یکپارچه مشتری، Commerce Media، "
            "Answer Engine Optimization، AI Customers و آینده بازار."
        ),
        "level": "فوق‌تخصصی",
    },
]


# ==========================================================
# Lessons
# ==========================================================

MARKETING_LESSONS: dict[str, list[dict[str, Any]]] = {

    "chapter_01": [

        {
            "id": "lesson_01_01",
            "title": "مفهوم بازاریابی حرفه‌ای",
            "content": """
بازاریابی حرفه‌ای مجموعه‌ای از فعالیت‌های منسجم برای شناخت بازار،
خلق ارزش، انتقال ارزش و دریافت ارزش از مشتری است.

بازاریابی با تبلیغات یکسان نیست. تبلیغات فقط یکی از ابزارهای
ارتباطات بازاریابی محسوب می‌شود. بازاریابی از شناخت مسئله مشتری
شروع می‌شود و تا طراحی محصول، قیمت‌گذاری، توزیع، ارتباطات،
تجربه مشتری و مدیریت رابطه ادامه پیدا می‌کند.

در رویکرد بازارگرا، سازمان به جای اینکه صرفاً محصولی را تولید
و سپس برای فروش آن مشتری پیدا کند، ابتدا بازار و نیاز مشتری را
درک می‌کند و سپس پیشنهاد ارزش خود را طراحی می‌کند.

اصل مهم:
بازاریابی موفق فقط فروش بیشتر نیست؛ بلکه ایجاد ارزش اقتصادی
و رابطه پایدار با مشتری است.
""",
            "keywords": [
                "Marketing",
                "Market Orientation",
                "Value Creation",
                "Customer Value",
            ],
        },

        {
            "id": "lesson_01_02",
            "title": "نیاز، خواسته، تقاضا و ارزش",
            "content": """
نیاز یک کمبود یا مسئله اساسی انسانی است.
خواسته شکل مشخصی است که فرد برای برطرف کردن نیاز انتخاب می‌کند.
تقاضا زمانی شکل می‌گیرد که خواسته با قدرت خرید و تمایل به پرداخت
همراه شود.

ارزش مشتری حاصل مقایسه منافع ادراک‌شده با هزینه‌های ادراک‌شده است.
این هزینه فقط قیمت نیست و می‌تواند شامل زمان، ریسک، انرژی،
هزینه جست‌وجو و هزینه روانی نیز باشد.

به همین دلیل دو محصول با قیمت مشابه می‌توانند ارزش ادراک‌شده
کاملاً متفاوتی ایجاد کنند.

بازاریاب حرفه‌ای باید بتواند پاسخ دهد:
مشتری دقیقاً چه مشکلی دارد؟
چه نتیجه‌ای برای او ارزشمند است؟
چه چیزی مانع خرید می‌شود؟
و چرا باید پیشنهاد ما را نسبت به جایگزین انتخاب کند؟
""",
            "keywords": [
                "Need",
                "Want",
                "Demand",
                "Customer Value",
                "Perceived Value",
            ],
        },

        {
            "id": "lesson_01_03",
            "title": "بازارگرایی و Customer-Centricity",
            "content": """
Customer-Centricity یعنی مشتری در مرکز تصمیم‌گیری سازمان قرار گیرد،
اما این مفهوم به معنی انجام هر خواسته مشتری نیست.

سازمان مشتری‌محور باید میان ارزش مشتری، سودآوری، قابلیت سازمان،
رقابت و اهداف بلندمدت تعادل ایجاد کند.

بازارگرایی معمولاً شامل سه قابلیت مهم است:
شناخت اطلاعات بازار،
انتشار اطلاعات در سازمان،
و پاسخ هماهنگ سازمان به اطلاعات بازار.

در یک سازمان بازارگرا، بازاریابی فقط وظیفه واحد Marketing نیست.
محصول، فروش، مالی، عملیات، خدمات و مدیریت ارشد باید در خلق
تجربه مشتری نقش داشته باشند.
""",
            "keywords": [
                "Market Orientation",
                "Customer Centricity",
                "Customer Experience",
            ],
        },
    ],

    "chapter_02": [

        {
            "id": "lesson_02_01",
            "title": "فرآیند تدوین استراتژی بازاریابی",
            "content": """
استراتژی بازاریابی باید از استراتژی کسب‌وکار جدا نباشد.

فرآیند حرفه‌ای معمولاً شامل:
تحلیل وضعیت،
تعریف مسئله،
تعیین اهداف،
انتخاب بازار هدف،
تدوین ارزش پیشنهادی،
انتخاب جایگاه،
طراحی برنامه اجرایی،
تخصیص منابع،
اندازه‌گیری و اصلاح است.

تحلیل SWOT به تنهایی استراتژی نیست.
SWOT صرفاً ابزاری برای سازمان‌دهی برخی یافته‌های داخلی و خارجی
است و باید به تصمیم مشخص تبدیل شود.

استراتژی زمانی معنا دارد که انتخاب ایجاد کند؛
یعنی مشخص کند سازمان چه کاری را انجام می‌دهد و چه کاری را انجام نمی‌دهد.
""",
            "keywords": [
                "Marketing Strategy",
                "SWOT",
                "Strategic Planning",
            ],
        },

        {
            "id": "lesson_02_02",
            "title": "مزیت رقابتی و دفاع‌پذیری",
            "content": """
مزیت رقابتی زمانی اهمیت دارد که برای مشتری ارزش ایجاد کند
و رقبا نتوانند به‌سادگی آن را تقلید یا خنثی کنند.

منابع مزیت می‌توانند شامل:
برند،
داده،
شبکه توزیع،
فناوری،
هزینه پایین،
سرمایه انسانی،
رابطه با مشتری،
اثر شبکه‌ای،
یا قابلیت سازمانی باشند.

مزیت رقابتی پایدار معمولاً نتیجه یک ویژگی منفرد نیست.
ترکیب چند قابلیت که در کنار یکدیگر قرار گرفته‌اند،
می‌تواند ساختاری ایجاد کند که تقلید از آن دشوار باشد.
""",
            "keywords": [
                "Competitive Advantage",
                "Defensibility",
                "Capabilities",
            ],
        },

        {
            "id": "lesson_02_03",
            "title": "اهداف بازاریابی و SMART",
            "content": """
هدف بازاریابی باید قابل اندازه‌گیری و مرتبط با نتیجه کسب‌وکار باشد.

اهداف SMART یعنی:
مشخص،
قابل اندازه‌گیری،
قابل دستیابی،
مرتبط،
و زمان‌مند.

مثلاً «افزایش فروش» هدف ضعیفی است.
اما «افزایش نرخ تبدیل لیدهای واجد شرایط از ۸ به ۱۰ درصد
در سه‌ماهه آینده» هدف دقیق‌تری است.

در مدیریت حرفه‌ای باید میان:
Business Outcome،
Marketing Outcome،
Channel Metric
و Activity Metric
تفاوت قائل شد.

تعداد پست‌ها یک Activity Metric است؛
درآمد حاصل از مشتریان جذب‌شده یک Business Outcome است.
""",
            "keywords": [
                "SMART",
                "Marketing Objectives",
                "Business Outcome",
                "KPI",
            ],
        },
    ],

    "chapter_03": [

        {
            "id": "lesson_03_01",
            "title": "مدل تصمیم‌گیری مصرف‌کننده",
            "content": """
فرآیند کلاسیک تصمیم خرید می‌تواند شامل:
تشخیص مسئله،
جست‌وجوی اطلاعات،
ارزیابی گزینه‌ها،
تصمیم خرید،
و رفتار پس از خرید باشد.

اما همه خریدها این مسیر را با یک شدت طی نمی‌کنند.
در خریدهای تکراری و کم‌درگیری، تصمیم می‌تواند بسیار سریع باشد.

بازاریاب باید سطح درگیری، ریسک ادراک‌شده، پیچیدگی محصول،
تجربه قبلی و هزینه تغییر را در نظر بگیرد.

یکی از اشتباهات رایج این است که برای همه مشتریان
یک پیام و یک قیف خرید طراحی شود.
""",
            "keywords": [
                "Consumer Behavior",
                "Decision Process",
                "Involvement",
            ],
        },

        {
            "id": "lesson_03_02",
            "title": "اقتصاد رفتاری در بازاریابی",
            "content": """
اقتصاد رفتاری نشان می‌دهد انسان همیشه تصمیم‌های کاملاً عقلایی
و مبتنی بر محاسبه کامل انجام نمی‌دهد.

مفاهیمی مانند:
Anchoring،
Loss Aversion،
Social Proof،
Scarcity،
Framing،
Default Effect
و Choice Architecture
می‌توانند بر رفتار تصمیم‌گیری اثر بگذارند.

استفاده حرفه‌ای از این مفاهیم باید اخلاقی باشد.
هدف نباید فریب مشتری باشد، بلکه باید اصطکاک تصمیم‌گیری
کاهش پیدا کند و اطلاعات به شکل قابل فهم ارائه شود.
""",
            "keywords": [
                "Behavioral Economics",
                "Anchoring",
                "Loss Aversion",
                "Social Proof",
            ],
        },

        {
            "id": "lesson_03_03",
            "title": "روان‌شناسی قیمت و انتخاب",
            "content": """
قیمت فقط یک عدد اقتصادی نیست؛ بلکه یک سیگنال است.

مشتری ممکن است قیمت را به عنوان نشانه کیفیت،
اعتبار، ریسک یا جایگاه اجتماعی تفسیر کند.

Framing قیمت، بسته‌بندی پیشنهاد،
مقایسه گزینه‌ها،
و ترتیب نمایش محصولات
می‌تواند ادراک مشتری را تغییر دهد.

با این حال اثرگذاری واقعی باید با داده و آزمایش بررسی شود،
نه با فرضیات بازاریاب.
""",
            "keywords": [
                "Pricing Psychology",
                "Framing",
                "Choice Architecture",
            ],
        },
    ],

    "chapter_04": [

        {
            "id": "lesson_04_01",
            "title": "فرآیند تحقیقات بازار",
            "content": """
تحقیقات بازار حرفه‌ای با تعریف دقیق مسئله آغاز می‌شود.

مراحل اصلی:
تعریف مسئله،
تعیین اهداف تحقیق،
انتخاب روش،
طراحی ابزار،
نمونه‌گیری،
جمع‌آوری داده،
تحلیل،
تفسیر،
و تبدیل یافته‌ها به تصمیم مدیریتی.

اگر مسئله اشتباه تعریف شود، حتی بهترین داده‌ها نیز
می‌توانند به تصمیم اشتباه منجر شوند.
""",
            "keywords": [
                "Market Research",
                "Research Design",
                "Problem Definition",
            ],
        },

        {
            "id": "lesson_04_02",
            "title": "داده اولیه و ثانویه",
            "content": """
Primary Data داده‌ای است که برای مسئله تحقیق فعلی
به صورت مستقیم جمع‌آوری می‌شود.

Secondary Data قبلاً توسط سازمان یا منبع دیگری جمع‌آوری شده است.

روش‌های Primary Data شامل:
مصاحبه،
Focus Group،
Survey،
Observation،
Experiment
و تحلیل رفتار واقعی کاربران است.

در تحقیقات حرفه‌ای باید کیفیت، اعتبار، سوگیری،
قابلیت تعمیم و تازگی داده بررسی شود.
""",
            "keywords": [
                "Primary Data",
                "Secondary Data",
                "Survey",
                "Interview",
            ],
        },

        {
            "id": "lesson_04_03",
            "title": "Customer Insight",
            "content": """
Insight صرفاً یک داده یا جمله مشتری نیست.

Insight زمانی ارزشمند است که:
یک الگوی معنادار را آشکار کند،
علت یا انگیزه مهمی را نشان دهد،
و بتواند تصمیم بازاریابی را تغییر دهد.

مثلاً «مشتریان از قیمت ناراضی‌اند» یک Observation است.

اما اگر مشخص شود مشتریان حاضرند قیمت بیشتری بپردازند
به شرط اینکه ریسک استفاده کاهش یابد، یک Insight عملیاتی‌تر
به دست آمده است.

هدف تحقیقات بازار باید تبدیل Data به Information
و سپس تبدیل Information به Insight و Action باشد.
""",
            "keywords": [
                "Customer Insight",
                "Data",
                "Information",
                "Actionable Insight",
            ],
        },
    ],

    "chapter_05": [

        {
            "id": "lesson_05_01",
            "title": "Segmentation",
            "content": """
Segmentation یعنی تقسیم بازار ناهمگن به گروه‌هایی
که از نظر نیاز، رفتار یا ویژگی‌های مرتبط تفاوت معنادار دارند.

معیارها می‌توانند:
جمعیت‌شناختی،
جغرافیایی،
روان‌شناختی،
رفتاری،
نیازمحور،
ارزش‌محور
یا ترکیبی باشند.

بخش‌بندی خوب فقط گروه‌های متفاوت ایجاد نمی‌کند؛
بلکه باید از نظر بازاریابی قابل استفاده باشد.
""",
            "keywords": [
                "Segmentation",
                "Behavioral Segmentation",
                "Needs-Based Segmentation",
            ],
        },

        {
            "id": "lesson_05_02",
            "title": "Targeting",
            "content": """
پس از بخش‌بندی، سازمان باید تصمیم بگیرد کدام بخش‌ها
برای تمرکز منابع مناسب‌تر هستند.

معیارهای Targeting می‌تواند شامل:
اندازه بازار،
رشد،
سودآوری،
شدت رقابت،
دسترسی،
تناسب با قابلیت‌های سازمان
و جذابیت استراتژیک باشد.

بزرگ‌ترین بازار همیشه بهترین بازار هدف نیست.
""",
            "keywords": [
                "Targeting",
                "Market Attractiveness",
                "Profitability",
            ],
        },

        {
            "id": "lesson_05_03",
            "title": "Positioning و Value Proposition",
            "content": """
Positioning جایگاه مطلوبی است که برند می‌خواهد
در ذهن بازار هدف نسبت به گزینه‌های رقیب داشته باشد.

Value Proposition باید روشن کند:
برای چه کسی؟
چه مسئله‌ای؟
چه منفعتی؟
چرا ما؟
و چرا اکنون؟

Positioning بدون Evidence ضعیف است.
اگر برند ادعای کیفیت، سرعت یا تخصص می‌کند،
باید شواهد قابل باور ارائه دهد.
""",
            "keywords": [
                "Positioning",
                "Value Proposition",
                "Brand Positioning",
            ],
        },
    ],

    "chapter_06": [

        {
            "id": "lesson_06_01",
            "title": "تحلیل رقبا",
            "content": """
تحلیل رقابتی فقط بررسی قیمت رقبا نیست.

باید:
پیشنهاد ارزش،
محصول،
قیمت،
کانال،
تجربه مشتری،
برند،
پیام،
فناوری،
مدل درآمد،
و نقاط ضعف
بررسی شوند.

رقیب واقعی همیشه شرکتی نیست که محصول مشابه دارد.
گاهی جایگزین مشتری، مهم‌ترین تهدید رقابتی است.
""",
            "keywords": [
                "Competitive Analysis",
                "Competitor",
                "Substitute",
            ],
        },

        {
            "id": "lesson_06_02",
            "title": "Porter Five Forces",
            "content": """
مدل پنج نیروی پورتر شامل:
رقابت موجود،
تهدید تازه‌واردها،
قدرت تأمین‌کنندگان،
قدرت خریداران،
و تهدید محصولات جایگزین است.

هدف مدل پیش‌بینی مستقیم فروش نیست.
هدف شناخت ساختار اقتصادی صنعت و میزان جذابیت آن است.
""",
            "keywords": [
                "Porter",
                "Five Forces",
                "Industry Analysis",
            ],
        },

        {
            "id": "lesson_06_03",
            "title": "Competitive Intelligence",
            "content": """
Competitive Intelligence یعنی جمع‌آوری و تحلیل قانونی
و اخلاقی اطلاعات برای بهبود تصمیم‌های رقابتی.

منابع می‌توانند:
وب‌سایت رقبا،
گزارش‌های عمومی،
قیمت‌های منتشرشده،
آگهی‌های استخدام،
نظرات مشتریان،
گزارش‌های صنعتی
و داده‌های بازار باشند.

هدف Intelligence تولید Insight است، نه جمع‌کردن فایل‌های بی‌مصرف.
""",
            "keywords": [
                "Competitive Intelligence",
                "Market Intelligence",
                "Benchmarking",
            ],
        },
    ],

    "chapter_07": [

        {
            "id": "lesson_07_01",
            "title": "Product-Market Fit",
            "content": """
Product-Market Fit زمانی مطرح می‌شود که محصول بتواند
یک مسئله واقعی بازار را به شکلی مطلوب حل کند
و نشانه‌های پایدار تقاضا ایجاد شود.

PMF با فروش اولیه یکی نیست.
باید تکرارپذیری، رضایت، Retention،
ارجاع مشتری و تناسب اقتصادی نیز بررسی شود.
""",
            "keywords": [
                "Product Market Fit",
                "PMF",
                "Retention",
            ],
        },

        {
            "id": "lesson_07_02",
            "title": "Go-to-Market Strategy",
            "content": """
GTM برنامه ورود یا گسترش محصول در بازار است.

اجزای مهم:
ICP،
Positioning،
Pricing،
Channel،
Sales Motion،
Marketing Motion،
Customer Success
و Metrics.

GTM باید مشخص کند محصول برای چه کسی،
با چه پیامی،
از چه کانالی،
و با چه مدل فروشی وارد بازار می‌شود.
""",
            "keywords": [
                "GTM",
                "Go To Market",
                "ICP",
            ],
        },

        {
            "id": "lesson_07_03",
            "title": "Product-Led Growth",
            "content": """
در Product-Led Growth خود محصول بخش مهمی از موتور جذب،
فعال‌سازی و تبدیل مشتری است.

نمونه‌ها:
Free Trial،
Freemium،
Self-Service،
In-App Onboarding
و Product Usage Signals.

PLG برای همه کسب‌وکارها مناسب نیست.
پیچیدگی محصول، قیمت، ریسک خرید و ساختار مشتری
باید بررسی شود.
""",
            "keywords": [
                "PLG",
                "Product Led Growth",
                "Freemium",
            ],
        },
    ],

    "chapter_08": [

        {
            "id": "lesson_08_01",
            "title": "استراتژی قیمت‌گذاری",
            "content": """
قیمت‌گذاری باید همزمان مشتری، هزینه، رقبا،
ارزش ایجادشده و اهداف کسب‌وکار را در نظر بگیرد.

روش‌های رایج:
Cost Plus،
Competition-Based،
Value-Based،
Dynamic Pricing
و Freemium.

قیمت‌گذاری مبتنی بر ارزش در شرایطی که
منافع اقتصادی یا عملکردی محصول قابل اثبات باشد
می‌تواند قدرت بیشتری داشته باشد.
""",
            "keywords": [
                "Pricing Strategy",
                "Value Based Pricing",
                "Dynamic Pricing",
            ],
        },

        {
            "id": "lesson_08_02",
            "title": "Price Elasticity",
            "content": """
کشش قیمتی تقاضا میزان حساسیت مقدار تقاضا
نسبت به تغییر قیمت را بررسی می‌کند.

اگر تقاضا نسبت به قیمت بسیار حساس باشد،
افزایش قیمت می‌تواند کاهش قابل‌توجهی در حجم تقاضا ایجاد کند.

اما تصمیم قیمت‌گذاری نباید صرفاً براساس Elasticity باشد.
Segment، رقبا، ارزش ادراک‌شده، ظرفیت و سودآوری نیز اهمیت دارند.
""",
            "keywords": [
                "Price Elasticity",
                "Demand",
                "Pricing",
            ],
        },

        {
            "id": "lesson_08_03",
            "title": "Revenue Management",
            "content": """
Revenue Management تلاش می‌کند قیمت و ظرفیت
را با تقاضای متفاوت در زمان‌ها و بخش‌های مختلف هماهنگ کند.

در صنایع دارای ظرفیت محدود مانند هتل، هواپیمایی،
حمل‌ونقل و برخی خدمات، این موضوع اهمیت ویژه دارد.

هدف صرفاً افزایش قیمت نیست؛
بلکه بهینه‌سازی درآمد و سود در طول زمان است.
""",
            "keywords": [
                "Revenue Management",
                "Yield Management",
                "Dynamic Pricing",
            ],
        },
    ],

    "chapter_09": [

        {
            "id": "lesson_09_01",
            "title": "Brand Identity و Brand Image",
            "content": """
Brand Identity چیزی است که سازمان می‌خواهد برند را بر اساس آن
تعریف و ارائه کند.

Brand Image برداشت واقعی بازار از برند است.

این دو ممکن است کاملاً یکسان نباشند.
مدیریت برند حرفه‌ای باید فاصله میان Identity و Image را شناسایی کند.

هویت برند شامل عناصر بصری نیست.
ارزش‌ها، شخصیت، وعده، لحن و تجربه نیز بخشی از آن هستند.
""",
            "keywords": [
                "Brand Identity",
                "Brand Image",
                "Brand Strategy",
            ],
        },

        {
            "id": "lesson_09_02",
            "title": "Brand Equity",
            "content": """
Brand Equity ارزش افزوده‌ای است که برند به محصول یا خدمت اضافه می‌کند.

آگاهی از برند،
تداعی‌های برند،
کیفیت ادراک‌شده،
وفاداری
و سایر دارایی‌های برند
می‌توانند در ایجاد Brand Equity نقش داشته باشند.

برند قوی می‌تواند هزینه جذب را کاهش،
تمایل به پرداخت را افزایش
و حساسیت مشتری به رقابت را کاهش دهد.
""",
            "keywords": [
                "Brand Equity",
                "Brand Awareness",
                "Brand Loyalty",
            ],
        },

        {
            "id": "lesson_09_03",
            "title": "Brand Experience",
            "content": """
تجربه برند از مجموع تعاملات مشتری با برند شکل می‌گیرد.

وب‌سایت،
فروشنده،
بسته‌بندی،
اپلیکیشن،
خدمات پس از فروش،
شبکه اجتماعی
و حتی نحوه پاسخ‌گویی به شکایت
می‌توانند بخشی از تجربه برند باشند.

برند وعده است؛ تجربه باید آن وعده را اثبات کند.
""",
            "keywords": [
                "Brand Experience",
                "Customer Experience",
                "CX",
            ],
        },
    ],

    "chapter_10": [

        {
            "id": "lesson_10_01",
            "title": "ماهیت بازاریابی B2B",
            "content": """
در B2B تصمیم خرید معمولاً چندنفره‌تر، طولانی‌تر
و مبتنی بر ریسک سازمانی است.

Buying Center ممکن است شامل:
کاربر،
Influencer،
Buyer،
Decision Maker،
Gatekeeper
و سایر نقش‌ها باشد.

بنابراین پیام بازاریابی باید برای نقش‌های مختلف
ارزش متفاوتی ایجاد کند.
""",
            "keywords": [
                "B2B",
                "Buying Center",
                "Decision Maker",
            ],
        },

        {
            "id": "lesson_10_02",
            "title": "Account-Based Marketing",
            "content": """
ABM به جای تمرکز صرف بر تعداد زیاد Lead،
روی حساب‌های مشخص و باارزش تمرکز می‌کند.

فرآیند:
انتخاب حساب هدف،
تحقیق حساب،
شناسایی ذی‌نفعان،
طراحی پیام،
اجرای کمپین،
Sales Alignment
و اندازه‌گیری.

ABM نیازمند همکاری نزدیک Marketing و Sales است.
""",
            "keywords": [
                "ABM",
                "Account Based Marketing",
                "B2B Marketing",
            ],
        },

        {
            "id": "lesson_10_03",
            "title": "Lead Generation و Demand Generation",
            "content": """
Lead Generation تمرکز بیشتری بر شناسایی و ثبت سرنخ دارد.

Demand Generation گسترده‌تر است و تلاش می‌کند
تقاضا، آگاهی، علاقه و آمادگی بازار را ایجاد کند.

یک سازمان ممکن است Lead زیادی داشته باشد
اما Demand واقعی کمی داشته باشد.

تمرکز حرفه‌ای باید روی کیفیت و ارزش اقتصادی
سرنخ‌ها باشد، نه فقط تعداد فرم‌های ثبت‌شده.
""",
            "keywords": [
                "Lead Generation",
                "Demand Generation",
                "Pipeline",
            ],
        },
    ],

    "chapter_11": [

        {
            "id": "lesson_11_01",
            "title": "Discovery و نیازسنجی فروش",
            "content": """
فروش حرفه‌ای با ارائه محصول شروع نمی‌شود.

در مرحله Discovery باید:
مسئله،
پیامد مسئله،
نیاز،
اولویت،
فرآیند تصمیم،
بودجه،
زمان‌بندی
و ذی‌نفعان شناسایی شوند.

فروشنده حرفه‌ای بیشتر از آنکه سخنرانی کند،
سؤال درست می‌پرسد.
""",
            "keywords": [
                "Discovery",
                "Needs Analysis",
                "Consultative Selling",
            ],
        },

        {
            "id": "lesson_11_02",
            "title": "Qualification",
            "content": """
Qualification یعنی بررسی اینکه آیا یک فرصت فروش
ارزش سرمایه‌گذاری زمان و منابع فروش را دارد یا خیر.

چارچوب‌هایی مانند BANT، MEDDIC و مدل‌های مشابه
می‌توانند به ساختاردهی فرآیند کمک کنند.

اما هیچ Framework نباید بدون تطبیق با صنعت،
چرخه فروش و مدل کسب‌وکار استفاده شود.
""",
            "keywords": [
                "Qualification",
                "BANT",
                "MEDDIC",
            ],
        },

        {
            "id": "lesson_11_03",
            "title": "Sales Enablement و Closing",
            "content": """
Sales Enablement یعنی فراهم کردن محتوا، آموزش،
ابزار، داده و فرآیند لازم برای افزایش اثربخشی فروش.

Closing نباید یک فشار ناگهانی برای خرید باشد.
اگر Qualification، Discovery و Value Communication
به درستی انجام شده باشند، Closing بیشتر به
رفع ابهام و تصمیم‌گیری کمک می‌کند.
""",
            "keywords": [
                "Sales Enablement",
                "Closing",
                "Sales Process",
            ],
        },
    ],

    "chapter_12": [

        {
            "id": "lesson_12_01",
            "title": "CRM به عنوان سیستم مدیریتی",
            "content": """
CRM فقط نرم‌افزار نیست.

CRM یک رویکرد مدیریتی برای شناخت،
جذب،
خدمت‌رسانی،
حفظ
و توسعه رابطه با مشتری است.

نرم‌افزار CRM زمانی ارزشمند است که فرآیند،
داده و رفتار سازمانی مناسب پشت آن وجود داشته باشد.
""",
            "keywords": [
                "CRM",
                "Customer Relationship Management",
            ],
        },

        {
            "id": "lesson_12_02",
            "title": "Retention و Churn",
            "content": """
Retention نشان می‌دهد چه مقدار از مشتریان
در طول زمان باقی می‌مانند.

Churn نشان‌دهنده از دست دادن مشتری یا اشتراک است.

کاهش Churn در بسیاری از مدل‌های کسب‌وکار
می‌تواند اثر اقتصادی بیشتری از افزایش جزئی Acquisition داشته باشد،
زیرا مشتری حفظ‌شده معمولاً هزینه جذب مجدد ندارد
و امکان خریدهای آینده وجود دارد.
""",
            "keywords": [
                "Retention",
                "Churn",
                "Customer Loyalty",
            ],
        },

        {
            "id": "lesson_12_03",
            "title": "Customer Lifetime Value",
            "content": """
CLV یا Customer Lifetime Value ارزش اقتصادی مورد انتظار
از رابطه مشتری با سازمان در طول دوره رابطه است.

در مدل‌های ساده می‌توان درآمد یا حاشیه سود مورد انتظار،
تکرار خرید، طول رابطه و هزینه‌های مرتبط را در نظر گرفت.

CLV نباید به عنوان یک عدد قطعی آینده تفسیر شود.
این شاخص به فرضیات و کیفیت داده وابسته است.
""",
            "keywords": [
                "CLV",
                "LTV",
                "Customer Lifetime Value",
            ],
        },
    ],

    "chapter_13": [

        {
            "id": "lesson_13_01",
            "title": "Digital Marketing Architecture",
            "content": """
بازاریابی دیجیتال یک کانال منفرد نیست.

معماری دیجیتال می‌تواند شامل:
Owned Media،
Paid Media،
Earned Media،
Search،
Social،
Email،
Content،
Website،
Marketplace
و CRM باشد.

هدف، ساخت یک سیستم یکپارچه است؛
نه تولید فعالیت‌های پراکنده در ده‌ها پلتفرم.
""",
            "keywords": [
                "Digital Marketing",
                "Owned Media",
                "Paid Media",
                "Earned Media",
            ],
        },

        {
            "id": "lesson_13_02",
            "title": "SEO و Search Marketing",
            "content": """
SEO مجموعه‌ای از فعالیت‌ها برای بهبود قابلیت دیده‌شدن
و دسترسی ارگانیک محتوا در موتورهای جست‌وجو است.

عناصر مهم:
Technical SEO،
Content،
Search Intent،
Internal Linking،
Authority
و تجربه کاربر.

بازاریابی جست‌وجو باید از Keyword Matching فراتر رود
و مسئله واقعی کاربر را هدف قرار دهد.
""",
            "keywords": [
                "SEO",
                "Search Intent",
                "Technical SEO",
            ],
        },

        {
            "id": "lesson_13_03",
            "title": "Performance Marketing",
            "content": """
Performance Marketing بر اندازه‌گیری نتیجه و بهینه‌سازی
سرمایه‌گذاری رسانه‌ای تمرکز دارد.

شاخص‌ها:
CTR،
CPC،
CPM،
CVR،
CPA،
CAC،
ROAS
و Revenue.

اما بهینه‌سازی صرفاً براساس آخرین کلیک می‌تواند
تصویر ناقصی از ارزش کانال ایجاد کند.
""",
            "keywords": [
                "Performance Marketing",
                "CTR",
                "CPA",
                "ROAS",
            ],
        },
    ],

    "chapter_14": [

        {
            "id": "lesson_14_01",
            "title": "Growth Funnel",
            "content": """
مدل Growth Funnel معمولاً مراحل:
Acquisition،
Activation،
Retention،
Revenue
و Referral
را بررسی می‌کند.

تمرکز Growth Marketing روی پیدا کردن
محدودیت اصلی سیستم رشد است.

اگر Acquisition خوب باشد ولی Activation ضعیف باشد،
افزایش بودجه تبلیغات فقط افراد بیشتری را وارد
یک سیستم ناکارآمد می‌کند.
""",
            "keywords": [
                "Growth Marketing",
                "AARRR",
                "Funnel",
            ],
        },

        {
            "id": "lesson_14_02",
            "title": "Conversion Rate Optimization",
            "content": """
CRO یعنی افزایش احتمال انجام اقدام مطلوب
بدون اتکا به افزایش صرف ترافیک.

عوامل:
پیام،
اعتماد،
طراحی،
اصطکاک،
سرعت،
Offer،
CTA
و تجربه کاربر
می‌توانند بر Conversion اثر بگذارند.

بهبود CRO باید با آزمایش کنترل‌شده انجام شود.
""",
            "keywords": [
                "CRO",
                "Conversion Rate",
                "CTA",
            ],
        },

        {
            "id": "lesson_14_03",
            "title": "Growth Loops",
            "content": """
Growth Loop برخلاف Funnel فقط یک مسیر خطی نیست.

در Loop، خروجی یک مشتری یا کاربر
می‌تواند ورودی مشتری یا کاربر بعدی شود.

نمونه:
Referral،
User Generated Content،
Network Effect
و Product Sharing.

Loopهای قدرتمند می‌توانند رشد را به صورت
تاحدی خودتقویت‌شونده کنند.
""",
            "keywords": [
                "Growth Loop",
                "Referral",
                "Network Effect",
            ],
        },
    ],

    "chapter_15": [

        {
            "id": "lesson_15_01",
            "title": "Marketing KPI",
            "content": """
KPI باید به هدف مشخص متصل باشد.

شاخص‌های مهم:
CAC،
CLV،
Conversion Rate،
Retention،
Churn،
ROAS،
ROI،
Revenue،
Pipeline،
Share of Voice
و Brand Metrics.

تعداد Followers یا Likes لزوماً KPI کسب‌وکار نیست.
شاخص باید به تصمیم و نتیجه قابل‌توجه متصل باشد.
""",
            "keywords": [
                "KPI",
                "Marketing Analytics",
                "Metrics",
            ],
        },

        {
            "id": "lesson_15_02",
            "title": "Attribution",
            "content": """
Attribution تلاش می‌کند مشخص کند
کدام Touchpointها در مسیر تبدیل مشتری نقش داشته‌اند.

مدل‌های ساده شامل:
First Touch،
Last Touch
و Linear Attribution هستند.

مدل‌های پیشرفته‌تر می‌توانند از داده و مدل‌سازی
برای تخمین نقش کانال‌ها استفاده کنند.

هیچ مدل Attribution به‌تنهایی حقیقت کامل رفتار مشتری نیست.
""",
            "keywords": [
                "Attribution",
                "First Touch",
                "Last Touch",
                "Multi Touch",
            ],
        },

        {
            "id": "lesson_15_03",
            "title": "Incrementality و Experimentation",
            "content": """
Incrementality بررسی می‌کند چه مقدار از نتیجه
واقعاً به دلیل فعالیت بازاریابی ایجاد شده است.

این موضوع با Attribution تفاوت دارد.

مثلاً اگر مشتری بدون تبلیغ نیز خرید می‌کرد،
نمی‌توان کل خرید را به تبلیغ نسبت داد.

آزمایش‌های کنترل‌شده، Holdout Groups و روش‌های
علّی می‌توانند به اندازه‌گیری Incrementality کمک کنند.
""",
            "keywords": [
                "Incrementality",
                "Experimentation",
                "Causal Inference",
            ],
        },

        {
            "id": "lesson_15_04",
            "title": "Cohort Analysis",
            "content": """
Cohort Analysis مشتریان را براساس زمان یا ویژگی مشترک
گروه‌بندی می‌کند و رفتار آنها را در طول زمان مقایسه می‌کند.

این روش برای بررسی:
Retention،
Revenue،
Churn،
Engagement
و رفتار خرید
بسیار مفید است.

Cohort Analysis کمک می‌کند رشد ظاهری را از رشد واقعی
کیفی تشخیص دهیم.
""",
            "keywords": [
                "Cohort Analysis",
                "Retention",
                "Customer Analytics",
            ],
        },
    ],

    "chapter_16": [

        {
            "id": "lesson_16_01",
            "title": "AI در بازاریابی",
            "content": """
هوش مصنوعی در بازاریابی می‌تواند برای:
Segmentation،
Prediction،
Personalization،
Content Generation،
Lead Scoring،
Customer Service،
Forecasting
و Optimization
استفاده شود.

اما AI جایگزین استراتژی نیست.

اگر مسئله کسب‌وکار مشخص نباشد،
AI فقط می‌تواند فعالیت‌های بیشتری تولید کند
بدون اینکه الزاماً ارزش بیشتری بسازد.
""",
            "keywords": [
                "AI Marketing",
                "Artificial Intelligence",
                "Predictive Marketing",
            ],
        },

        {
            "id": "lesson_16_02",
            "title": "Generative AI و Marketing Content",
            "content": """
Generative AI می‌تواند در ایده‌پردازی،
تحقیق اولیه،
تولید نسخه‌های مختلف محتوا،
خلاصه‌سازی،
تحلیل بازخورد
و Personalization کمک کند.

اما خروجی AI باید بررسی انسانی،
کنترل Brand Voice،
Fact Checking
و کنترل حقوقی و اخلاقی داشته باشد.

استفاده حرفه‌ای از AI یعنی افزایش کیفیت و سرعت،
نه تولید انبوه محتوای بی‌هویت.
""",
            "keywords": [
                "Generative AI",
                "AI Content",
                "Brand Voice",
            ],
        },

        {
            "id": "lesson_16_03",
            "title": "Predictive Marketing",
            "content": """
Predictive Marketing از داده تاریخی و مدل‌های تحلیلی
برای تخمین رفتار آینده استفاده می‌کند.

کاربردها:
Propensity Modeling،
Churn Prediction،
Lead Scoring،
Next Best Action
و Demand Forecasting.

مدل پیش‌بینی نباید با قطعیت اشتباه گرفته شود.
Prediction یک احتمال یا برآورد است، نه تضمین آینده.
""",
            "keywords": [
                "Predictive Marketing",
                "Propensity",
                "Churn Prediction",
            ],
        },

        {
            "id": "lesson_16_04",
            "title": "Machine Marketing و AI Customers",
            "content": """
با توسعه AI Agents، بخشی از فرآیند انتخاب محصول
ممکن است توسط سیستم‌های هوشمند انجام شود.

در این شرایط برندها فقط برای انسان‌ها بازاریابی نمی‌کنند؛
بلکه باید محتوای دقیق، قابل اعتماد، ساختاریافته و قابل تفسیر
برای سیستم‌های هوش مصنوعی نیز داشته باشند.

پژوهش‌های جدید بازاریابی این پدیده را
Machine Marketing می‌نامند و آن را به عنوان
یکی از حوزه‌های نوظهور رفتار بازار بررسی می‌کنند. 
این تغییر می‌تواند رابطه میان برند، انسان و واسطه‌های هوشمند
را دوباره تعریف کند.
""",
            "keywords": [
                "Machine Marketing",
                "AI Customers",
                "AI Agents",
            ],
        },
    ],

    "chapter_17": [

        {
            "id": "lesson_17_01",
            "title": "First-party Data",
            "content": """
First-party Data داده‌ای است که سازمان مستقیماً
از تعاملات خودش با مشتری یا کاربر به دست می‌آورد.

منابع:
Website،
CRM،
Purchase History،
App،
Email،
Customer Service
و Loyalty Program.

در بازاریابی مدرن، مالکیت و کیفیت داده اهمیت بیشتری پیدا کرده است.
گزارش‌های ۲۰۲۶ نیز First-party Data را یکی از قابلیت‌های
محوری برای فعال‌سازی و اندازه‌گیری بازاریابی می‌دانند. 
""",
            "keywords": [
                "First Party Data",
                "CRM Data",
                "Customer Data",
            ],
        },

        {
            "id": "lesson_17_02",
            "title": "Zero-party Data",
            "content": """
Zero-party Data اطلاعاتی است که مشتری به صورت آگاهانه
و مستقیم درباره ترجیحات، نیازها یا علایق خود اعلام می‌کند.

Preference Center،
Quiz،
Survey،
Profile،
و فرم‌های انتخاب ترجیحات
می‌توانند منابع آن باشند.

مزیت مهم آن این است که اطلاعات با Intent آشکار همراه است،
اما ارزش آن به کیفیت انگیزه و صداقت کاربر وابسته است.
""",
            "keywords": [
                "Zero Party Data",
                "Preference Data",
                "Consent",
            ],
        },

        {
            "id": "lesson_17_03",
            "title": "Privacy-first Marketing",
            "content": """
Privacy-first Marketing یعنی بازاریابی بر اساس
شفافیت، رضایت، حداقل‌گرایی داده و استفاده مسئولانه از اطلاعات.

در این رویکرد:
داده باید دلیل مشخص داشته باشد،
رضایت باید قابل فهم باشد،
استفاده باید متناسب با هدف باشد،
و دسترسی‌ها باید کنترل شوند.

در ۲۰۲۶، همگرایی AI و داده باعث شده
Data Governance اهمیت بیشتری پیدا کند؛
زیرا AI فقط به اندازه کیفیت و اعتبار داده‌ای که دریافت می‌کند
قابل اعتماد است. [oai_citation:1‡Experian](https://www.experian.com/marketing/resources/audience/digital-trends?utm_source=chatgpt.com)
""",
            "keywords": [
                "Privacy First",
                "Data Governance",
                "Consent",
            ],
        },

        {
            "id": "lesson_17_04",
            "title": "CDP و Marketing Technology",
            "content": """
Customer Data Platform یا CDP با هدف ایجاد دید یکپارچه‌تر
از داده‌های مشتری در نقاط تماس مختلف استفاده می‌شود.

MarTech Stack می‌تواند شامل:
CRM،
CDP،
Marketing Automation،
Analytics،
CMS،
Ad Platforms
و Customer Service Tools باشد.

چالش اصلی تعداد ابزارها نیست؛
بلکه کیفیت Integration، Data Governance و قابلیت تبدیل داده
به تصمیم است.
""",
            "keywords": [
                "CDP",
                "MarTech",
                "Marketing Automation",
            ],
        },
    ],

    "chapter_18": [

        {
            "id": "lesson_18_01",
            "title": "Omnichannel Marketing",
            "content": """
Omnichannel به معنای ایجاد تجربه هماهنگ
در نقاط تماس مختلف مشتری است.

کانال‌ها می‌توانند:
وب‌سایت،
اپلیکیشن،
فروشگاه،
شبکه اجتماعی،
Email،
Call Center
و Marketplace باشند.

Omnichannel با Multichannel یکسان نیست.
در Multichannel ممکن است کانال‌های زیادی وجود داشته باشند،
اما در Omnichannel تلاش می‌شود تجربه و داده میان آنها هماهنگ باشد.
""",
            "keywords": [
                "Omnichannel",
                "Multichannel",
                "Customer Journey",
            ],
        },

        {
            "id": "lesson_18_02",
            "title": "AEO و Search در عصر AI",
            "content": """
Answer Engine Optimization یا AEO به مجموعه فعالیت‌هایی
اشاره دارد که هدف آن افزایش احتمال دیده‌شدن و استفاده از
اطلاعات برند در محیط‌هایی است که پاسخ را مستقیماً تولید می‌کنند.

در عصر AI، کاربر ممکن است به جای مشاهده ده لینک،
یک پاسخ ترکیبی دریافت کند.

بنابراین ساختار محتوا،
اعتبار منبع،
دقت اطلاعات،
Entity Clarity،
FAQ،
Structured Content
و حضور معتبر برند اهمیت بیشتری پیدا می‌کند.

این حوزه در حال تکامل است و نباید با یک فرمول ثابت
یا وعده تضمینی رتبه‌گیری در AI اشتباه گرفته شود.
""",
            "keywords": [
                "AEO",
                "Answer Engine Optimization",
                "AI Search",
            ],
        },

        {
            "id": "lesson_18_03",
            "title": "Commerce Media",
            "content": """
Commerce Media مدل‌هایی را به وجود می‌آورد که در آن
داده و سیگنال خرید به فعالیت رسانه‌ای و تجاری متصل می‌شوند.

این حوزه دیگر فقط محدود به Retail نیست و در صنایع مختلف
در حال گسترش است.

مزیت اصلی زمانی ایجاد می‌شود که:
Audience،
Media،
Transaction
و Measurement
به شکل قابل اعتماد به یکدیگر متصل شوند. [oai_citation:2‡Experian](https://www.experian.com/marketing/resources/audience/digital-trends?utm_source=chatgpt.com)
""",
            "keywords": [
                "Commerce Media",
                "Retail Media",
                "Media Measurement",
            ],
        },

        {
            "id": "lesson_18_04",
            "title": "آینده بازاریابی",
            "content": """
بازاریابی آینده ترکیبی از انسان، داده، فناوری و اعتماد خواهد بود.

بازاریاب آینده باید علاوه بر مهارت‌های کلاسیک،
درک مناسبی از:
AI،
Analytics،
Customer Experience،
Experimentation،
Data Governance،
Automation،
Search،
Brand Strategy
و Business Strategy
داشته باشد.

روندهای جدید نشان می‌دهند AI در حال حرکت از مرحله آزمایش
به اجرای روزمره است و اتصال میان داده، فعال‌سازی و اندازه‌گیری
اهمیت بیشتری پیدا کرده است. [oai_citation:3‡Experian](https://www.experian.com/marketing/resources/audience/digital-trends?utm_source=chatgpt.com)

با این حال، فناوری بدون استراتژی ارزش پایدار ایجاد نمی‌کند.
مزیت واقعی زمانی ایجاد می‌شود که فناوری در خدمت
مسئله واقعی مشتری و هدف واقعی کسب‌وکار قرار گیرد.
""",
            "keywords": [
                "Future of Marketing",
                "AI",
                "Analytics",
                "Customer Experience",
                "Strategy",
            ],
        },
    ],
}


# ==========================================================
# Quiz Questions
# ==========================================================

MARKETING_QUIZ_QUESTIONS: dict[
    tuple[str, str],
    list[dict[str, Any]],
] = {

    (
        "chapter_01",
        "lesson_01_01",
    ): [
        {
            "id": "mk01_q01",
            "question": "بازاریابی حرفه‌ای از کدام نقطه شروع می‌شود؟",
            "options": [
                "شناخت مسئله و نیاز بازار",
                "افزایش تبلیغات",
                "کاهش قیمت",
                "افزایش تولید",
            ],
            "correct_answer": "شناخت مسئله و نیاز بازار",
        },
        {
            "id": "mk01_q02",
            "question": "کدام گزینه درباره بازاریابی صحیح‌تر است؟",
            "options": [
                "بازاریابی فراتر از تبلیغات است",
                "بازاریابی فقط تبلیغات است",
                "بازاریابی فقط فروش است",
                "بازاریابی فقط تحقیقات بازار است",
            ],
            "correct_answer": "بازاریابی فراتر از تبلیغات است",
        },
    ],

    (
        "chapter_01",
        "lesson_01_02",
    ): [
        {
            "id": "mk01_q03",
            "question": "تقاضا زمانی شکل می‌گیرد که خواسته با چه چیزی همراه شود؟",
            "options": [
                "قدرت خرید و تمایل به پرداخت",
                "تبلیغات تلویزیونی",
                "تعداد کارکنان",
                "تولید انبوه",
            ],
            "correct_answer": "قدرت خرید و تمایل به پرداخت",
        },
        {
            "id": "mk01_q04",
            "question": "کدام مورد می‌تواند بخشی از هزینه ادراک‌شده مشتری باشد؟",
            "options": [
                "زمان و ریسک",
                "فقط قیمت",
                "فقط مالیات",
                "فقط هزینه تولید",
            ],
            "correct_answer": "زمان و ریسک",
        },
    ],

    (
        "chapter_01",
        "lesson_01_03",
    ): [
        {
            "id": "mk01_q05",
            "question": "Customer-Centricity یعنی چه؟",
            "options": [
                "قرار دادن مشتری در مرکز تصمیم‌گیری",
                "انجام هر خواسته مشتری بدون محدودیت",
                "حذف سودآوری",
                "حذف رقبا",
            ],
            "correct_answer": "قرار دادن مشتری در مرکز تصمیم‌گیری",
        },
    ],

    (
        "chapter_02",
        "lesson_02_01",
    ): [
        {
            "id": "mk02_q01",
            "question": "کدام مورد بخشی از فرآیند استراتژی بازاریابی است؟",
            "options": [
                "انتخاب بازار هدف",
                "حذف تحلیل",
                "افزایش تصادفی تبلیغات",
                "تولید بدون تحقیق",
            ],
            "correct_answer": "انتخاب بازار هدف",
        },
    ],

    (
        "chapter_02",
        "lesson_02_02",
    ): [
        {
            "id": "mk02_q02",
            "question": "مزیت رقابتی زمانی ارزشمندتر است که چه ویژگی‌ای داشته باشد؟",
            "options": [
                "برای مشتری ارزش ایجاد کند و تقلید از آن دشوار باشد",
                "فقط قیمت بالاتری داشته باشد",
                "تبلیغات بیشتری داشته باشد",
                "نام طولانی‌تری داشته باشد",
            ],
            "correct_answer": "برای مشتری ارزش ایجاد کند و تقلید از آن دشوار باشد",
        },
    ],

    (
        "chapter_02",
        "lesson_02_03",
    ): [
        {
            "id": "mk02_q03",
            "question": "کدام مورد نمونه Business Outcome است؟",
            "options": [
                "افزایش درآمد",
                "تعداد پست منتشرشده",
                "تعداد جلسات تیم",
                "تعداد ایده‌های تبلیغاتی",
            ],
            "correct_answer": "افزایش درآمد",
        },
    ],

    (
        "chapter_03",
        "lesson_03_01",
    ): [
        {
            "id": "mk03_q01",
            "question": "کدام مورد بخشی از فرآیند کلاسیک تصمیم خرید است؟",
            "options": [
                "ارزیابی گزینه‌ها",
                "حذف رقبا",
                "حذف بازار",
                "حذف محصول",
            ],
            "correct_answer": "ارزیابی گزینه‌ها",
        },
    ],

    (
        "chapter_03",
        "lesson_03_02",
    ): [
        {
            "id": "mk03_q02",
            "question": "Loss Aversion به چه مفهومی اشاره دارد؟",
            "options": [
                "تمایل به حساسیت بیشتر نسبت به زیان",
                "تمایل به خرید بیشتر",
                "کاهش قیمت",
                "افزایش تبلیغات",
            ],
            "correct_answer": "تمایل به حساسیت بیشتر نسبت به زیان",
        },
    ],

    (
        "chapter_03",
        "lesson_03_03",
    ): [
        {
            "id": "mk03_q03",
            "question": "قیمت در ذهن مشتری می‌تواند چه نقشی داشته باشد؟",
            "options": [
                "سیگنال کیفیت و جایگاه",
                "فقط هزینه تولید",
                "فقط مالیات",
                "فقط هزینه حمل",
            ],
            "correct_answer": "سیگنال کیفیت و جایگاه",
        },
    ],

    (
        "chapter_04",
        "lesson_04_01",
    ): [
        {
            "id": "mk04_q01",
            "question": "اولین مرحله تحقیقات بازار چیست؟",
            "options": [
                "تعریف مسئله",
                "انتشار تبلیغ",
                "استخدام فروشنده",
                "تعیین شعار",
            ],
            "correct_answer": "تعریف مسئله",
        },
    ],

    (
        "chapter_04",
        "lesson_04_02",
    ): [
        {
            "id": "mk04_q02",
            "question": "کدام مورد نمونه Primary Data است؟",
            "options": [
                "مصاحبه مستقیم با مشتری برای تحقیق فعلی",
                "گزارش منتشرشده سال گذشته",
                "آمار رسمی منتشرشده",
                "مقاله دانشگاهی قدیمی",
            ],
            "correct_answer": "مصاحبه مستقیم با مشتری برای تحقیق فعلی",
        },
    ],

    (
        "chapter_04",
        "lesson_04_03",
    ): [
        {
            "id": "mk04_q03",
            "question": "Insight حرفه‌ای چه ویژگی‌ای دارد؟",
            "options": [
                "قابل تبدیل به تصمیم و اقدام باشد",
                "فقط یک عدد باشد",
                "فقط نظر مدیر باشد",
                "هیچ ارتباطی با تصمیم نداشته باشد",
            ],
            "correct_answer": "قابل تبدیل به تصمیم و اقدام باشد",
        },
    ],

    (
        "chapter_05",
        "lesson_05_01",
    ): [
        {
            "id": "mk05_q01",
            "question": "کدام مورد معیار Behavioral Segmentation است؟",
            "options": [
                "رفتار خرید",
                "شماره ثبت شرکت",
                "نام مدیر",
                "کد حسابداری",
            ],
            "correct_answer": "رفتار خرید",
        },
    ],

    (
        "chapter_05",
        "lesson_05_02",
    ): [
        {
            "id": "mk05_q02",
            "question": "Targeting به چه تصمیمی مربوط است؟",
            "options": [
                "انتخاب بخش‌های مناسب برای تمرکز",
                "طراحی لوگو",
                "انتخاب رنگ سازمانی",
                "ثبت شرکت",
            ],
            "correct_answer": "انتخاب بخش‌های مناسب برای تمرکز",
        },
    ],

    (
        "chapter_05",
        "lesson_05_03",
    ): [
        {
            "id": "mk05_q03",
            "question": "ترتیب صحیح STP چیست؟",
            "options": [
                "Segmentation → Targeting → Positioning",
                "Targeting → Segmentation → Positioning",
                "Positioning → Targeting → Segmentation",
                "Targeting → Positioning → Segmentation",
            ],
            "correct_answer": "Segmentation → Targeting → Positioning",
        },
    ],

    (
        "chapter_06",
        "lesson_06_01",
    ): [
        {
            "id": "mk06_q01",
            "question": "در تحلیل رقابتی کدام مورد اهمیت دارد؟",
            "options": [
                "پیشنهاد ارزش رقبا",
                "فقط رنگ لوگو",
                "فقط تعداد کارکنان",
                "فقط نام مدیرعامل",
            ],
            "correct_answer": "پیشنهاد ارزش رقبا",
        },
    ],

    (
        "chapter_06",
        "lesson_06_02",
    ): [
        {
            "id": "mk06_q02",
            "question": "کدام مورد جزء Five Forces پورتر است؟",
            "options": [
                "قدرت خریداران",
                "رنگ برند",
                "تعداد پست‌ها",
                "طراحی لوگو",
            ],
            "correct_answer": "قدرت خریداران",
        },
    ],

    (
        "chapter_06",
        "lesson_06_03",
    ): [
        {
            "id": "mk06_q03",
            "question": "هدف Competitive Intelligence چیست؟",
            "options": [
                "تبدیل اطلاعات رقابتی به بینش تصمیم‌ساز",
                "جمع‌آوری فایل بدون تحلیل",
                "کپی‌کردن تبلیغات",
                "حذف تحقیقات بازار",
            ],
            "correct_answer": "تبدیل اطلاعات رقابتی به بینش تصمیم‌ساز",
        },
    ],

    (
        "chapter_07",
        "lesson_07_01",
    ): [
        {
            "id": "mk07_q01",
            "question": "Product-Market Fit بیشتر به چه چیزی اشاره دارد؟",
            "options": [
                "تناسب واقعی محصول با نیاز بازار",
                "تعداد تبلیغات",
                "قیمت بالاتر",
                "تعداد کارکنان",
            ],
            "correct_answer": "تناسب واقعی محصول با نیاز بازار",
        },
    ],

    (
        "chapter_07",
        "lesson_07_02",
    ): [
        {
            "id": "mk07_q02",
            "question": "کدام مورد بخشی از GTM است؟",
            "options": [
                "Positioning و Channel",
                "فقط حسابداری",
                "فقط منابع انسانی",
                "فقط انبارداری",
            ],
            "correct_answer": "Positioning و Channel",
        },
    ],

    (
        "chapter_07",
        "lesson_07_03",
    ): [
        {
            "id": "mk07_q03",
            "question": "Product-Led Growth چه نقشی برای محصول قائل است؟",
            "options": [
                "محصول بخشی از موتور رشد است",
                "محصول هیچ نقشی ندارد",
                "فقط تبلیغات موتور رشد است",
                "فقط فروشنده موتور رشد است",
            ],
            "correct_answer": "محصول بخشی از موتور رشد است",
        },
    ],

    (
        "chapter_08",
        "lesson_08_01",
    ): [
        {
            "id": "mk08_q01",
            "question": "Value-Based Pricing بر چه چیزی تمرکز دارد؟",
            "options": [
                "ارزش ایجادشده برای مشتری",
                "فقط هزینه تولید",
                "فقط قیمت رقیب",
                "فقط هزینه تبلیغات",
            ],
            "correct_answer": "ارزش ایجادشده برای مشتری",
        },
    ],

    (
        "chapter_08",
        "lesson_08_02",
    ): [
        {
            "id": "mk08_q02",
            "question": "Price Elasticity چه چیزی را بررسی می‌کند؟",
            "options": [
                "حساسیت تقاضا نسبت به تغییر قیمت",
                "کیفیت برند",
                "تعداد کارکنان",
                "تعداد تبلیغات",
            ],
            "correct_answer": "حساسیت تقاضا نسبت به تغییر قیمت",
        },
    ],

    (
        "chapter_08",
        "lesson_08_03",
    ): [
        {
            "id": "mk08_q03",
            "question": "Revenue Management بیشتر برای چه چیزی استفاده می‌شود؟",
            "options": [
                "بهینه‌سازی درآمد با توجه به تقاضا و ظرفیت",
                "طراحی لوگو",
                "استخدام نیروی انسانی",
                "حسابداری مالی",
            ],
            "correct_answer": "بهینه‌سازی درآمد با توجه به تقاضا و ظرفیت",
        },
    ],

    (
        "chapter_09",
        "lesson_09_01",
    ): [
        {
            "id": "mk09_q01",
            "question": "Brand Image چیست؟",
            "options": [
                "برداشت واقعی مخاطب از برند",
                "هدف داخلی شرکت",
                "بودجه تبلیغات",
                "ساختار مالی",
            ],
            "correct_answer": "برداشت واقعی مخاطب از برند",
        },
    ],

    (
        "chapter_09",
        "lesson_09_02",
    ): [
        {
            "id": "mk09_q02",
            "question": "Brand Equity به چه مفهومی مربوط است؟",
            "options": [
                "ارزش افزوده ناشی از برند",
                "تعداد شعب",
                "هزینه حسابداری",
                "تعداد کارکنان",
            ],
            "correct_answer": "ارزش افزوده ناشی از برند",
        },
    ],

    (
        "chapter_09",
        "lesson_09_03",
    ): [
        {
            "id": "mk09_q03",
            "question": "کدام مورد می‌تواند بخشی از Brand Experience باشد؟",
            "options": [
                "خدمات پس از فروش",
                "فقط لوگو",
                "فقط نام برند",
                "فقط قیمت",
            ],
            "correct_answer": "خدمات پس از فروش",
        },
    ],

    (
        "chapter_10",
        "lesson_10_01",
    ): [
        {
            "id": "mk10_q01",
            "question": "در B2B تصمیم خرید معمولاً چه ویژگی‌ای دارد؟",
            "options": [
                "ممکن است چندنفره و پیچیده باشد",
                "همیشه فقط یک نفر تصمیم می‌گیرد",
                "هیچ ریسکی ندارد",
                "همیشه فوری است",
            ],
            "correct_answer": "ممکن است چندنفره و پیچیده باشد",
        },
    ],

    (
        "chapter_10",
        "lesson_10_02",
    ): [
        {
            "id": "mk10_q02",
            "question": "ABM بر چه چیزی تمرکز دارد؟",
            "options": [
                "حساب‌های هدف باارزش",
                "همه افراد بدون تفکیک",
                "فقط تبلیغات عمومی",
                "فقط فروشگاه فیزیکی",
            ],
            "correct_answer": "حساب‌های هدف باارزش",
        },
    ],

    (
        "chapter_10",
        "lesson_10_03",
    ): [
        {
            "id": "mk10_q03",
            "question": "Demand Generation نسبت به Lead Generation چه تفاوتی دارد؟",
            "options": [
                "روی ایجاد تقاضا و آمادگی بازار تمرکز گسترده‌تری دارد",
                "فقط فرم ثبت‌نام است",
                "فقط تبلیغات تلویزیونی است",
                "هیچ ارتباطی با بازار ندارد",
            ],
            "correct_answer": "روی ایجاد تقاضا و آمادگی بازار تمرکز گسترده‌تری دارد",
        },
    ],

    (
        "chapter_11",
        "lesson_11_01",
    ): [
        {
            "id": "mk11_q01",
            "question": "Discovery در فروش حرفه‌ای برای چیست؟",
            "options": [
                "شناخت مسئله و نیاز مشتری",
                "اعلام قیمت بدون سؤال",
                "بستن فوری قرارداد",
                "حذف اطلاعات",
            ],
            "correct_answer": "شناخت مسئله و نیاز مشتری",
        },
    ],

    (
        "chapter_11",
        "lesson_11_02",
    ): [
        {
            "id": "mk11_q02",
            "question": "Qualification چه چیزی را بررسی می‌کند؟",
            "options": [
                "تناسب و کیفیت فرصت فروش",
                "رنگ برند",
                "طراحی سایت",
                "حسابداری",
            ],
            "correct_answer": "تناسب و کیفیت فرصت فروش",
        },
    ],

    (
        "chapter_11",
        "lesson_11_03",
    ): [
        {
            "id": "mk11_q03",
            "question": "Sales Enablement شامل چیست؟",
            "options": [
                "آموزش، محتوا، ابزار و داده برای فروش",
                "فقط تبلیغات",
                "فقط حسابداری",
                "فقط طراحی لوگو",
            ],
            "correct_answer": "آموزش، محتوا، ابزار و داده برای فروش",
        },
    ],

    (
        "chapter_12",
        "lesson_12_01",
    ): [
        {
            "id": "mk12_q01",
            "question": "CRM فقط چیست؟",
            "options": [
                "CRM فقط نرم‌افزار نیست و رویکرد مدیریتی نیز هست",
                "فقط نرم‌افزار حسابداری است",
                "فقط ابزار تبلیغات است",
                "هیچ ارتباطی با مشتری ندارد",
            ],
            "correct_answer": "CRM فقط نرم‌افزار نیست و رویکرد مدیریتی نیز هست",
        },
    ],

    (
        "chapter_12",
        "lesson_12_02",
    ): [
        {
            "id": "mk12_q02",
            "question": "Churn به چه مفهومی اشاره دارد؟",
            "options": [
                "از دست دادن مشتری یا اشتراک",
                "جذب مشتری جدید",
                "افزایش برند",
                "افزایش تبلیغات",
            ],
            "correct_answer": "از دست دادن مشتری یا اشتراک",
        },
    ],

    (
        "chapter_12",
        "lesson_12_03",
    ): [
        {
            "id": "mk12_q03",
            "question": "CLV چه چیزی را بررسی می‌کند؟",
            "options": [
                "ارزش اقتصادی رابطه مشتری در طول زمان",
                "فقط اولین خرید",
                "فقط تعداد تبلیغات",
                "فقط هزینه سایت",
            ],
            "correct_answer": "ارزش اقتصادی رابطه مشتری در طول زمان",
        },
    ],

    (
        "chapter_13",
        "lesson_13_01",
    ): [
        {
            "id": "mk13_q01",
            "question": "کدام مورد Owned Media محسوب می‌شود؟",
            "options": [
                "وب‌سایت برند",
                "تبلیغ رقیب",
                "مقاله رسانه مستقل",
                "تبلیغ تلویزیونی خریداری‌شده",
            ],
            "correct_answer": "وب‌سایت برند",
        },
    ],

    (
        "chapter_13",
        "lesson_13_02",
    ): [
        {
            "id": "mk13_q02",
            "question": "Search Intent چیست؟",
            "options": [
                "هدف واقعی کاربر از جست‌وجو",
                "نام موتور جست‌وجو",
                "هزینه تبلیغ",
                "تعداد لینک‌ها",
            ],
            "correct_answer": "هدف واقعی کاربر از جست‌وجو",
        },
    ],

    (
        "chapter_13",
        "lesson_13_03",
    ): [
        {
            "id": "mk13_q03",
            "question": "ROAS چه چیزی را اندازه‌گیری می‌کند؟",
            "options": [
                "بازده هزینه تبلیغات",
                "ارزش طول عمر مشتری",
                "هزینه تولید",
                "حقوق کارکنان",
            ],
            "correct_answer": "بازده هزینه تبلیغات",
        },
    ],

    (
        "chapter_14",
        "lesson_14_01",
    ): [
        {
            "id": "mk14_q01",
            "question": "کدام مورد یکی از مراحل AARRR است؟",
            "options": [
                "Retention",
                "Accounting",
                "Recruitment",
                "Inventory",
            ],
            "correct_answer": "Retention",
        },
    ],

    (
        "chapter_14",
        "lesson_14_02",
    ): [
        {
            "id": "mk14_q02",
            "question": "هدف CRO چیست؟",
            "options": [
                "افزایش نرخ تبدیل",
                "افزایش هزینه",
                "کاهش داده",
                "حذف مشتری",
            ],
            "correct_answer": "افزایش نرخ تبدیل",
        },
    ],

    (
        "chapter_14",
        "lesson_14_03",
    ): [
        {
            "id": "mk14_q03",
            "question": "Growth Loop چه ویژگی‌ای دارد؟",
            "options": [
                "خروجی یک کاربر می‌تواند ورودی رشد بعدی شود",
                "کاملاً خطی است",
                "فقط برای حسابداری است",
                "هیچ ارتباطی با مشتری ندارد",
            ],
            "correct_answer": "خروجی یک کاربر می‌تواند ورودی رشد بعدی شود",
        },
    ],

    (
        "chapter_15",
        "lesson_15_01",
    ): [
        {
            "id": "mk15_q01",
            "question": "CAC به چه مفهومی اشاره دارد؟",
            "options": [
                "هزینه جذب مشتری",
                "ارزش برند",
                "نرخ کلیک",
                "هزینه انبار",
            ],
            "correct_answer": "هزینه جذب مشتری",
        },
    ],

    (
        "chapter_15",
        "lesson_15_02",
    ): [
        {
            "id": "mk15_q02",
            "question": "Last-Touch Attribution چه چیزی را برجسته می‌کند؟",
            "options": [
                "آخرین Touchpoint قبل از تبدیل",
                "اولین تعامل مشتری",
                "همه تعاملات به شکل برابر",
                "فقط تعاملات آفلاین",
            ],
            "correct_answer": "آخرین Touchpoint قبل از تبدیل",
        },
    ],

    (
        "chapter_15",
        "lesson_15_03",
    ): [
        {
            "id": "mk15_q03",
            "question": "Incrementality چه چیزی را بررسی می‌کند؟",
            "options": [
                "اثر واقعی و افزوده فعالیت بازاریابی",
                "فقط تعداد کلیک",
                "فقط تعداد نمایش",
                "فقط تعداد پست",
            ],
            "correct_answer": "اثر واقعی و افزوده فعالیت بازاریابی",
        },
    ],

    (
        "chapter_15",
        "lesson_15_04",
    ): [
        {
            "id": "mk15_q04",
            "question": "Cohort Analysis برای چه کاری مفید است؟",
            "options": [
                "مقایسه رفتار گروه‌های مشتری در طول زمان",
                "طراحی لوگو",
                "حسابداری مالی",
                "تعیین مالیات",
            ],
            "correct_answer": "مقایسه رفتار گروه‌های مشتری در طول زمان",
        },
    ],

    (
        "chapter_16",
        "lesson_16_01",
    ): [
        {
            "id": "mk16_q01",
            "question": "AI در بازاریابی چه کاربردی دارد؟",
            "options": [
                "پیش‌بینی رفتار و Personalization",
                "تضمین قطعی فروش",
                "حذف کامل استراتژی",
                "حذف کامل انسان",
            ],
            "correct_answer": "پیش‌بینی رفتار و Personalization",
        },
    ],

    (
        "chapter_16",
        "lesson_16_02",
    ): [
        {
            "id": "mk16_q02",
            "question": "در استفاده حرفه‌ای از Generative AI چه چیزی ضروری است؟",
            "options": [
                "Fact Checking و کنترل انسانی",
                "انتشار بدون بررسی",
                "حذف Brand Voice",
                "اعتماد کامل به هر خروجی",
            ],
            "correct_answer": "Fact Checking و کنترل انسانی",
        },
    ],

    (
        "chapter_16",
        "lesson_16_03",
    ): [
        {
            "id": "mk16_q03",
            "question": "Predictive Marketing چه کاری انجام می‌دهد؟",
            "options": [
                "برآورد رفتار احتمالی آینده",
                "تضمین رفتار آینده",
                "حذف داده",
                "حذف مشتری",
            ],
            "correct_answer": "برآورد رفتار احتمالی آینده",
        },
    ],

    (
        "chapter_16",
        "lesson_16_04",
    ): [
        {
            "id": "mk16_q04",
            "question": "Machine Marketing به چه تغییر مهمی اشاره دارد؟",
            "options": [
                "اهمیت رفتار سیستم‌های هوشمند در تصمیم خرید",
                "حذف کامل مشتری انسانی",
                "حذف برند",
                "حذف بازاریابی",
            ],
            "correct_answer": "اهمیت رفتار سیستم‌های هوشمند در تصمیم خرید",
        },
    ],

    (
        "chapter_17",
        "lesson_17_01",
    ): [
        {
            "id": "mk17_q01",
            "question": "First-party Data چیست؟",
            "options": [
                "داده جمع‌آوری‌شده مستقیم از تعامل با مشتری",
                "داده ساختگی",
                "داده بدون منبع",
                "همیشه داده خریداری‌شده",
            ],
            "correct_answer": "داده جمع‌آوری‌شده مستقیم از تعامل با مشتری",
        },
    ],

    (
        "chapter_17",
        "lesson_17_02",
    ): [
        {
            "id": "mk17_q02",
            "question": "Zero-party Data چه ویژگی‌ای دارد؟",
            "options": [
                "مشتری اطلاعات را آگاهانه و مستقیم اعلام می‌کند",
                "همیشه از رقیب خریداری می‌شود",
                "بدون رضایت جمع‌آوری می‌شود",
                "داده ساختگی است",
            ],
            "correct_answer": "مشتری اطلاعات را آگاهانه و مستقیم اعلام می‌کند",
        },
    ],

    (
        "chapter_17",
        "lesson_17_03",
    ): [
        {
            "id": "mk17_q03",
            "question": "Privacy-first Marketing بر چه چیزی تأکید دارد؟",
            "options": [
                "شفافیت، رضایت و استفاده مسئولانه از داده",
                "جمع‌آوری هرچه بیشتر داده",
                "نادیده گرفتن رضایت",
                "فروش آزاد اطلاعات",
            ],
            "correct_answer": "شفافیت، رضایت و استفاده مسئولانه از داده",
        },
    ],

    (
        "chapter_17",
        "lesson_17_04",
    ): [
        {
            "id": "mk17_q04",
            "question": "CDP چه هدفی دارد؟",
            "options": [
                "ایجاد دید یکپارچه‌تر از داده‌های مشتری",
                "جایگزینی کامل استراتژی",
                "فقط حسابداری",
                "فقط طراحی تبلیغ",
            ],
            "correct_answer": "ایجاد دید یکپارچه‌تر از داده‌های مشتری",
        },
    ],

    (
        "chapter_18",
        "lesson_18_01",
    ): [
        {
            "id": "mk18_q01",
            "question": "ویژگی اصلی Omnichannel چیست؟",
            "options": [
                "تجربه هماهنگ میان نقاط تماس",
                "استفاده فقط از یک کانال",
                "حذف CRM",
                "حذف فروشگاه",
            ],
            "correct_answer": "تجربه هماهنگ میان نقاط تماس",
        },
    ],

    (
        "chapter_18",
        "lesson_18_02",
    ): [
        {
            "id": "mk18_q02",
            "question": "AEO بیشتر با چه چیزی ارتباط دارد؟",
            "options": [
                "بهینه‌سازی حضور محتوا در محیط‌های پاسخ‌محور",
                "حسابداری",
                "مدیریت انبار",
                "تولید صنعتی",
            ],
            "correct_answer": "بهینه‌سازی حضور محتوا در محیط‌های پاسخ‌محور",
        },
    ],

    (
        "chapter_18",
        "lesson_18_03",
    ): [
        {
            "id": "mk18_q03",
            "question": "Commerce Media چه چیزی را به هم نزدیک می‌کند؟",
            "options": [
                "داده، رسانه و نتیجه تجاری",
                "فقط تبلیغات تلویزیونی",
                "فقط فروشگاه فیزیکی",
                "فقط حسابداری",
            ],
            "correct_answer": "داده، رسانه و نتیجه تجاری",
        },
    ],

    (
        "chapter_18",
        "lesson_18_04",
    ): [
        {
            "id": "mk18_q04",
            "question": "مهم‌ترین اصل در استفاده از فناوری در بازاریابی چیست؟",
            "options": [
                "فناوری باید در خدمت مسئله واقعی مشتری و کسب‌وکار باشد",
                "هرچه ابزار بیشتر باشد بهتر است",
                "AI همیشه جایگزین استراتژی است",
                "داده همیشه بدون محدودیت قابل استفاده است",
            ],
            "correct_answer": "فناوری باید در خدمت مسئله واقعی مشتری و کسب‌وکار باشد",
        },
    ],
}


# ==========================================================
# Public API
# ==========================================================

def get_chapters() -> list[dict[str, Any]]:
    """Return all Marketing chapters."""
    return [
        dict(chapter)
        for chapter in MARKETING_CURRICULUM
    ]


def get_chapter(
    chapter_id: str,
) -> dict[str, Any] | None:
    """Return one Marketing chapter."""
    if chapter_id is None:
        return None

    normalized_id = str(
        chapter_id
    ).strip()

    for chapter in MARKETING_CURRICULUM:
        if chapter.get("id") == normalized_id:
            return dict(chapter)

    return None


def get_chapter_by_id(
    chapter_id: str,
) -> dict[str, Any] | None:
    """Compatibility alias."""
    return get_chapter(chapter_id)


def get_lessons(
    chapter_id: str,
) -> list[dict[str, Any]]:
    """Return lessons for a chapter."""
    if chapter_id is None:
        return []

    normalized_id = str(
        chapter_id
    ).strip()

    return [
        dict(lesson)
        for lesson in MARKETING_LESSONS.get(
            normalized_id,
            [],
        )
    ]


def get_lesson(
    chapter_id: str,
    lesson_id: str,
) -> dict[str, Any] | None:
    """Return one lesson."""
    if (
        chapter_id is None
        or lesson_id is None
    ):
        return None

    normalized_chapter_id = str(
        chapter_id
    ).strip()

    normalized_lesson_id = str(
        lesson_id
    ).strip()

    for lesson in MARKETING_LESSONS.get(
        normalized_chapter_id,
        [],
    ):
        if lesson.get("id") == normalized_lesson_id:
            return dict(lesson)

    return None


def get_lesson_by_id(
    chapter_id: str,
    lesson_id: str,
) -> dict[str, Any] | None:
    """Compatibility alias."""
    return get_lesson(
        chapter_id,
        lesson_id,
    )


def get_quiz_questions(
    chapter_id: str,
    lesson_id: str,
) -> list[dict[str, Any]]:
    """Return quiz questions for a lesson."""
    if (
        chapter_id is None
        or lesson_id is None
    ):
        return []

    key = (
        str(chapter_id).strip(),
        str(lesson_id).strip(),
    )

    return [
        dict(question)
        for question in MARKETING_QUIZ_QUESTIONS.get(
            key,
            [],
        )
    ]


def get_quiz_questions_for_lesson(
    chapter_id: str,
    lesson_id: str,
) -> list[dict[str, Any]]:
    """Compatibility alias."""
    return get_quiz_questions(
        chapter_id,
        lesson_id,
    )


def get_module_info() -> dict[str, Any]:
    """Return complete module information."""
    return {
        "id": MODULE_ID,
        "module_id": MODULE_ID,
        "title": MODULE_TITLE,
        "description": MODULE_DESCRIPTION,
        "version": MODULE_VERSION,
        "level": MODULE_LEVEL,
        "chapters": len(MARKETING_CURRICULUM),
    }


def get_curriculum_statistics() -> dict[str, int]:
    """Return curriculum statistics."""
    chapters_count = len(
        MARKETING_CURRICULUM
    )

    lessons_count = 0
    quiz_count = 0

    for chapter in MARKETING_CURRICULUM:

        chapter_id = str(
            chapter.get(
                "id",
                "",
            )
        )

        lessons = MARKETING_LESSONS.get(
            chapter_id,
            [],
        )

        lessons_count += len(
            lessons
        )

        for lesson in lessons:

            lesson_id = str(
                lesson.get(
                    "id",
                    "",
                )
            )

            quiz_count += len(
                MARKETING_QUIZ_QUESTIONS.get(
                    (
                        chapter_id,
                        lesson_id,
                    ),
                    [],
                )
            )

    return {
        "modules": 1,
        "chapters": chapters_count,
        "lessons": lessons_count,
        "quiz_questions": quiz_count,
    }


def get_module_statistics() -> dict[str, Any]:
    """Return module statistics with metadata."""
    return {
        "module_id": MODULE_ID,
        "title": MODULE_TITLE,
        **get_curriculum_statistics(),
    }


def search_lessons(
    keyword: str,
) -> list[dict[str, Any]]:
    """Search lessons by title, content or keywords."""
    if keyword is None:
        return []

    normalized_keyword = str(
        keyword
    ).strip().casefold()

    if not normalized_keyword:
        return []

    results: list[dict[str, Any]] = []

    for chapter in MARKETING_CURRICULUM:

        chapter_id = str(
            chapter.get(
                "id",
                "",
            )
        )

        chapter_title = str(
            chapter.get(
                "title",
                "",
            )
        )

        for lesson in MARKETING_LESSONS.get(
            chapter_id,
            [],
        ):

            lesson_id = str(
                lesson.get(
                    "id",
                    "",
                )
            )

            title = str(
                lesson.get(
                    "title",
                    "",
                )
            )

            content = str(
                lesson.get(
                    "content",
                    "",
                )
            )

            keywords = " ".join(
                str(item)
                for item in lesson.get(
                    "keywords",
                    [],
                )
            )

            searchable_text = (
                f"{chapter_title}\n"
                f"{title}\n"
                f"{content}\n"
                f"{keywords}"
            ).casefold()

            if normalized_keyword in searchable_text:

                results.append(
                    {
                        "module_id": MODULE_ID,
                        "chapter_id": chapter_id,
                        "lesson_id": lesson_id,
                        "chapter_title": chapter_title,
                        "title": title,
                    }
                )

    return results


def validate_curriculum() -> dict[str, Any]:
    """Validate curriculum integrity."""

    errors: list[str] = []
    warnings: list[str] = []

    chapter_ids: set[str] = set()

    for chapter_index, chapter in enumerate(
        MARKETING_CURRICULUM,
        start=1,
    ):

        chapter_id = str(
            chapter.get(
                "id",
                "",
            )
        ).strip()

        if not chapter_id:

            errors.append(
                f"Chapter #{chapter_index} has no ID."
            )

            continue

        if chapter_id in chapter_ids:

            errors.append(
                f"Duplicate chapter ID: {chapter_id}"
            )

        chapter_ids.add(
            chapter_id
        )

        if not chapter.get("title"):

            warnings.append(
                f"Chapter '{chapter_id}' has no title."
            )

        lessons = MARKETING_LESSONS.get(
            chapter_id,
            [],
        )

        if not lessons:

            warnings.append(
                f"Chapter '{chapter_id}' has no lessons."
            )

        lesson_ids: set[str] = set()

        for lesson_index, lesson in enumerate(
            lessons,
            start=1,
        ):

            lesson_id = str(
                lesson.get(
                    "id",
                    "",
                )
            ).strip()

            if not lesson_id:

                errors.append(
                    f"Chapter '{chapter_id}' lesson "
                    f"#{lesson_index} has no ID."
                )

                continue

            if lesson_id in lesson_ids:

                errors.append(
                    f"Duplicate lesson ID '{lesson_id}' "
                    f"in chapter '{chapter_id}'."
                )

            lesson_ids.add(
                lesson_id
            )

            if not lesson.get("title"):

                warnings.append(
                    f"Lesson '{lesson_id}' has no title."
                )

            if not lesson.get("content"):

                warnings.append(
                    f"Lesson '{lesson_id}' has no content."
                )

            quiz_key = (
                chapter_id,
                lesson_id,
            )

            if not MARKETING_QUIZ_QUESTIONS.get(
                quiz_key,
                [],
            ):

                warnings.append(
                    f"Lesson '{lesson_id}' has no quiz."
                )

    statistics = get_curriculum_statistics()

    return {
        "valid": not errors,
        "errors": errors,
        "warnings": warnings,
        "statistics": statistics,
    }


def health_check() -> bool:
    """Return True when the module data is healthy."""
    try:

        result = validate_curriculum()

        return bool(
            result.get(
                "valid",
                False,
            )
        )

    except Exception:

        return False


# ==========================================================
# Compatibility Constants
# ==========================================================

MARKETING_CHAPTERS = MARKETING_CURRICULUM


# ==========================================================
# Public Exports
# ==========================================================

__all__ = [
    "MODULE_ID",
    "MODULE_TITLE",
    "MODULE_DESCRIPTION",
    "MODULE_VERSION",
    "MODULE_LEVEL",

    "MARKETING_CURRICULUM",
    "MARKETING_CHAPTERS",
    "MARKETING_LESSONS",
    "MARKETING_QUIZ_QUESTIONS",

    "get_chapters",
    "get_chapter",
    "get_chapter_by_id",

    "get_lessons",
    "get_lesson",
    "get_lesson_by_id",

    "get_quiz_questions",
    "get_quiz_questions_for_lesson",

    "get_module_info",
    "get_curriculum_statistics",
    "get_module_statistics",

    "search_lessons",
    "validate_curriculum",
    "health_check",
]


# ==========================================================
# Local Test
# ==========================================================

if __name__ == "__main__":

    print(
        "Marketing Module Health:",
        health_check(),
    )

    print(
        "Module:",
        get_module_info(),
    )

    print(
        "Statistics:",
        get_curriculum_statistics(),
    )
