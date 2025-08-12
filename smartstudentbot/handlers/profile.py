from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from ..utils.gates import RegistrationMiddleware

router = Router(name="profile")

# All handlers in this router require the user to be registered.
# We can set the middleware for the entire router.
router.message.middleware(RegistrationMiddleware())
router.callback_query.middleware(RegistrationMiddleware())


@router.message(Command("profile"), flags={"require_registration": True})
async def handle_profile_command(message: Message):
    """Handles the /profile command."""
    # In a full implementation, this would fetch user data from GSheets/Redis
    # and display it nicely.
    await message.answer(
        "👤 This is your profile page.\n\n"
        "Features like editing your profile or viewing your data will be available here soon."
    )

@router.callback_query(F.data == "profile_menu", flags={"require_registration": True})
async def handle_profile_callback(callback: CallbackQuery):
    """Handles the callback button for the profile menu."""
    await callback.message.edit_text(
        "👤 This is your profile page.\n\n"
        "Features like editing your profile or viewing your data will be available here soon."
    )
    await callback.answer()
