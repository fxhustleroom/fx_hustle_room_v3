from __future__ import annotations

import asyncio
from datetime import datetime, timezone
from pathlib import Path
import sys

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import pandas as pd
import streamlit as st
from aiogram import Bot
from sqlalchemy import String, create_engine, func, or_, select
from sqlalchemy.orm import Session

from app.config import settings
from app.keyboards import join_premium_keyboard, yes_no_keyboard
from app.models import User
from app.texts import t

st.set_page_config(
    page_title="FX Hustle Room Admin",
    layout="wide",
    initial_sidebar_state="collapsed",
)

engine = create_engine(settings.database_url, future=True)

st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(circle at top left, rgba(0, 255, 200, 0.10), transparent 25%),
            radial-gradient(circle at top right, rgba(138, 92, 246, 0.12), transparent 30%),
            linear-gradient(135deg, #0a0f1f 0%, #0d1328 40%, #070b16 100%);
        color: #f3f7ff;
    }

    .block-container {
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        max-width: 1420px;
    }

    .hero-card {
        background: linear-gradient(135deg, rgba(19, 30, 58, 0.95), rgba(10, 16, 32, 0.92));
        border: 1px solid rgba(80, 190, 255, 0.22);
        border-radius: 24px;
        padding: 28px 30px;
        box-shadow: 0 0 30px rgba(0, 255, 200, 0.08);
        margin-bottom: 22px;
    }

    .hero-title {
        font-size: 2.2rem;
        font-weight: 800;
        margin-bottom: 0.4rem;
        background: linear-gradient(90deg, #7cf7d4, #7aa2ff, #b48cff);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-subtitle {
        color: #9fb3d9;
        font-size: 0.98rem;
        line-height: 1.6;
    }

    .mini-label {
        font-size: 0.78rem;
        color: #7cf7d4;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        font-weight: 700;
        margin-bottom: 8px;
    }

    div[data-testid="stMetric"] {
        background: linear-gradient(180deg, rgba(20, 28, 52, 0.95), rgba(10, 15, 29, 0.92));
        border: 1px solid rgba(121, 163, 255, 0.18);
        border-radius: 20px;
        padding: 16px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.20);
    }

    div[data-testid="stMetricLabel"] {
        color: #8fa7d6 !important;
        font-weight: 600 !important;
    }

    div[data-testid="stMetricValue"] {
        color: #ffffff !important;
        font-weight: 800 !important;
    }

    .section-card {
        background: linear-gradient(180deg, rgba(18, 24, 46, 0.96), rgba(9, 14, 28, 0.92));
        border: 1px solid rgba(124, 247, 212, 0.10);
        border-radius: 22px;
        padding: 20px;
        margin-top: 14px;
        margin-bottom: 18px;
    }

    .action-card {
        background: linear-gradient(180deg, rgba(15, 21, 40, 0.98), rgba(8, 12, 24, 0.95));
        border: 1px solid rgba(120, 145, 255, 0.16);
        border-radius: 18px;
        padding: 16px;
        margin-bottom: 14px;
    }

    .user-name {
        font-size: 1.05rem;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 0.2rem;
    }

    .user-meta {
        color: #9fb3d9;
        font-size: 0.92rem;
        line-height: 1.6;
    }

    .stTextInput > div > div > input,
    .stNumberInput input,
    .stSelectbox div[data-baseweb="select"] > div {
        background: rgba(255,255,255,0.04) !important;
        color: white !important;
        border-radius: 14px !important;
        border: 1px solid rgba(125, 152, 255, 0.18) !important;
    }

    .stButton > button,
    .stFormSubmitButton > button {
        background: linear-gradient(90deg, #00d4ff, #7c4dff) !important;
        color: white !important;
        border: none !important;
        border-radius: 14px !important;
        font-weight: 700 !important;
        padding: 0.65rem 1.2rem !important;
        box-shadow: 0 8px 24px rgba(86, 95, 255, 0.35);
    }

    .stDataFrame, div[data-testid="stDataFrame"] {
        border-radius: 18px !important;
        overflow: hidden !important;
        border: 1px solid rgba(125, 152, 255, 0.14) !important;
    }

    h2, h3 {
        color: #f8fbff !important;
    }

    hr {
        border-color: rgba(255,255,255,0.08);
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def user_display_name(user: User) -> str:
    if getattr(user, "full_name", None):
        return str(user.full_name)
    if getattr(user, "username", None):
        return f"@{user.username}"
    return f"User {user.telegram_id}"


def load_users(search: str = "") -> pd.DataFrame:
    with Session(engine) as session:
        stmt = select(User)
        if search:
            term = f"%{search}%"
            stmt = stmt.where(
                or_(
                    User.username.ilike(term),
                    User.full_name.ilike(term),
                    User.telegram_id.cast(String).ilike(term),
                )
            )

        rows = session.execute(stmt.order_by(User.created_at.desc())).scalars().all()

        data = []
        for u in rows:
            data.append(
                {
                    "telegram_id": u.telegram_id,
                    "username": u.username or "",
                    "full_name": u.full_name or "",
                    "language": u.language or "",
                    "deposit_status": "Approved" if u.deposit_confirmed else "Pending",
                    "risk_status": "Completed" if u.risk_completed else "Pending",
                    "premium_status": "Active" if u.premium_active else "Pending",
                    "join_date": u.created_at,
                    "state": getattr(u, "state", "") or "",
                    "deposit_submitted_at": getattr(u, "deposit_submitted_at", None),
                    "deposit_proof_type": u.deposit_proof_file_type or "",
                    "trade_proof_type": u.first_trade_proof_file_type or "",
                }
            )

        return pd.DataFrame(data)


def metric_counts() -> tuple[int, int, int, int, int]:
    with Session(engine) as session:
        total = session.scalar(select(func.count()).select_from(User)) or 0
        deposit = session.scalar(
            select(func.count()).select_from(User).where(User.deposit_confirmed.is_(True))
        ) or 0
        risk = session.scalar(
            select(func.count()).select_from(User).where(User.risk_completed.is_(True))
        ) or 0
        premium = session.scalar(
            select(func.count()).select_from(User).where(User.premium_active.is_(True))
        ) or 0
        pending_deposits = session.scalar(
            select(func.count()).select_from(User).where(
                User.deposit_confirmed.is_(False),
                or_(
                    User.state == "DEPOSIT_UNDER_REVIEW",
                    User.deposit_submitted_at.is_not(None),
                    User.deposit_proof_path.is_not(None),
                ),
            )
        ) or 0
        return total, deposit, risk, premium, pending_deposits


def proof_ids(telegram_id: int) -> tuple[str | None, str | None]:
    with Session(engine) as session:
        user = session.execute(
            select(User).where(User.telegram_id == telegram_id)
        ).scalar_one_or_none()

        if not user:
            return None, None

        return user.deposit_proof_path, user.first_trade_proof_path


async def send_deposit_approved_message(user_id: int, language: str) -> None:
    bot = Bot(token=settings.bot_token)
    try:
        await bot.send_message(
            user_id,
            t("deposit_approved", language),
            reply_markup=yes_no_keyboard(),
        )
    finally:
        await bot.session.close()


async def send_deposit_rejected_message(user_id: int, language: str) -> None:
    bot = Bot(token=settings.bot_token)
    try:
        await bot.send_message(
            user_id,
            t("deposit_rejected", language),
        )
    finally:
        await bot.session.close()


async def send_premium_granted_message(user_id: int, language: str) -> None:
    bot = Bot(token=settings.bot_token)
    try:
        if settings.premium_group_invite_link:
            await bot.send_message(
                user_id,
                t("premium_granted", language),
                reply_markup=join_premium_keyboard(settings.premium_group_invite_link),
            )
        else:
            await bot.send_message(
                user_id,
                t("premium_granted", language),
            )
    finally:
        await bot.session.close()


def approve_deposit(telegram_id: int) -> tuple[bool, str]:
    with Session(engine) as session:
        user = session.execute(
            select(User).where(User.telegram_id == telegram_id)
        ).scalar_one_or_none()

        if not user:
            return False, "User not found."

        user.deposit_confirmed = True
        user.deposit_approved_at = datetime.now(timezone.utc)
        user.state = "RISK_STEP"
        user_language = user.language or "en"
        user_id = user.telegram_id

        session.commit()

    try:
        asyncio.run(send_deposit_approved_message(user_id, user_language))
    except Exception as e:
        return False, f"Deposit saved, but Telegram notify failed: {e}"

    return True, "Deposit approved and user notified."


def reject_deposit(telegram_id: int) -> tuple[bool, str]:
    with Session(engine) as session:
        user = session.execute(
            select(User).where(User.telegram_id == telegram_id)
        ).scalar_one_or_none()

        if not user:
            return False, "User not found."

        user.deposit_confirmed = False
        user.deposit_approved_at = None
        user.state = "WAITING_DEPOSIT_PROOF"
        user_language = user.language or "en"
        user_id = user.telegram_id

        session.commit()

    try:
        asyncio.run(send_deposit_rejected_message(user_id, user_language))
    except Exception as e:
        return False, f"Rejection saved, but Telegram notify failed: {e}"

    return True, "Deposit rejected and user notified."


def activate_premium(telegram_id: int) -> tuple[bool, str]:
    with Session(engine) as session:
        user = session.execute(
            select(User).where(User.telegram_id == telegram_id)
        ).scalar_one_or_none()

        if not user:
            return False, "User not found."

        user.deposit_confirmed = True
        user.risk_completed = True
        user.premium_active = True
        user.premium_activated_at = datetime.now(timezone.utc)
        user.state = "PREMIUM_ACTIVE"
        user_language = user.language or "en"
        user_id = user.telegram_id

        session.commit()

    try:
        asyncio.run(send_premium_granted_message(user_id, user_language))
    except Exception as e:
        return False, f"Premium saved, but Telegram notify failed: {e}"

    return True, "Premium activated and user notified."


def deactivate_premium(telegram_id: int) -> tuple[bool, str]:
    with Session(engine) as session:
        user = session.execute(
            select(User).where(User.telegram_id == telegram_id)
        ).scalar_one_or_none()

        if not user:
            return False, "User not found."

        user.premium_active = False
        user.state = "RISK_STEP" if user.deposit_confirmed else "WAITING_DEPOSIT_PROOF"

        session.commit()

    return True, "Premium deactivated."


def pending_deposit_users() -> list[User]:
    with Session(engine) as session:
        rows = session.execute(
            select(User)
            .where(
                User.deposit_confirmed.is_(False),
                or_(
                    User.state == "DEPOSIT_UNDER_REVIEW",
                    User.deposit_submitted_at.is_not(None),
                    User.deposit_proof_path.is_not(None),
                ),
            )
            .order_by(User.deposit_submitted_at.desc().nullslast(), User.created_at.desc())
        ).scalars().all()
        return rows


def debug_deposit_rows() -> pd.DataFrame:
    with Session(engine) as session:
        rows = session.execute(
            select(User).order_by(User.created_at.desc())
        ).scalars().all()

        data = []
        for u in rows:
            data.append(
                {
                    "telegram_id": u.telegram_id,
                    "username": u.username or "",
                    "state": u.state,
                    "deposit_confirmed": u.deposit_confirmed,
                    "deposit_submitted_at": u.deposit_submitted_at,
                    "deposit_proof_path": u.deposit_proof_path,
                    "deposit_proof_file_type": u.deposit_proof_file_type,
                    "created_at": u.created_at,
                }
            )
        return pd.DataFrame(data)


st.markdown(
    """
    <div class="hero-card">
        <div class="mini-label">Admin Dashboard</div>
        <div class="hero-title">FX Hustle Room Control Center</div>
        <div class="hero-subtitle">
            Review pending deposit uploads, approve or reject requests, activate premium,
            and inspect proof file IDs from one cleaner web3-style dashboard.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

total, deposit, risk, premium, pending_deposits_count = metric_counts()
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Total Users", total)
col2.metric("Deposit Approved", deposit)
col3.metric("Risk Completed", risk)
col4.metric("Premium Active", premium)
col5.metric("Pending Deposits", pending_deposits_count)

st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("Pending Deposit Approvals")
st.caption("Users who uploaded a deposit proof but are still waiting for admin review.")

pending_users = pending_deposit_users()

if not pending_users:
    st.success("No pending deposit approvals right now.")
else:
    for user in pending_users:
        st.markdown('<div class="action-card">', unsafe_allow_html=True)

        st.markdown(
            f"""
            <div class="user-name">{user_display_name(user)}</div>
            <div class="user-meta">
                Telegram ID: {user.telegram_id}<br>
                Username: @{user.username if user.username else "-"}<br>
                Language: {user.language or "-"}<br>
                Current State: {getattr(user, "state", "-") or "-"}<br>
                Deposit Proof Type: {user.deposit_proof_file_type or "-"}<br>
                Deposit Submitted At: {getattr(user, "deposit_submitted_at", "-") or "-"}
            </div>
            """,
            unsafe_allow_html=True,
        )

        deposit_proof = user.deposit_proof_path or "-"
        trade_proof = user.first_trade_proof_path or "-"

        st.code(
            f"deposit_proof_file_id: {deposit_proof}\nfirst_trade_proof_file_id: {trade_proof}",
            language="text",
        )

        a1, a2 = st.columns(2)
        with a1:
            if st.button("Approve Deposit", key=f"approve_deposit_{user.telegram_id}", width="stretch"):
                ok, msg = approve_deposit(int(user.telegram_id))
                if ok:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)

        with a2:
            if st.button("Reject Deposit", key=f"reject_deposit_{user.telegram_id}", width="stretch"):
                ok, msg = reject_deposit(int(user.telegram_id))
                if ok:
                    st.warning(msg)
                    st.rerun()
                else:
                    st.error(msg)

        st.markdown("</div>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("User Explorer")
search = st.text_input("Search by username, full name, or Telegram ID")
df = load_users(search)

if not df.empty:
    st.dataframe(df, width="stretch", hide_index=True)
else:
    st.info("No users found.")
st.markdown("</div>", unsafe_allow_html=True)

left, right = st.columns([1.15, 0.85])

with left:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Premium Access Control")
    st.caption("Deposit approval is now handled from the pending approvals section above.")

    with st.form("premium_actions"):
        telegram_id = st.number_input("Telegram ID", min_value=1, step=1, format="%d")
        action = st.selectbox(
            "Action",
            [
                "activate_premium",
                "deactivate_premium",
            ],
        )
        submitted = st.form_submit_button("Apply Action")

        if submitted:
            ok = False
            msg = "Unknown action."
            if action == "activate_premium":
                ok, msg = activate_premium(int(telegram_id))
            elif action == "deactivate_premium":
                ok, msg = deactivate_premium(int(telegram_id))

            if ok:
                st.success(msg)
                st.rerun()
            else:
                st.error(msg)
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Proof Viewer")
    st.caption("Telegram-hosted files cannot be previewed directly in Streamlit.")

    proof_user_id = st.number_input(
        "Telegram ID for proof lookup",
        key="proof_lookup",
        min_value=1,
        step=1,
        format="%d",
    )

    if st.button("Load Proof IDs"):
        deposit_proof, trade_proof = proof_ids(int(proof_user_id))
        if not deposit_proof and not trade_proof:
            st.warning("No proof files found for this user.")
        else:
            st.json(
                {
                    "deposit_proof_file_id": deposit_proof,
                    "first_trade_proof_file_id": trade_proof,
                }
            )
            st.info(
                "These are Telegram file IDs. The bot can resend them, but Streamlit cannot render Telegram-hosted files directly."
            )
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("Debug Deposit State")
st.caption("Use this to confirm what the bot is actually saving to the database.")
debug_df = debug_deposit_rows()
if not debug_df.empty:
    st.dataframe(debug_df, width="stretch", hide_index=True)
else:
    st.info("No users found.")
st.markdown("</div>", unsafe_allow_html=True)