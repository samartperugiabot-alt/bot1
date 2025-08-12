from typing import Dict
from ..config import DEFAULT_LANG

# Internationalization Messages
# Using nested dictionaries for easy access: MSG[lang][key]
MSG: Dict[str, Dict[str, str]] = {
    "fa": {
        "welcome": "سلام! به ربات دانشجوی هوشمند خوش آمدید 🇮🇹\n\nلطفاً برای دسترسی به امکانات، ثبت‌نام کنید.",
        "welcome_registered": "سلام دوباره، {first_name}!\n\nچه کاری می‌تونم برات انجام بدم؟",
        "register_button": "📝 ثبت‌نام",
        "main_menu_button": "🏠 منوی اصلی",
        "back_button": "🔙 بازگشت",
        "select_language": "لطفاً زبان خود را انتخاب کنید:",
        "lang_changed": "زبان شما به فارسی تغییر کرد.",
        # Main Menu Buttons
        "resources_hub": "🇮🇹 مرکز منابع",
        "scholarships": "🎓 بورسیه‌ها",
        "isee_calculator": "🧮 محاسبه ISEE",
        "weather": "🌤️ آب‌وهوا",
        "news": "📰 اخبار",
        "fx_rates": "💱 تبدیل ارز",
        "profile": "👤 پروفایل",
        "roommate_finder": "🏠 هم‌اتاقی",
        "admin_chat": "🗣️ چت با ادمین",
        "language_training": "🧠 آموزش زبان",
        "consult_appointment": "🗓️ وقت مشاوره",
        "success_stories": "📖 داستان‌های موفقیت",
        "search": "🔎 جستجو",
        "ask_question": "💬 پرسش و پاسخ",
        "points": "⭐ امتیازها",
        "upload_document": "📤 آپلود مدارک",
        "living_cost": "💰 هزینه‌ها",
        "discounts": "💸 تخفیف‌ها",
        "life_simulator": "🧪 شبیه‌ساز زندگی",
        "migration_status": "🚦 وضعیت مهاجرت",
        "change_language": "🌐 تغییر زبان",
        "podcast": "🎙️ پادکست",
        "tips": "💡 نکات",
        "events": "📅 رویدادها",
        # Registration
        "start_registration": "فرآیند ثبت‌نام شروع شد.\n\nلطفاً نام خود را وارد کنید:",
        "ask_for_age": "عالیه! حالا سنت رو وارد کن (بین ۱۶ تا ۱۰۰):",
        "ask_for_city": "کدوم شهر ایتالیا هستی یا قصد داری بیای؟ (مثال: Perugia)",
        "ask_for_major": "چه رشته‌ای می‌خونی یا قصد داری بخونی؟",
        "ask_for_email": "لطفاً ایمیلت رو وارد کن:",
        "registration_complete": "✅ ثبت‌نام شما با موفقیت تکمیل شد!\nحالا می‌تونید از تمام امکانات ربات استفاده کنید.",
        "invalid_email": "ایمیل معتبر نیست. لطفاً دوباره تلاش کنید.",
        "invalid_age": "سن باید یک عدد بین ۱۶ تا ۱۰۰ باشه.",
        # Errors
        "generic_error": "خطایی رخ داد. لطفاً دوباره تلاش کنید یا با ادمین تماس بگیرید.",
        "must_register": "⛔️ برای دسترسی به این بخش باید ثبت‌نام کنید. لطفاً روی /start کلیک کرده و دکمه «📝 ثبت‌نام» را بزنید.",
    },
    "en": {
        "welcome": "Hello! Welcome to the Smart Student Bot 🇮🇹\n\nPlease register to access the features.",
        "welcome_registered": "Welcome back, {first_name}!\n\nHow can I help you today?",
        "register_button": "📝 Register",
        "main_menu_button": "🏠 Main Menu",
        "back_button": "🔙 Back",
        "select_language": "Please select your language:",
        "lang_changed": "Your language has been changed to English.",
        # Main Menu Buttons
        "resources_hub": "🇮🇹 Resources Hub",
        "scholarships": "🎓 Scholarships",
        "isee_calculator": "🧮 ISEE Calculator",
        "weather": "🌤️ Weather",
        "news": "📰 News",
        "fx_rates": "💱 FX Rates",
        "profile": "👤 Profile",
        "roommate_finder": "🏠 Roommate Finder",
        "admin_chat": "🗣️ Admin Chat",
        "language_training": "🧠 Language Training",
        "consult_appointment": "🗓️ Book Consultation",
        "success_stories": "📖 Success Stories",
        "search": "🔎 Search",
        "ask_question": "💬 Q&A",
        "points": "⭐ Points",
        "upload_document": "📤 Upload Documents",
        "living_cost": "💰 Living Costs",
        "discounts": "💸 Discounts",
        "life_simulator": "🧪 Life Simulator",
        "migration_status": "🚦 Migration Status",
        "change_language": "🌐 Change Language",
        "podcast": "🎙️ Podcast",
        "tips": "💡 Tips",
        "events": "📅 Events",
        # Registration
        "start_registration": "Registration process started.\n\nPlease enter your name:",
        "ask_for_age": "Great! Now, enter your age (between 16 and 100):",
        "ask_for_city": "Which city in Italy are you in or planning to come to? (e.g., Perugia)",
        "ask_for_major": "What is your field of study?",
        "ask_for_email": "Please enter your email:",
        "registration_complete": "✅ Your registration is complete!\nYou can now use all the bot's features.",
        "invalid_email": "Invalid email. Please try again.",
        "invalid_age": "Age must be a number between 16 and 100.",
        # Errors
        "generic_error": "An error occurred. Please try again or contact an admin.",
        "must_register": "⛔️ You must be registered to access this section. Please click /start and press the '📝 Register' button.",
    },
    "it": {
        "welcome": "Ciao! Benvenuto nello Smart Student Bot 🇮🇹\n\nPer favore, registrati per accedere alle funzionalità.",
        "welcome_registered": "Bentornato, {first_name}!\n\nCome posso aiutarti oggi?",
        "register_button": "📝 Registrati",
        "main_menu_button": "🏠 Menu Principale",
        "back_button": "🔙 Indietro",
        "select_language": "Seleziona la tua lingua:",
        "lang_changed": "La tua lingua è stata cambiata in Italiano.",
        # Main Menu Buttons
        "resources_hub": "🇮🇹 Centro Risorse",
        "scholarships": "🎓 Borse di Studio",
        "isee_calculator": "🧮 Calcolo ISEE",
        "weather": "🌤️ Meteo",
        "news": "📰 Notizie",
        "fx_rates": "💱 Tassi di Cambio",
        "profile": "👤 Profilo",
        "roommate_finder": "🏠 Trova Coinquilino",
        "admin_chat": "🗣️ Chat con Admin",
        "language_training": "🧠 Formazione Linguistica",
        "consult_appointment": "🗓️ Prenota Consulenza",
        "success_stories": "📖 Storie di Successo",
        "search": "🔎 Cerca",
        "ask_question": "💬 Domande e Risposte",
        "points": "⭐ Punti",
        "upload_document": "📤 Carica Documenti",
        "living_cost": "💰 Costo della Vita",
        "discounts": "💸 Sconti",
        "life_simulator": "🧪 Simulatore di Vita",
        "migration_status": "🚦 Stato Migrazione",
        "change_language": "🌐 Cambia Lingua",
        "podcast": "🎙️ Podcast",
        "tips": "💡 Consigli",
        "events": "📅 Eventi",
        # Registration
        "start_registration": "Processo di registrazione avviato.\n\nPer favore, inserisci il tuo nome:",
        "ask_for_age": "Ottimo! Ora, inserisci la tua età (tra 16 e 100):",
        "ask_for_city": "In quale città d'Italia ti trovi o hai intenzione di venire? (es. Perugia)",
        "ask_for_major": "Qual è il tuo campo di studi?",
        "ask_for_email": "Per favore, inserisci la tua email:",
        "registration_complete": "✅ La tua registrazione è completa!\nOra puoi usare tutte le funzionalità del bot.",
        "invalid_email": "Email non valida. Riprova.",
        "invalid_age": "L'età deve essere un numero tra 16 e 100.",
        # Errors
        "generic_error": "Si è verificato un errore. Riprova o contatta un amministratore.",
        "must_register": "⛔️ Devi essere registrato per accedere a questa sezione. Per favore, clicca /start e premi il pulsante '📝 Registrati'.",
    }
}

# This function will be a dependency for many handlers.
# In a real app, `user_lang` would be fetched from a database or Redis cache.
# For now, we'll create a helper that safely gets text.
def get_text(key: str, lang: str) -> str:
    """
    Retrieves a string from the MSG dictionary for a given language.
    Falls back to the default language if the key is not found in the target language.
    Falls back to the key itself if not found anywhere.
    """
    return MSG.get(lang, MSG[DEFAULT_LANG]).get(key, key)
