from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import Message, CallbackQuery

from .gsheets import gsheets_manager
from .redis_utils import redis_manager
from .i18n import get_text
from ..config import DEFAULT_LANG

# A simple in-memory cache for registration status to avoid hitting GSheets on every message.
# In a multi-worker setup, Redis would be better.
# Key: user_id (int), Value: is_registered (bool)
REGISTRATION_CACHE = {}

async def is_user_registered(user_id: int) -> bool:
    """
    Checks if a user is registered.
    Uses a local cache first, then Redis, then falls back to Google Sheets.
    """
    # 1. Check local cache
    if user_id in REGISTRATION_CACHE:
        return REGISTRATION_CACHE[user_id]

    # 2. Check Redis cache
    # Using a simple key like `user:{user_id}:registered`
    if redis_manager.redis:
        is_registered = await redis_manager.redis.get(f"user:{user_id}:registered")
        if is_registered is not None:
            status = is_registered == "1"
            REGISTRATION_CACHE[user_id] = status # Update local cache
            return status

    # 3. Fallback to Google Sheets (the source of truth)
    user_profile = await gsheets_manager.get_user_by_id(user_id)
    is_registered = user_profile is not None

    # 4. Update caches
    REGISTRATION_CACHE[user_id] = is_registered
    if redis_manager.redis:
        # Cache for 1 hour in Redis
        await redis_manager.redis.setex(f"user:{user_id}:registered", 3600, "1" if is_registered else "0")

    return is_registered


class RegistrationMiddleware(BaseMiddleware):
    """
    Middleware to check if a user is registered before processing an update.
    This is attached to specific handlers that require registration.
    """
    async def __call__(
        self,
        handler: Callable[[Message, Dict[str, Any]], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: Dict[str, Any]
    ) -> Any:

        user = data.get("event_from_user")
        if not user:
            return await handler(event, data)

        # The 'require_registration' flag must be passed to the handler decorator
        # e.g., @router.message(Command("profile"), flags={"require_registration": True})
        if not data.get("require_registration"):
            return await handler(event, data)

        if await is_user_registered(user.id):
            return await handler(event, data)

        # User is not registered, send a message and stop processing
        lang = await redis_manager.get_user_lang(user.id) or DEFAULT_LANG
        text = get_text("must_register", lang)

        if isinstance(event, Message):
            await event.answer(text)
        elif isinstance(event, CallbackQuery):
            await event.answer(text, show_alert=True)

        return # Stop propagation
