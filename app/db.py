from __future__ import annotations

import json
from collections.abc import AsyncGenerator
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from app.config import settings
from app.models import AppSetting, Base, Event, User


async_engine = create_async_engine(settings.database_url, echo=False, future=True)
AsyncSessionLocal = async_sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session


async def init_db() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    await seed_default_settings()


async def seed_default_settings() -> None:
    async with AsyncSessionLocal() as session:
        for key, value in {
            "trading_video_file_id": settings.trading_video_file_id or "",
            "first_signal_text": settings.first_signal_text,
        }.items():
            existing = await session.get(AppSetting, key)
            if not existing:
                session.add(AppSetting(key=key, value=value))
        await session.commit()


async def get_or_create_user(session: AsyncSession, telegram_id: int, username: str | None, full_name: str | None, language: str) -> User:
    result = await session.execute(select(User).where(User.telegram_id == telegram_id))
    user = result.scalar_one_or_none()
    if user is None:
        user = User(
            telegram_id=telegram_id,
            username=username,
            full_name=full_name,
            language=language,
        )
        session.add(user)
        await session.flush()
    else:
        user.username = username
        user.full_name = full_name
        if not user.language:
            user.language = language
    return user


async def add_event(session: AsyncSession, user: User, event_type: str, metadata: dict[str, Any] | None = None) -> None:
    session.add(Event(user_id=user.id, event_type=event_type, metadata_json=json.dumps(metadata or {})))


async def set_app_setting(session: AsyncSession, key: str, value: str) -> None:
    record = await session.get(AppSetting, key)
    if record:
        record.value = value
    else:
        session.add(AppSetting(key=key, value=value))
    await session.commit()


async def get_app_setting(session: AsyncSession, key: str, default: str | None = None) -> str | None:
    record = await session.get(AppSetting, key)
    if record and record.value is not None:
        return record.value
    return default
