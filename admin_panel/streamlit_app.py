from __future__ import annotations

from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))
import pandas as pd
import streamlit as st
from sqlalchemy import String, create_engine, func, select
from sqlalchemy.orm import Session

from app.config import settings
from app.models import User

st.set_page_config(page_title="FX Hustle Room Admin", layout="wide")
st.title("FX Hustle Room Admin Panel")

engine = create_engine(settings.database_sync_url, future=True)


def load_users(search: str = "") -> pd.DataFrame:
    with Session(engine) as session:
        stmt = select(User)
        if search:
            term = f"%{search}%"
            stmt = stmt.where((User.username.ilike(term)) | (User.full_name.ilike(term)) | (User.telegram_id.cast(String).ilike(term)))
        rows = session.execute(stmt.order_by(User.created_at.desc())).scalars().all()
        data = [
            {
                "telegram_id": u.telegram_id,
                "username": u.username,
                "language": u.language,
                "deposit_confirmed": u.deposit_confirmed,
                "risk_completed": u.risk_completed,
                "first_trade_completed": u.first_trade_completed,
                "premium_active": u.premium_active,
                "join_date": u.created_at,
                "deposit_proof_file_type": u.deposit_proof_file_type,
                "first_trade_proof_file_type": u.first_trade_proof_file_type,
            }
            for u in rows
        ]
        return pd.DataFrame(data)


def metric_counts() -> tuple[int, int, int, int]:
    with Session(engine) as session:
        total = session.scalar(select(func.count()).select_from(User)) or 0
        deposit = session.scalar(select(func.count()).select_from(User).where(User.deposit_confirmed.is_(True))) or 0
        trade = session.scalar(select(func.count()).select_from(User).where(User.first_trade_completed.is_(True))) or 0
        premium = session.scalar(select(func.count()).select_from(User).where(User.premium_active.is_(True))) or 0
        return total, deposit, trade, premium


def manual_update(telegram_id: int, field: str, value: bool) -> None:
    with Session(engine) as session:
        user = session.execute(select(User).where(User.telegram_id == telegram_id)).scalar_one_or_none()
        if user:
            setattr(user, field, value)
            if field == "premium_active" and value:
                user.first_trade_completed = True
                user.deposit_confirmed = True
                user.risk_completed = True
            session.commit()


def proof_ids(telegram_id: int) -> tuple[str | None, str | None]:
    with Session(engine) as session:
        user = session.execute(select(User).where(User.telegram_id == telegram_id)).scalar_one_or_none()
        if not user:
            return None, None
        return user.deposit_proof_path, user.first_trade_proof_path


total, deposit, trade, premium = metric_counts()
col1, col2, col3, col4 = st.columns(4)
col1.metric("Users", total)
col2.metric("Deposit Approved", deposit)
col3.metric("First Trade Approved", trade)
col4.metric("Premium Active", premium)

search = st.text_input("Search by username, name, or Telegram ID")
df = load_users(search)
st.subheader("Users")
st.dataframe(df, use_container_width=True)

st.subheader("Manual Actions")
with st.form("manual_actions"):
    telegram_id = st.number_input("Telegram ID", step=1, format="%d")
    action = st.selectbox("Action", ["deposit_confirmed", "risk_completed", "first_trade_completed", "premium_active"])
    value = st.checkbox("Set value to True", value=True)
    submitted = st.form_submit_button("Apply")
    if submitted:
        manual_update(int(telegram_id), action, value)
        st.success("Updated")

st.subheader("Proof Viewer")
proof_user_id = st.number_input("Telegram ID for proof lookup", key="proof_lookup", step=1, format="%d")
if st.button("Load Proof IDs"):
    deposit_proof, trade_proof = proof_ids(int(proof_user_id))
    st.write({"deposit_proof_file_id": deposit_proof, "first_trade_proof_file_id": trade_proof})
    st.info("These are Telegram file IDs. The bot can resend them, but Streamlit cannot directly preview Telegram-hosted files without downloading them through the Bot API.")
