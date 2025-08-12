import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request, Response
from aiogram import Bot, Dispatcher
from aiogram.types import Update

from config import (
    TELEGRAM_BOT_TOKEN, BASE_URL, WEBHOOK_SECRET, PORT,
    logger
)
from handlers import all_routers
from utils.redis_utils import redis_manager
from utils.gsheets import gsheets_manager

# Aiogram Bot and Dispatcher
bot = Bot(token=TELEGRAM_BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles startup and shutdown events for the FastAPI application.
    """
    # --- Startup ---
    logger.info("Application startup...")
    # Include all routers from the handlers package
    dp.include_routers(*all_routers)

    # Initialize external services
    await redis_manager.initialize()
    await gsheets_manager.initialize()

    # Set Telegram webhook
    webhook_url = f"{BASE_URL}/telegram/webhook"
    await bot.set_webhook(
        url=webhook_url,
        secret_token=WEBHOOK_SECRET,
        allowed_updates=['message', 'callback_query', 'chat_member']
    )
    logger.info(f"Webhook set to {webhook_url}")

    yield

    # --- Shutdown ---
    logger.info("Application shutdown...")
    # Close external service connections
    await redis_manager.close()

    # Delete Telegram webhook
    await bot.delete_webhook()
    logger.info("Webhook deleted.")


# FastAPI application
app = FastAPI(lifespan=lifespan)

@app.post("/telegram/webhook")
async def telegram_webhook(request: Request):
    """
    Handles incoming updates from Telegram.
    Verifies the secret token and feeds the update to the dispatcher.
    """
    secret_token = request.headers.get("X-Telegram-Bot-Api-Secret-Token")
    if secret_token != WEBHOOK_SECRET:
        logger.warning("Webhook received with invalid secret token.")
        return Response(status_code=403)

    try:
        update_data = await request.json()
        update = Update.model_validate(update_data, context={"bot": bot})
        await dp.feed_update(bot=bot, update=update)
    except Exception as e:
        logger.error(f"Error processing update: {e}")
        # Log the problematic update data for debugging if possible
        # logger.debug(f"Update data: {update_data}")

    return Response(status_code=200)

@app.get("/health")
async def health_check():
    """Simple health check endpoint to confirm the service is running."""
    return {"status": "ok"}

@app.get("/ready")
async def readiness_check():
    """
    Readiness check endpoint to confirm the service and its dependencies are ready.
    """
    # Check Redis connection
    redis_ok = False
    if redis_manager.redis:
        try:
            await redis_manager.redis.ping()
            redis_ok = True
        except Exception:
            redis_ok = False

    # Check Google Sheets connection
    gsheets_ok = gsheets_manager.spreadsheet is not None

    if redis_ok and gsheets_ok:
        return {"status": "ready", "redis": "ok", "gsheets": "ok"}

    return Response(
        content=f'{{"status": "not_ready", "redis": "{'ok' if redis_ok else 'error'}", "gsheets": "{'ok' if gsheets_ok else 'error'}"}}',
        status_code=503,
        media_type="application/json"
    )

if __name__ == "__main__":
    """
    Allows running the application directly for local development.
    `uvicorn main:app --reload` is the recommended way.
    """
    uvicorn.run(app, host="0.0.0.0", port=PORT)
