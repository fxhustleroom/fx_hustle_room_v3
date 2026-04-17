from __future__ import annotations

from datetime import datetime, timezone

from aiogram import Bot, F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.db import add_event, set_app_setting
from app.models import User
from app.states import AdminFlow
from app.texts import t
from app.keyboards import yes_no_keyboard

router = Router()


def is_admin(user_id: int) -> bool:
    return user_id in settings.admin_chat_ids


@router.message(Command("admin_stats"))
async def admin_stats(message: Message, session: AsyncSession) -> None:
    if not is_admin(message.from_user.id):
        await message.answer(t("admin_only", settings.default_language))
        return

    total = await session.scalar(select(func.count()).select_from(User))
    deposits = await session.scalar(
        select(func.count()).select_from(User).where(User.deposit_confirmed.is_(True))
    )
    risk_completed = await session.scalar(
        select(func.count()).select_from(User).where(User.risk_completed.is_(True))
    )
    premium = await session.scalar(
        select(func.count()).select_from(User).where(User.premium_active.is_(True))
    )

    await message.answer(
        f"Users: {total or 0}\n"
        f"Deposit approved: {deposits or 0}\n"
        f"Risk completed: {risk_completed or 0}\n"
        f"Premium active: {premium or 0}"
    )


@router.message(Command("set_trading_video"))
async def set_trading_video_start(message: Message, state: FSMContext) -> None:
    if not is_admin(message.from_user.id):
        await message.answer(t("admin_only", settings.default_language))
        return
    await state.set_state(AdminFlow.waiting_trading_video)
    await message.answer("Please upload the Telegram trading video now.")


@router.message(AdminFlow.waiting_trading_video, F.video)
async def save_trading_video(message: Message, state: FSMContext, session: AsyncSession) -> None:
    if not is_admin(message.from_user.id):
        return
    await set_app_setting(session, "trading_video_file_id", message.video.file_id)
    await state.clear()
    await message.answer(t("saved", settings.default_language))


@router.message(Command("set_first_signal"))
async def set_first_signal_start(message: Message, state: FSMContext) -> None:
    if not is_admin(message.from_user.id):
        await message.answer(t("admin_only", settings.default_language))
        return
    await state.set_state(AdminFlow.waiting_first_signal_text)
    await message.answer("Send the first signal text now.")


@router.message(AdminFlow.waiting_first_signal_text)
async def save_first_signal(message: Message, state: FSMContext, session: AsyncSession) -> None:
    if not is_admin(message.from_user.id):
        return
    await set_app_setting(session, "first_signal_text", message.text or "")
    await state.clear()
    await message.answer(t("saved", settings.default_language))


@router.callback_query(F.data.startswith("admin:"))
async def handle_admin_actions(callback: CallbackQuery, bot: Bot, session: AsyncSession) -> None:
    if not is_admin(callback.from_user.id):
        await callback.answer(t("admin_only", settings.default_language), show_alert=True)
        return

    _, scope, action, user_telegram_id = callback.data.split(":")
    result = await session.execute(select(User).where(User.telegram_id == int(user_telegram_id)))
    user = result.scalar_one_or_none()

    if not user:
        await callback.answer("User not found", show_alert=True)
        return

    if scope != "deposit":
        await callback.answer("Trade approval flow has been removed.", show_alert=True)
        return

    if action == "approve":
        user.deposit_confirmed = True
        user.deposit_approved_at = datetime.now(timezone.utc)
        user.state = "RISK_STEP"
        await add_event(session, user, "deposit_approved", {"admin": callback.from_user.id})
        await session.commit()
        await bot.send_message(
            user.telegram_id,
            t("deposit_approved", user.language),
            reply_markup=yes_no_keyboard()
        )
    else:
        user.deposit_confirmed = False
        user.state = "WAITING_DEPOSIT_PROOF"
        await add_event(session, user, "deposit_rejected", {"admin": callback.from_user.id})
        await session.commit()
        await bot.send_message(user.telegram_id, t("deposit_rejected", user.language))

    await callback.answer("Done")