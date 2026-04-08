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
    },
    "welcome": {
        "en": "Welcome to The FX Hustle Room Exclusive Trading Alerts.\n\nGet premium forex and gold trade ideas, structured onboarding, and access to our private signals room.",
        "es": "Bienvenido a The FX Hustle Room Exclusive Trading Alerts.\n\nObtén ideas premium de trading en forex y oro, onboarding estructurado y acceso a nuestra sala privada de señales.",
        "fr": "Bienvenue sur The FX Hustle Room Exclusive Trading Alerts.\n\nRecevez des idées premium de trading forex et or, un parcours d'intégration structuré et l'accès à notre salle privée de signaux.",
        "de": "Willkommen bei The FX Hustle Room Exclusive Trading Alerts.\n\nErhalte Premium-Ideen für Forex- und Gold-Trades, ein strukturiertes Onboarding und Zugang zu unserem privaten Signalraum.",
        "pt": "Bem-vindo ao The FX Hustle Room Exclusive Trading Alerts.\n\nReceba ideias premium de trade em forex e ouro, onboarding estruturado e acesso à nossa sala privada de sinais.",
        "ar": "مرحبًا بك في The FX Hustle Room Exclusive Trading Alerts.\n\nاحصل على أفكار تداول مميزة للفوركس والذهب، ومسار انضمام منظم، ووصول إلى غرفة الإشارات الخاصة بنا.",
        "hi": "The FX Hustle Room Exclusive Trading Alerts में आपका स्वागत है।\n\nप्रीमियम फॉरेक्स और गोल्ड ट्रेड आइडियाज़, व्यवस्थित ऑनबोर्डिंग और हमारे प्राइवेट सिग्नल रूम तक पहुँच प्राप्त करें।",
        "id": "Selamat datang di The FX Hustle Room Exclusive Trading Alerts.\n\nDapatkan ide trading forex dan emas premium, onboarding terstruktur, dan akses ke ruang sinyal privat kami.",
        "tr": "The FX Hustle Room Exclusive Trading Alerts'e hoş geldiniz.\n\nPremium forex ve altın işlem fikirleri, yapılandırılmış onboarding ve özel sinyal odamıza erişim elde edin.",
        "ru": "Добро пожаловать в The FX Hustle Room Exclusive Trading Alerts.\n\nПолучайте премиальные идеи по торговле на форекс и золоте, структурированный онбординг и доступ в нашу приватную комнату сигналов.",
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
    },
    "create_account": _same("Create a trading account\n\nRegister with this link:\n👉 https://go.vtaffiliates.com/visit/?bta=42404&brand=vt\n\nRecommended platform: MetaTrader 5 (mobile app is fine)\nAccount Type: RAW-ECN\nAccount Currency: EUR"),
    "verify_identity": _same("Verify your identity\n\nComplete the identity verification (one-time only) to fully activate your account."),
    "fund_account": _same("Step 3️⃣ — Fund your account\n\nTo trade XAUUSD using our execution model and required lot sizes, a minimum deposit of €350 is required.\n\n✅ Once deposited, your balance may be doubled (as per your broker offer), giving more flexibility."),
    "upload_deposit_prompt": _same("Please upload a screenshot or PDF of your deposit proof."),
    "deposit_pending": _same("Your deposit proof is pending admin approval."),
    "deposit_approved": _same("Your deposit has been approved Risk management is a critical aspect of trading. Before entering any trades, make sure you have reviewed the risk management module in your online training environment. Do you understand the importance of risk management? ."),
    "deposit_rejected": _same("Your deposit proof was rejected. Please upload it again."),
    "risk": _same("Risk management is a critical aspect of trading.\n\nBefore entering any trades, make sure you have reviewed the risk management module in your online training environment.\n\nDo you understand the importance of risk management?"),
    "risk_no": _same("Risk management is the foundation of successful trading. make sure you understand this before placing your first trade. Next button below."),
    "signal_instruction": _same("Place this trade, then upload a screenshot proof of your executed trade."),
    "trade_upload_prompt": _same("Please upload a screenshot of your first executed trade."),
    "trade_rejected": _same("Your trade proof was rejected. Please upload the screenshot again."),
    "premium_granted": _same("Premium access granted.\n\nClick below to join the premium signals group."),
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
