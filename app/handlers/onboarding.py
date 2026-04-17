from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from aiogram import Bot, F, Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Document, Message, PhotoSize
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.db import add_event, get_app_setting
from app.keyboards import (
    admin_deposit_keyboard,
    fund_account_keyboard,
    join_premium_keyboard,
    single_button,
    yes_no_keyboard,
)
from app.models import User
from app.states import UserFlow
from app.texts import t

router = Router()


async def _current_user(session: AsyncSession, telegram_id: int) -> User | None:
    result = await session.execute(select(User).where(User.telegram_id == telegram_id))
    return result.scalar_one_or_none()


async def _save_file(bot: Bot, file_id: str, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    await bot.download(file_id, destination=destination)


async def _notify_admins_deposit(bot: Bot, user: User) -> None:
    caption = (
        f"{t('admin_deposit_caption', user.language)}\n\n"
        f"User: @{user.username or 'no_username'}\n"
        f"Telegram ID: {user.telegram_id}\n"
        f"State: {user.state}\n"
        f"File Type: {user.deposit_proof_file_type or '-'}"
    )

    for admin_id in settings.admin_chat_ids:
        if user.deposit_proof_file_type == "pdf":
            await bot.send_document(
                admin_id,
                document=user.deposit_proof_path,
                caption=caption,
                reply_markup=admin_deposit_keyboard(user.telegram_id),
            )
        else:
            await bot.send_photo(
                admin_id,
                photo=user.deposit_proof_path,
                caption=caption,
                reply_markup=admin_deposit_keyboard(user.telegram_id),
            )


@router.callback_query(F.data == "terms:accept")
async def accept_terms(callback: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    user = await _current_user(session, callback.from_user.id)
    if not user:
        await callback.answer("Please send /start first.", show_alert=True)
        return

    user.terms_accepted = True
    user.state = "CREATE_ACCOUNT"

    await add_event(session, user, "terms_accepted")
    await session.commit()

    await state.set_state(UserFlow.create_account)

    await callback.message.answer(
        t("create_account", user.language),
        reply_markup=single_button("Next", "flow:create_account_next"),
    )
    await callback.answer()


@router.callback_query(F.data == "flow:create_account_next")
async def create_account_next(callback: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    user = await _current_user(session, callback.from_user.id)
    if not user:
        await callback.answer("Please send /start first.", show_alert=True)
        return

    user.state = "VERIFY_IDENTITY"
    await session.commit()

    await state.set_state(UserFlow.verify_identity)

    await callback.message.answer(
        t("verify_identity", user.language),
        reply_markup=single_button("Next", "flow:verify_identity_next"),
    )
    await callback.answer()


@router.callback_query(F.data == "flow:verify_identity_next")
async def verify_identity_next(callback: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    user = await _current_user(session, callback.from_user.id)
    if not user:
        await callback.answer("Please send /start first.", show_alert=True)
        return

    user.state = "FUND_ACCOUNT"
    await session.commit()

    await state.set_state(UserFlow.fund_account)

    await callback.message.answer(
        t("fund_account", user.language),
        reply_markup=fund_account_keyboard(
            {
                "upload": "Upload Deposit Proof",
                "status": "Check Deposit Status",
            }
        ),
    )
    await callback.answer()


@router.callback_query(F.data == "deposit:upload")
async def deposit_upload_requested(callback: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    user = await _current_user(session, callback.from_user.id)
    if not user:
        await callback.answer("Please send /start first.", show_alert=True)
        return

    user.state = "WAITING_DEPOSIT_PROOF"
    await session.commit()

    await state.set_state(UserFlow.waiting_deposit_proof)

    await callback.message.answer(t("upload_deposit_prompt", user.language))
    await callback.answer()


@router.message(UserFlow.waiting_deposit_proof, F.photo)
async def deposit_photo_uploaded(message: Message, bot: Bot, state: FSMContext, session: AsyncSession) -> None:
    user = await _current_user(session, message.from_user.id)
    if not user:
        await message.answer("Please send /start first.")
        return

    photo: PhotoSize = message.photo[-1]
    file_path = settings.upload_path / f"deposit_{user.telegram_id}_{int(datetime.now().timestamp())}.jpg"

    await _save_file(bot, photo.file_id, file_path)

    user.deposit_proof_path = photo.file_id
    user.deposit_proof_file_type = "image"
    user.deposit_submitted_at = datetime.now(timezone.utc)
    user.deposit_approved_at = None
    user.deposit_confirmed = False
    user.state = "DEPOSIT_UNDER_REVIEW"

    await add_event(
        session,
        user,
        "deposit_uploaded",
        {
            "saved_file": str(file_path),
            "telegram_file_id": photo.file_id,
            "file_type": "image",
        },
    )
    await session.commit()

    await state.set_state(UserFlow.deposit_under_review)

    await message.answer(t("deposit_pending", user.language))
    await _notify_admins_deposit(bot, user)


@router.message(UserFlow.waiting_deposit_proof, F.document)
async def deposit_document_uploaded(message: Message, bot: Bot, state: FSMContext, session: AsyncSession) -> None:
    user = await _current_user(session, message.from_user.id)
    if not user:
        await message.answer("Please send /start first.")
        return

    doc: Document = message.document

    if doc.mime_type != "application/pdf":
        await message.answer(t("unsupported_file", user.language))
        return

    file_path = settings.upload_path / f"deposit_{user.telegram_id}_{int(datetime.now().timestamp())}.pdf"

    await _save_file(bot, doc.file_id, file_path)

    user.deposit_proof_path = doc.file_id
    user.deposit_proof_file_type = "pdf"
    user.deposit_submitted_at = datetime.now(timezone.utc)
    user.deposit_approved_at = None
    user.deposit_confirmed = False
    user.state = "DEPOSIT_UNDER_REVIEW"

    await add_event(
        session,
        user,
        "deposit_uploaded",
        {
            "saved_file": str(file_path),
            "telegram_file_id": doc.file_id,
            "file_type": "pdf",
        },
    )
    await session.commit()

    await state.set_state(UserFlow.deposit_under_review)

    await message.answer(t("deposit_pending", user.language))
    await _notify_admins_deposit(bot, user)


@router.message(UserFlow.waiting_deposit_proof)
async def invalid_deposit_upload(message: Message, session: AsyncSession) -> None:
    user = await _current_user(session, message.from_user.id)
    if not user:
        await message.answer("Please send /start first.")
        return

    await message.answer(t("unsupported_file", user.language))


@router.callback_query(F.data == "deposit:status")
async def deposit_status(callback: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    user = await _current_user(session, callback.from_user.id)
    if not user:
        await callback.answer("Please send /start first.", show_alert=True)
        return

    if user.deposit_confirmed:
        user.state = "RISK_STEP"
        await session.commit()

        await state.set_state(UserFlow.risk_step)

        await callback.message.answer(
            t("risk", user.language),
            reply_markup=yes_no_keyboard(),
        )
    else:
        if user.state == "DEPOSIT_UNDER_REVIEW":
            await callback.message.answer(t("deposit_pending", user.language))
        else:
            await callback.message.answer(t("status_waiting_deposit", user.language))

    await callback.answer()


@router.callback_query(F.data == "risk:yes")
async def risk_yes(callback: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    user = await _current_user(session, callback.from_user.id)
    if not user:
        await callback.answer("Please send /start first.", show_alert=True)
        return

    user.risk_completed = True
    user.premium_active = True
    user.premium_activated_at = datetime.now(timezone.utc)
    user.state = "PREMIUM_ACTIVE"

    await add_event(session, user, "risk_yes")
    await session.commit()

    await callback.message.answer(t("ready_to_trade", user.language))

    trading_video_file_id = await get_app_setting(
        session,
        "trading_video_file_id",
        settings.trading_video_file_id or "",
    )

    if trading_video_file_id:
        await callback.message.answer_video(video=trading_video_file_id)
    else:
        await callback.message.answer(t("trading_video_missing", user.language))

    await notify_user_premium(callback.bot, user)
    await callback.answer()


@router.callback_query(F.data == "risk:no")
async def risk_no(callback: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    user = await _current_user(session, callback.from_user.id)
    if not user:
        await callback.answer("Please send /start first.", show_alert=True)
        return

    await add_event(session, user, "risk_no")
    await session.commit()

    await callback.message.answer(
        t("risk_no", user.language),
        reply_markup=single_button("Next", "risk:no_next"),
    )
    await callback.answer()


@router.callback_query(F.data == "risk:no_next")
async def risk_no_next(callback: CallbackQuery, state: FSMContext, session: AsyncSession) -> None:
    user = await _current_user(session, callback.from_user.id)
    if not user:
        await callback.answer("Please send /start first.", show_alert=True)
        return

    user.risk_completed = True
    user.premium_active = True
    user.premium_activated_at = datetime.now(timezone.utc)
    user.state = "PREMIUM_ACTIVE"

    await add_event(session, user, "risk_no_next")
    await session.commit()

    await callback.message.answer(t("ready_to_trade", user.language))

    trading_video_file_id = await get_app_setting(
        session,
        "trading_video_file_id",
        settings.trading_video_file_id or "",
    )

    if trading_video_file_id:
        await callback.message.answer_video(video=trading_video_file_id)
    else:
        await callback.message.answer(t("trading_video_missing", user.language))

    await notify_user_premium(callback.bot, user)
    await callback.answer()


async def notify_user_premium(bot: Bot, user: User) -> None:
    if settings.premium_group_invite_link:
        await bot.send_message(
            user.telegram_id,
            t("premium_granted", user.language),
            reply_markup=join_premium_keyboard(settings.premium_group_invite_link),
        )
    else:
        await bot.send_message(
            user.telegram_id,
            t("premium_granted", user.language),
        )