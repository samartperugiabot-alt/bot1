import datetime
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, CallbackQuery

from ..utils.i18n import get_text
from ..utils.gsheets import gsheets_manager
from ..utils.redis_utils import redis_manager
from ..config import QUESTIONS_SHEET_NAME, DEFAULT_LANG
from ..utils.gates import RegistrationMiddleware

router = Router(name="question")
# This handler requires registration
router.callback_query.middleware(RegistrationMiddleware())
router.message.middleware(RegistrationMiddleware())


class QuestionStates(StatesGroup):
    asking_question = State()

@router.callback_query(F.data == "qna_menu", flags={"require_registration": True})
async def start_qna(callback: CallbackQuery, state: FSMContext):
    """Initiates the question asking process."""
    user_id = callback.from_user.id
    lang = await redis_manager.get_user_lang(user_id) or DEFAULT_LANG

    # In a real implementation, you would first search the FAQ from a JSON file.
    # For simplicity, we go straight to asking a question.
    await state.set_state(QuestionStates.asking_question)
    await callback.message.edit_text(
        "📝 Please type your question. You can also send an image or a short voice message."
    )
    await callback.answer()

@router.message(QuestionStates.asking_question)
async def process_question(message: Message, state: FSMContext):
    """Saves the user's question to Google Sheets."""
    await state.clear()
    user_id = message.from_user.id
    lang = await redis_manager.get_user_lang(user_id) or DEFAULT_LANG

    question_text = message.text or message.caption or ""
    media_link = "" # Placeholder for file link if uploaded to Drive

    # Here you would add logic to handle message.voice, message.photo, etc.
    # and upload them to Google Drive to get a `media_link`.

    question_data = [
        # id, telegram_id, ts, lang, question_text, media_link, status, admin_answer, answer_ts
        f"q_{int(datetime.datetime.utcnow().timestamp())}", # a unique ID
        user_id,
        datetime.datetime.utcnow().isoformat(),
        lang,
        question_text,
        media_link,
        "pending", # Initial status
        "", # Admin answer
        "", # Answer timestamp
    ]

    await gsheets_manager.append_row_to_sheet(QUESTIONS_SHEET_NAME, question_data)

    await message.answer(
        "✅ Your question has been submitted. Our admins will review it and answer as soon as possible."
    )

    # Here you would also send a notification to the ADMIN_CHAT_ID.
    # bot.send_message(ADMIN_CHAT_ID, f"New question from {user_id}: {question_text}")
    # This needs the `bot` object, which is typically passed via middleware or context.
