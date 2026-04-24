from __future__ import annotations

import os
import asyncio
from contextlib import asynccontextmanager

import uvicorn
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Update
from fastapi import Depends, FastAPI, Request
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.middlewares.db import DbSessionMiddleware
from app.config import settings
from app.db import AsyncSessionLocal, init_db
from app.handlers.start import router as start_router
from app.handlers.onboarding import router as onboarding_router
from app.handlers.admin import router as admin_router
from app.handlers.signals import IncomingSignal, persist_signal, send_signal_to_premium_group


# ---------------- SETUP ----------------

settings.ensure_dirs()

logger.remove()
logger.add(lambda msg: print(msg, end=""), level=settings.log_level)


# ---------------- BOT ----------------

bot = Bot(
    token=settings.bot_token,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)

dp = Dispatcher(storage=MemoryStorage())

dp.include_router(start_router)
dp.include_router(onboarding_router)
dp.include_router(admin_router)

dp.update.middleware(DbSessionMiddleware())


# ---------------- DB ----------------

async def get_db_session():
    async with AsyncSessionLocal() as session:
        yield session


# ---------------- LIFESPAN ----------------

@asynccontextmanager
async def lifespan(app: FastAPI):

    try:
        await init_db()
        logger.info("Database initialized")
    except Exception as exc:
        logger.warning(f"Database initialization failed: {exc}")

    polling_task = None

    if settings.app_base_url.startswith("https"):

        webhook_url = f"{settings.app_base_url}/telegram/webhook"

        await bot.delete_webhook(drop_pending_updates=True)
        await bot.set_webhook(webhook_url)

        logger.info(f"Webhook set: {webhook_url}")

    else:

        logger.info("Running locally — starting polling")

        await bot.delete_webhook(drop_pending_updates=True)

        polling_task = asyncio.create_task(dp.start_polling(bot))

    yield

    logger.info("Shutting down bot")

    if polling_task:
        polling_task.cancel()

    await bot.session.close()


# ---------------- FASTAPI ----------------

app = FastAPI(
    title="FX Hustle Room API",
    lifespan=lifespan
)


@app.get("/health")
async def health():
    return {"status": "ok"}


# ---------------- TELEGRAM WEBHOOK ----------------

@app.post("/telegram/webhook")
async def telegram_webhook(request: Request):

    data = await request.json()

    update = Update.model_validate(data)  # ✅ FIX

    await dp.feed_update(bot, update)  # ✅ FIX

    return {"ok": True}


# ---------------- SIGNAL WEBHOOK ----------------

@app.post("/webhook/signal")
async def webhook_signal(
    payload: IncomingSignal,
    session: AsyncSession = Depends(get_db_session)
):

    signal = await persist_signal(session, payload)

    await send_signal_to_premium_group(bot, payload)

    return {
        "status": "ok",
        "signal_id": signal.id
    }


# ---------------- START ----------------

if __name__ == "__main__":

    port = int(os.getenv("PORT", settings.webhook_port))

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        reload=False
    )