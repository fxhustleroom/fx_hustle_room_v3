from app.languages import LANGUAGES


def _same(text: str) -> dict[str, str]:
    return {code: text for code in LANGUAGES}


TEXTS = {
    "select_language": {
        "en": "Please choose your language:",
        "es": "Selecciona tu idioma:",
        "fr": "Veuillez choisir votre langue :",
        "de": "Bitte wählen Sie Ihre Sprache:",
        "pt": "Escolha seu idioma:",
        "ar": "يرجى اختيار لغتك:",
        "hi": "कृपया अपनी भाषा चुनें:",
        "id": "Silakan pilih bahasa Anda:",
        "tr": "Lütfen dilinizi seçin:",
        "ru": "Пожалуйста, выберите язык:",
        "nl": "Kies uw taal:",  # ✅ ADD
    },
    "welcome": {
        "en": "Welcome to The FX Hustle Room Exclusive Trading Alerts.\n\n➡️ You now have access to our Exclusive Forex & Gold trade ideas, a structured onboarding path, and our private alert room.\n\nLet’s start with your onboarding.",
        "es": "Bienvenido a The FX Hustle Room Exclusive Trading Alerts.\n\n➡️ Ahora tienes acceso a nuestras ideas exclusivas de trading en Forex y Oro, un proceso de incorporación estructurado y nuestra sala privada de alertas.\n\nComencemos con tu onboarding.",
        "fr": "Bienvenue sur The FX Hustle Room Exclusive Trading Alerts.\n\n➡️ Vous avez maintenant accès à nos idées exclusives de trading Forex et Or, un parcours d’intégration structuré et notre salle privée d’alertes.\n\nCommençons votre onboarding.",
        "de": "Willkommen bei The FX Hustle Room Exclusive Trading Alerts.\n\n➡️ Du hast jetzt Zugang zu unseren exklusiven Forex- und Gold-Trading-Ideen, einem strukturierten Onboarding-Prozess und unserem privaten Signalraum.\n\nLass uns mit deinem Onboarding beginnen.",
        "pt": "Bem-vindo ao The FX Hustle Room Exclusive Trading Alerts.\n\n➡️ Agora você tem acesso às nossas ideias exclusivas de trading em Forex e Ouro, um processo de onboarding estruturado e nossa sala privada de alertas.\n\nVamos começar com seu onboarding.",
        "ar": "مرحبًا بك في The FX Hustle Room Exclusive Trading Alerts.\n\n➡️ لديك الآن وصول إلى أفكار تداول الفوركس والذهب الحصرية لدينا، ومسار إعداد منظم، وغرفة التنبيهات الخاصة بنا.\n\nلنبدأ عملية الإعداد.",
        "hi": "The FX Hustle Room Exclusive Trading Alerts में आपका स्वागत है।\n\n➡️ अब आपके पास हमारे एक्सक्लूसिव फॉरेक्स और गोल्ड ट्रेड आइडियाज़, एक संरचित ऑनबोर्डिंग प्रक्रिया और हमारे प्राइवेट अलर्ट रूम तक पहुंच है।\n\nआइए आपका ऑनबोर्डिंग शुरू करें।",
        "id": "Selamat datang di The FX Hustle Room Exclusive Trading Alerts.\n\n➡️ Sekarang Anda memiliki akses ke ide trading Forex & Emas eksklusif kami, alur onboarding terstruktur, dan ruang alert privat kami.\n\nMari mulai onboarding Anda.",
        "tr": "The FX Hustle Room Exclusive Trading Alerts'e hoş geldiniz.\n\n➡️ Artık özel Forex ve Altın işlem fikirlerimize, yapılandırılmış bir onboarding sürecine ve özel sinyal odamıza erişiminiz var.\n\nOnboarding sürecinize başlayalım.",
        "ru": "Добро пожаловать в The FX Hustle Room Exclusive Trading Alerts.\n\n➡️ Теперь у вас есть доступ к нашим эксклюзивным торговым идеям по Forex и золоту, структурированному онбордингу и нашей приватной комнате сигналов.\n\nДавайте начнем ваше онбординг.",
        "nl": "Welkom bij The FX Hustle Room Exclusive Trading Alerts.\n\n➡️ Je hebt nu toegang tot onze exclusieve Forex- en goud handelsideeën, een gestructureerd onboardingproces en onze privé alertgroep.\n\nLaten we beginnen met je onboarding.",  # ✅ ADD
    },
    "terms": {
        "en": "Please read and accept our Rules & Terms to continue.\n⚠️ Trading involves risk. You are responsible for your own decisions.",
        "es": "Lee y acepta nuestras Reglas y Términos para continuar.\n⚠️ El trading implica riesgo. Eres responsable de tus propias decisiones.",
        "fr": "Veuillez lire et accepter nos Règles et Conditions pour continuer.\n⚠️ Le trading comporte des risques. Vous êtes responsable de vos propres décisions.",
        "de": "Bitte lies und akzeptiere unsere Regeln und Bedingungen, um fortzufahren.\n⚠️ Trading ist mit Risiken verbunden. Du bist für deine eigenen Entscheidungen verantwortlich.",
        "pt": "Leia e aceite nossos Termos e Regras para continuar.\n⚠️ O trading envolve risco. Você é responsável por suas próprias decisões.",
        "ar": "يرجى قراءة القواعد والشروط والموافقة عليها للمتابعة.\n⚠️ التداول ينطوي على مخاطر. أنت مسؤول عن قراراتك الخاصة.",
        "hi": "जारी रखने के लिए कृपया हमारे नियम और शर्तें पढ़ें और स्वीकार करें।\n⚠️ ट्रेडिंग में जोखिम शामिल है। अपने निर्णयों के लिए आप स्वयं जिम्मेदार हैं।",
        "id": "Silakan baca dan setujui Aturan & Ketentuan kami untuk melanjutkan.\n⚠️ Trading memiliki risiko. Anda bertanggung jawab atas keputusan Anda sendiri.",
        "tr": "Devam etmek için lütfen Kurallarımızı ve Şartlarımızı okuyup kabul edin.\n⚠️ İşlem yapmak risk içerir. Kendi kararlarınızdan siz sorumlusunuz.",
        "ru": "Пожалуйста, прочитайте и примите наши Правила и Условия, чтобы продолжить.\n⚠️ Торговля связана с риском. Вы несете ответственность за свои решения.",
        "nl": "Lees en accepteer onze Regels en Voorwaarden om door te gaan.\n⚠️ Trading bevat risico's. U bent verantwoordelijk voor uw eigen beslissingen.",  # ✅ ADD
    },
    "create_account": _same(
    "Step 1️⃣ — Create a live trading account:\n\n"
    "Register with this link:\n"
    "👉 https://go.vtaffiliates.com/visit/?bta=42404&brand=vt\n\n"
    "Recommended platform: MetaTrader 5 (mobile app is fine)\n"
    "Account Type: RAW-ECN\n"
    "Account Currency: EUR"),
    "verify_identity": _same(
    "Step 2️⃣ — Verify your identity:\n\n"
    "Complete the identity verification inside VT Markets (one-time only) to fully activate your account."
    ),
    "fund_account": _same(
    "Step 3️⃣ — Fund your account:\n\n"
    "To trade XAUUSD using our execution model and required lot sizes, a minimum deposit of €350 is required.\n\n"
    "✅ After your deposit is confirmed, your balance will be doubled, providing you with additional capital to trade."
),
    "upload_deposit_prompt": _same("Please upload a screenshot or PDF of your deposit proof."),
    "deposit_pending": _same("Your deposit proof is pending admin approval."),
    "deposit_approved": _same(
    "Your deposit has been approved.\n\n"
    "Risk management is a critical aspect of trading. Before entering any trades, make sure you have reviewed the risk management module in your online training environment.\n\n"
    "Do you understand the importance of risk management?"
),
    "deposit_rejected": _same("Your deposit proof was rejected. Please upload it again."),
    "risk": _same("Risk management is a critical aspect of trading.\n\nBefore entering any trades, make sure you have reviewed the risk management module in your online training environment.\n\nDo you understand the importance of risk management?"),
    "risk_no": _same("Risk management is the foundation of successful trading. make sure you understand this before placing your first trade. Next button below."),
    "signal_instruction": _same("Place this trade, then upload a screenshot proof of your executed trade."),
    "trade_upload_prompt": _same("Please upload a screenshot of your first executed trade."),
    "trade_rejected": _same("Your trade proof was rejected. Please upload the screenshot again."),
    "premium_granted": _same(
    "Access to our Exclusive Trading Alerts is granted.\n\n"
    "Click below to join now."
),
    "unsupported_file": _same("Unsupported file. Please upload an image or PDF."),
    "status_waiting_deposit": _same("Your deposit is still pending approval."),
    "admin_deposit_caption": _same("New deposit proof submitted."),
    "admin_trade_caption": _same("New first trade proof submitted."),
    "trading_video_missing": _same("Trading video is not configured yet. The admin needs to upload it first."),
    "admin_only": _same("This action is only available to admins."),
    "saved": _same("Saved successfully."),
}


def t(key: str, language: str) -> str:
    bundle = TEXTS.get(key, {})
    return bundle.get(language) or bundle.get("en") or key
