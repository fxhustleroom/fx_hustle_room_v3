from datetime import datetime
from decimal import Decimal

from sqlalchemy import BigInteger, Boolean, DateTime, ForeignKey, Integer, Numeric, String, Text, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    telegram_id: Mapped[int] = mapped_column(BigInteger, unique=True, index=True)
    username: Mapped[str | None] = mapped_column(String(255), nullable=True)
    full_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    language: Mapped[str] = mapped_column(String(8), default="en")
    state: Mapped[str] = mapped_column(String(64), default="LANGUAGE_SELECTION")

    terms_accepted: Mapped[bool] = mapped_column(Boolean, default=False)
    deposit_confirmed: Mapped[bool] = mapped_column(Boolean, default=False)
    risk_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    first_signal_sent: Mapped[bool] = mapped_column(Boolean, default=False)
    first_trade_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    premium_active: Mapped[bool] = mapped_column(Boolean, default=False)

    deposit_proof_path: Mapped[str | None] = mapped_column(Text, nullable=True)
    deposit_proof_file_type: Mapped[str | None] = mapped_column(String(16), nullable=True)
    deposit_submitted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    deposit_approved_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    first_trade_proof_path: Mapped[str | None] = mapped_column(Text, nullable=True)
    first_trade_proof_file_type: Mapped[str | None] = mapped_column(String(16), nullable=True)
    first_trade_submitted_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    premium_activated_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    events: Mapped[list["Event"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class Event(Base):
    __tablename__ = "events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), index=True)
    event_type: Mapped[str] = mapped_column(String(100), index=True)
    metadata_json: Mapped[str | None] = mapped_column(Text, nullable=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user: Mapped[User] = relationship(back_populates="events")


class Signal(Base):
    __tablename__ = "signals"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    pair: Mapped[str] = mapped_column(String(20), index=True)
    direction: Mapped[str] = mapped_column(String(10))
    entry: Mapped[Decimal] = mapped_column(Numeric(12, 4))
    sl: Mapped[Decimal] = mapped_column(Numeric(12, 4))
    tp1: Mapped[Decimal | None] = mapped_column(Numeric(12, 4), nullable=True)
    tp2: Mapped[Decimal | None] = mapped_column(Numeric(12, 4), nullable=True)
    risk_percentage: Mapped[Decimal | None] = mapped_column(Numeric(6, 2), nullable=True)
    chart_image_url: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())


class AppSetting(Base):
    __tablename__ = "app_settings"

    key: Mapped[str] = mapped_column(String(100), primary_key=True)
    value: Mapped[str | None] = mapped_column(Text, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())