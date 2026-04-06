from pathlib import Path
from typing import List

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    bot_token: str = Field(alias="BOT_TOKEN")
    database_url: str = Field(alias="DATABASE_URL")
    database_sync_url: str = Field(alias="DATABASE_SYNC_URL")
    admin_chat_ids: List[int] = Field(default_factory=list, alias="ADMIN_CHAT_IDS")
    premium_group_id: int = Field(alias="PREMIUM_GROUP_ID")
    premium_group_invite_link: str | None = Field(default=None, alias="PREMIUM_GROUP_INVITE_LINK")
    default_language: str = Field(default="en", alias="DEFAULT_LANGUAGE")
    upload_dir: str = Field(default="storage/uploads", alias="UPLOAD_DIR")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    webhook_host: str = Field(default="0.0.0.0", alias="WEBHOOK_HOST")
    webhook_port: int = Field(default=8080, alias="WEBHOOK_PORT")
    streamlit_port: int = Field(default=8501, alias="STREAMLIT_PORT")
    app_base_url: str = Field(default="http://localhost:8080", alias="APP_BASE_URL")
    trading_video_file_id: str | None = Field(default=None, alias="TRADING_VIDEO_FILE_ID")
    first_signal_text: str = Field(default="XAUUSD BUY, Entry: 2320.50, Stop Loss: 2315.00, Take Profit 1: 2325.00, Take Profit 2: 2330.00, Risk: 1.0%", alias="FIRST_SIGNAL_TEXT")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @field_validator("admin_chat_ids", mode="before")
    @classmethod
    def parse_admin_chat_ids(cls, value):
        if value in (None, "", []):
            return []
        if isinstance(value, list):
            return [int(v) for v in value]
        text = str(value).strip()
        if text.startswith("[") and text.endswith("]"):
            text = text[1:-1]
        return [int(part.strip()) for part in text.split(",") if part.strip()]

    @property
    def upload_path(self) -> Path:
        return Path(self.upload_dir)

    def ensure_dirs(self) -> None:
        self.upload_path.mkdir(parents=True, exist_ok=True)


settings = Settings()
