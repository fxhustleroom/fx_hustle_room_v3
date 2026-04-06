from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.db import add_event, get_or_create_user
from app.keyboards import language_keyboard, single_button
from app.languages import TELEGRAM_TO_SUPPORTED
from app.states import UserFlow
from app.texts import t

router = Router()


@router.message(CommandStart())
async def start_handler(message: Message, state: FSMContext, session: AsyncSession) -> None:
    logger.info(f"Start command received from user {message.from_user.id}")
    language_code = TELEGRAM_TO_SUPPORTED.get((message.from_user.language_code or "").split("-")[0], settings.default_language)
    await get_or_create_user(
        session,
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        full_name=message.from_user.full_name,
        language=language_code,
    )
    await session.commit()
    await state.set_state(UserFlow.selecting_language)
    await message.answer(t("select_language", language_code), reply_markup=language_keyboard())


@router.callback_query(F.data.startswith("lang:"))
async def language_selected(callback: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    code = callback.data.split(":", 1)[1]
    user = await get_or_create_user(
        session,
        telegram_id=callback.from_user.id,
        username=callback.from_user.username,
        full_name=callback.from_user.full_name,
        language=code,
    )
    user.language = code
    user.state = "TERMS"
    await add_event(session, user, "language_selected", {"language": code})
    await session.commit()
    await state.set_state(UserFlow.terms)
    await callback.message.answer(t("welcome", code))
    await callback.message.answer(t("terms", code), reply_markup=single_button("I Accept", "terms:accept"))
    await callback.answer()
