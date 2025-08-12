from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

from ..utils.i18n import get_text
from ..utils.redis_utils import redis_manager
from ..utils.gsheets import gsheets_manager
from ..config import SUPPORTED_LANGUAGES, USERS_SHEET_NAME, DEFAULT_LANG

router = Router(name="language")

def get_language_keyboard():
    """Builds the language selection keyboard."""
    builder = InlineKeyboardBuilder()
    # Emojis for languages
    lang_map = {"fa": "🇮🇷 فارسی", "en": "🇬🇧 English", "it": "🇮🇹 Italiano"}
    for lang_code in SUPPORTED_LANGUAGES:
        builder.button(text=lang_map.get(lang_code, lang_code), callback_data=f"set_lang_{lang_code}")
    builder.adjust(1)
    return builder.as_markup()

@router.message(Command("language"))
async def handle_language_command(message: Message):
    """Shows the language selection menu."""
    user_id = message.from_user.id
    lang = await redis_manager.get_user_lang(user_id) or DEFAULT_LANG

    text = get_text("select_language", lang)
    keyboard = get_language_keyboard()
    await message.answer(text, reply_markup=keyboard)

@router.callback_query(F.data == "language_menu")
async def handle_language_callback(callback: CallbackQuery):
    """Handles the callback to open the language menu."""
    user_id = callback.from_user.id
    lang = await redis_manager.get_user_lang(user_id) or DEFAULT_LANG

    text = get_text("select_language", lang)
    keyboard = get_language_keyboard()
    await callback.message.edit_text(text, reply_markup=keyboard)
    await callback.answer()

@router.callback_query(F.data.startswith("set_lang_"))
async def handle_set_language(callback: CallbackQuery):
    """Sets the user's language and confirms the change."""
    new_lang = callback.data.split("_")[-1]
    user_id = callback.from_user.id

    if new_lang not in SUPPORTED_LANGUAGES:
        await callback.answer("Invalid language selected.", show_alert=True)
        return

    # 1. Update Redis cache immediately for responsiveness
    await redis_manager.set_user_lang(user_id, new_lang)

    # 2. Update Google Sheets in the background
    # We need to find the user and update their 'lang' column.
    # This is a simplified example. A real implementation might queue this job.
    user_profile = await gsheets_manager.get_user_by_id(user_id)
    if user_profile:
        user_profile['lang'] = new_lang
        # This assumes a 'save' method that can update based on a dict.
        # Our current gsheets_manager saves the whole row.
        await gsheets_manager.save_user_profile(user_profile)

    confirmation_text = get_text("lang_changed", new_lang)

    # After changing the language, show the main menu again (if registered)
    # We re-import here to avoid circular dependency issues
    from .cmd_start import get_main_menu_keyboard
    from ..utils.gates import is_user_registered

    if await is_user_registered(user_id):
        keyboard = get_main_menu_keyboard(new_lang)
        await callback.message.edit_text(confirmation_text, reply_markup=keyboard)
    else:
        # If not registered, just confirm and they can proceed with registration in the new language
        await callback.message.edit_text(confirmation_text)

    await callback.answer()
