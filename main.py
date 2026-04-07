from __future__ import annotations

import asyncio
import os
from contextlib import asynccontextmanager

import uvicorn
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from fastapi import Depends, FastAPI
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.middlewares.db import DbSessionMiddleware
from app.config import settings
from app.db import AsyncSessionLocal, init_db
from app.handlers import admin, onboarding, start
from app.handlers.signals import IncomingSignal, persist_signal, send_signal_to_premium_group

# --------------------------------------------------
# Setup
# --------------------------------------------------

settings.ensure_dirs()

logger.remove()
logger.add(lambda msg: print(msg, end=""), level=settings.log_level)

# --------------------------------------------------
# Telegram bot
# --------------------------------------------------

bot = Bot(
    token=settings.bot_token,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML),
)

dp = Dispatcher(storage=MemoryStorage())

dp.include_router(start.router)
dp.include_router(onboarding.router)
dp.include_router(admin.router)

dp.update.middleware(DbSessionMiddleware())

# --------------------------------------------------
# Database dependency
# --------------------------------------------------

async def get_db_session():
    async with AsyncSessionLocal() as session:
        yield session

# --------------------------------------------------
# FastAPI lifespan
# --------------------------------------------------

@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_db()
    logger.info("Database initialized")
    yield

# --------------------------------------------------
# FastAPI app
# --------------------------------------------------

app = FastAPI(
    title="FX Hustle Room Webhook API",
    lifespan=lifespan
)

@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok"}

@app.post("/webhook/signal")
async def webhook_signal(
    payload: IncomingSignal,
    session: AsyncSession = Depends(get_db_session)
) -> dict[str, str | int]:

    signal = await persist_signal(session, payload)

    await send_signal_to_premium_group(bot, payload)

    return {
        "status": "ok",
        "signal_id": signal.id
    }

# --------------------------------------------------
# API server runner (Railway compatible)
# --------------------------------------------------

async def run_api() -> None:

    port = int(os.getenv("PORT", settings.webhook_port))

    config = uvicorn.Config(
        app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )

    server = uvicorn.Server(config)

    await server.serve()

# --------------------------------------------------
# Main runner
# --------------------------------------------------

async def main() -> None:
    await bot.delete_webhook(drop_pending_updates=True)

    await init_db()

    logger.info("Starting Telegram bot polling and webhook API")

    await asyncio.gather(
        dp.start_polling(bot),
        run_api(),
    )

# --------------------------------------------------
# Entry point
# --------------------------------------------------

if __name__ == "__main__":
    asyncio.run(main())
