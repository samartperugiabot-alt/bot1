import datetime
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from ..utils.i18n import get_text
from ..utils.common import is_valid_email, is_valid_age
from ..utils.gsheets import gsheets_manager
from ..utils.redis_utils import redis_manager
from ..config import DEFAULT_LANG, DEFAULT_CITY, USERS_SHEET_NAME
from ..utils.gates import REGISTRATION_CACHE # For updating cache after registration

router = Router(name="register")

# Define FSM states for the registration process
class RegistrationStates(StatesGroup):
    getting_name = State()
    getting_age = State()
    getting_city = State()
    getting_major = State()
    getting_email = State()

@router.callback_query(F.data == "start_registration")
async def start_registration(callback: CallbackQuery, state: FSMContext):
    """Starts the registration process."""
    user_id = callback.from_user.id
    lang = await redis_manager.get_user_lang(user_id) or DEFAULT_LANG

    await state.set_state(RegistrationStates.getting_name)
    await callback.message.answer(get_text("start_registration", lang))
    await callback.answer()

@router.message(RegistrationStates.getting_name)
async def get_name(message: Message, state: FSMContext):
    """Receives the user's name and asks for their age."""
    user_id = message.from_user.id
    lang = await redis_manager.get_user_lang(user_id) or DEFAULT_LANG

    await state.update_data(name=message.text.strip())
    await state.set_state(RegistrationStates.getting_age)
    await message.answer(get_text("ask_for_age", lang))

@router.message(RegistrationStates.getting_age)
async def get_age(message: Message, state: FSMContext):
    """Receives age, validates it, and asks for the city."""
    user_id = message.from_user.id
    lang = await redis_manager.get_user_lang(user_id) or DEFAULT_LANG

    if not is_valid_age(message.text.strip()):
        await message.answer(get_text("invalid_age", lang))
        return

    await state.update_data(age=int(message.text.strip()))
    await state.set_state(RegistrationStates.getting_city)
    await message.answer(get_text("ask_for_city", lang))

@router.message(RegistrationStates.getting_city)
async def get_city(message: Message, state: FSMContext):
    """Receives city and asks for the major."""
    user_id = message.from_user.id
    lang = await redis_manager.get_user_lang(user_id) or DEFAULT_LANG

    await state.update_data(city=message.text.strip().capitalize())
    await state.set_state(RegistrationStates.getting_major)
    await message.answer(get_text("ask_for_major", lang))

@router.message(RegistrationStates.getting_major)
async def get_major(message: Message, state: FSMContext):
    """Receives major and asks for the email."""
    user_id = message.from_user.id
    lang = await redis_manager.get_user_lang(user_id) or DEFAULT_LANG

    await state.update_data(major=message.text.strip())
    await state.set_state(RegistrationStates.getting_email)
    await message.answer(get_text("ask_for_email", lang))

@router.message(RegistrationStates.getting_email)
async def get_email_and_complete(message: Message, state: FSMContext):
    """Receives email, validates, completes registration, and saves data."""
    user_id = message.from_user.id
    lang = await redis_manager.get_user_lang(user_id) or DEFAULT_LANG
    email = message.text.strip()

    if not is_valid_email(email):
        await message.answer(get_text("invalid_email", lang))
        return

    await state.update_data(email=email)

    # --- Finalize Registration ---
    user_data = await state.get_data()
    await state.clear()

    # Prepare data for Google Sheets
    profile_data = {
        "telegram_id": user_id,
        "telegram_username": message.from_user.username or "",
        "first_name": user_data.get("name"),
        "age": user_data.get("age"),
        "city": user_data.get("city", DEFAULT_CITY),
        "major": user_data.get("major"),
        "email": user_data.get("email"),
        "lang": lang,
        "registration_date": datetime.datetime.utcnow().isoformat(),
        "is_active": True,
    }

    # Save to Google Sheets
    await gsheets_manager.save_user_profile(profile_data)

    # Update registration cache
    REGISTRATION_CACHE[user_id] = True
    if redis_manager.redis:
        await redis_manager.redis.setex(f"user:{user_id}:registered", 3600, "1")

    # Confirm completion and show main menu
    await message.answer(get_text("registration_complete", lang))

    # Show the main menu
    from .cmd_start import get_main_menu_keyboard
    keyboard = get_main_menu_keyboard(lang)
    await message.answer(get_text("welcome_registered", lang).format(first_name=profile_data["first_name"]), reply_markup=keyboard)
