from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.utils.markdown import hbold

from ..utils.i18n import get_text
from ..utils.gates import is_user_registered
from ..utils.redis_utils import redis_manager
from ..config import DEFAULT_LANG

router = Router(name="cmd_start")

def get_main_menu_keyboard(lang: str):
    """Builds the main menu inline keyboard."""
    builder = InlineKeyboardBuilder()
    buttons = {
        "resources_hub": "hub_menu", "scholarships": "scholarships_menu", "isee_calculator": "isee_form",
        "weather": "weather_menu", "news": "news_menu", "fx_rates": "fx_menu",
        "profile": "profile_menu", "roommate_finder": "roommate_menu", "admin_chat": "live_chat",
        "language_training": "lang_training_menu", "consult_appointment": "consult_form", "success_stories": "stories_menu",
        "search": "search_menu", "ask_question": "qna_menu", "points": "points_menu",
        "upload_document": "upload_form", "living_cost": "cost_menu", "discounts": "discounts_menu",
        "life_simulator": "simulation_menu", "migration_status": "migration_menu", "change_language": "language_menu",
        "podcast": "podcast_menu", "tips": "tips_menu", "events": "events_menu",
    }
    for text_key, callback_data in buttons.items():
        builder.button(text=get_text(text_key, lang), callback_data=callback_data)

    # Adjust layout to be 3 buttons per row
    builder.adjust(3)
    return builder.as_markup()

@router.message(CommandStart())
async def handle_start(message: Message):
    """
    Handler for the /start command.
    Greets the user and shows the main menu or a registration prompt.
    """
    user = message.from_user
    lang = await redis_manager.get_user_lang(user.id) or user.language_code or DEFAULT_LANG

    if await is_user_registered(user.id):
        # User is registered, show the full menu
        welcome_text = get_text("welcome_registered", lang).format(first_name=hbold(user.first_name))
        keyboard = get_main_menu_keyboard(lang)
    else:
        # New user, prompt to register
        welcome_text = get_text("welcome", lang)
        builder = InlineKeyboardBuilder()
        builder.button(text=get_text("register_button", lang), callback_data="start_registration")
        builder.button(text=get_text("change_language", lang), callback_data="language_menu")
        builder.adjust(1)
        keyboard = builder.as_markup()

    await message.answer(welcome_text, reply_markup=keyboard)

@router.callback_query(F.data == "main_menu")
async def show_main_menu_callback(callback: CallbackQuery):
    """
    Handler for the 'main_menu' callback button.
    Shows the main menu again, useful for a "Back to Main Menu" button.
    """
    user = callback.from_user
    lang = await redis_manager.get_user_lang(user.id) or user.language_code or DEFAULT_LANG

    # Assume if they can click this, they are registered
    welcome_text = get_text("welcome_registered", lang).format(first_name=hbold(user.first_name))
    keyboard = get_main_menu_keyboard(lang)

    await callback.message.edit_text(welcome_text, reply_markup=keyboard)
    await callback.answer()
