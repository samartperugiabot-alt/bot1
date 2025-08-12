import aiohttp
from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from ..config import GITHUB_DATA_URL, DEFAULT_CITY
from ..utils.i18n import get_text
from ..utils.redis_utils import redis_manager
from ..utils.logger import logger
from ..utils.gates import RegistrationMiddleware

router = Router(name="resources_hub")
# This handler requires registration
router.callback_query.middleware(RegistrationMiddleware())
router.message.middleware(RegistrationMiddleware())


async def fetch_github_json(url: str):
    """Fetches and parses a JSON file from a URL using aiohttp."""
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                return await response.json()
    except aiohttp.ClientError as e:
        logger.error(f"Error fetching data from {url}: {e}")
        return None

async def get_hub_index(city: str):
    """
    Gets the resource hub index for a given city.
    Uses Redis cache with a 15-minute TTL.
    """
    cache_key = f"data:hub:{city}:index"
    cached_index = await redis_manager.get_json(cache_key)
    if cached_index:
        logger.info(f"Hub index for '{city}' found in cache.")
        return cached_index

    logger.info(f"Hub index for '{city}' not in cache. Fetching from GitHub.")
    index_url = f"{GITHUB_DATA_URL}/hub/index.json"
    full_index = await fetch_github_json(index_url)

    if not full_index or "items" not in full_index:
        return None

    # Filter items by the requested city
    city_index = {
        "version": full_index.get("version"),
        "items": [item for item in full_index["items"] if item.get("city", "").lower() == city.lower()]
    }

    if city_index["items"]:
        await redis_manager.set_json(cache_key, city_index, ttl=900) # 15 minutes TTL

    return city_index

@router.callback_query(F.data == "hub_menu")
async def hub_main_menu(callback: CallbackQuery):
    """Displays the main menu for the Resources Hub."""
    # This would typically get the user's city from their profile
    user_city = DEFAULT_CITY
    lang = await redis_manager.get_user_lang(callback.from_user.id) or "fa"

    index = await get_hub_index(user_city)
    if not index or not index.get("items"):
        await callback.answer("Sorry, no resources found for your city.", show_alert=True)
        return

    # Create a menu with categories
    categories = sorted(list(set(item['category'] for item in index['items'])))
    builder = InlineKeyboardBuilder()

    for category in categories:
        builder.button(text=f"📂 {category.capitalize()}", callback_data=f"hub_cat:{category}:0")

    builder.button(text=get_text("search", lang), callback_data="hub_search")
    builder.button(text=get_text("back_button", lang), callback_data="main_menu")
    builder.adjust(2)

    await callback.message.edit_text(
        f"📚 Resources Hub for {user_city}",
        reply_markup=builder.as_markup()
    )
    await callback.answer()

# Placeholder for pagination and content display
@router.callback_query(F.data.startswith("hub_cat:"))
async def show_category_items(callback: CallbackQuery):
    """Shows items in a category with pagination."""
    _, category, page_str = callback.data.split(":")
    page = int(page_str)

    # This is a simplified placeholder. A full implementation would:
    # 1. Get the hub index.
    # 2. Filter items for the selected category.
    # 3. Implement pagination logic (e.g., 6 items per page).
    # 4. Build a keyboard with item buttons and next/prev page buttons.

    await callback.answer(f"You selected category '{category}' on page {page}. This feature is under development.", show_alert=True)

# This is a placeholder to show how to get the content
async def get_resource_content(city: str, file_name: str):
    """Fetches content of a specific resource file."""
    url = f"{GITHUB_DATA_URL}/hub/{city.lower()}/{file_name}"
    # Add caching logic here as well
    return await fetch_github_json(url)
