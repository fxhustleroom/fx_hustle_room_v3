from app.languages import LANGUAGES
from googletrans import Translator

translator = Translator()

# Cache translations (prevents repeated API calls)
_translation_cache = {}


def auto_translate(text: str, target_lang: str) -> str:
    if target_lang == "en":
        return text

    cache_key = f"{target_lang}:{text}"

    if cache_key in _translation_cache:
        return _translation_cache[cache_key]

    try:
        translated = translator.translate(text, dest=target_lang).text
        _translation_cache[cache_key] = translated
        return translated
    except Exception:
        return text


TEXTS = {
    "select_language": "Please choose your language:",

    "welcome": (
        "Welcome to The FX Hustle Room Exclusive Trading Alerts.\n\n"
        "➡️ You now have access to our Exclusive Forex & Gold trade ideas, a structured onboarding path, and our private alert room.\n\n"
        "Let’s start with your onboarding."
    ),

    "terms": (
        "Please read and accept our Rules & Terms to continue.\n"
        "⚠️ Trading involves risk. You are responsible for your own decisions."
    ),

    "create_account": (
        "Step 1️⃣ — Create a live trading account:\n\n"
        "Register with this link:\n"
        "👉 https://go.vtaffiliates.com/visit/?bta=42404&brand=vt\n\n"
        "Recommended platform: MetaTrader 5 (mobile app is fine)\n"
        "Account Type: RAW-ECN\n"
        "Account Currency: EUR"
    ),

    "verify_identity": (
        "Step 2️⃣ — Verify your identity:\n\n"
        "Complete the identity verification inside VT Markets (one-time only) to fully activate your account."
    ),

    "fund_account": (
        "Step 3️⃣ — Fund your account:\n\n"
        "To trade XAUUSD using our execution model and required lot sizes, a minimum deposit of €350 is required.\n\n"
        "✅ After your deposit is confirmed, your balance will be doubled, providing you with additional capital to trade."
    ),

    "upload_deposit_prompt": "Please upload a screenshot or PDF of your deposit proof.",
    "deposit_pending": "Your deposit proof is pending admin approval.",

    "deposit_approved": (
        "Your deposit has been approved.\n\n"
        "Risk management is a critical aspect of trading. Before entering any trades, make sure you have reviewed the risk management module in your online training environment.\n\n"
        "Do you understand the importance of risk management?"
    ),

    "deposit_rejected": "Your deposit proof was rejected. Please upload it again.",

    "risk": (
        "Risk management is a critical aspect of trading.\n\n"
        "Before entering any trades, make sure you have reviewed the risk management module in your online training environment.\n\n"
        "Do you understand the importance of risk management?"
    ),

    "risk_no": (
        "Risk management is the foundation of successful trading. "
        "Make sure you understand this before placing your first trade."
    ),

    "signal_instruction": "Place this trade, then upload a screenshot proof of your executed trade.",
    "trade_upload_prompt": "Please upload a screenshot of your first executed trade.",
    "trade_rejected": "Your trade proof was rejected. Please upload the screenshot again.",

    "premium_granted": (
        "Access to our Exclusive Trading Alerts is granted.\n\n"
        "Click below to join now."
    ),

    "unsupported_file": "Unsupported file. Please upload an image or PDF.",
    "status_waiting_deposit": "Your deposit is still pending approval.",
    "admin_deposit_caption": "New deposit proof submitted.",
    "admin_trade_caption": "New first trade proof submitted.",
    "trading_video_missing": "Trading video is not configured yet. The admin needs to upload it first.",
    "admin_only": "This action is only available to admins.",
    "saved": "Saved successfully.",
}


def t(key: str, language: str) -> str:
    text = TEXTS.get(key, key)
    return auto_translate(text, language)