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

st.set_page_config(
    page_title="FX Hustle Room Admin",
    page_icon="🚀",
    layout="wide",
)

st.markdown(
    """
    <style>
    .stApp {
        background:
            radial-gradient(circle at top left, rgba(124,58,237,0.22), transparent 28%),
            radial-gradient(circle at top right, rgba(56,189,248,0.18), transparent 25%),
            radial-gradient(circle at bottom left, rgba(16,185,129,0.14), transparent 22%),
            linear-gradient(135deg, #0b1020 0%, #111827 45%, #0f172a 100%);
        color: #f8fafc;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    h1, h2, h3, h4 {
        color: #f8fafc !important;
    }

    .hero-card {
        background: linear-gradient(135deg, rgba(30,41,59,0.92), rgba(15,23,42,0.92));
        border: 1px solid rgba(148,163,184,0.18);
        border-radius: 22px;
        padding: 24px 28px;
        box-shadow: 0 10px 35px rgba(0,0,0,0.28);
        margin-bottom: 1rem;
    }

    .metric-card {
        background: linear-gradient(135deg, rgba(17,24,39,0.94), rgba(30,41,59,0.92));
        border: 1px solid rgba(99,102,241,0.18);
        border-radius: 18px;
        padding: 14px 18px;
        box-shadow: 0 10px 26px rgba(0,0,0,0.22);
    }

    .section-card {
        background: rgba(15,23,42,0.88);
        border: 1px solid rgba(148,163,184,0.14);
        border-radius: 18px;
        padding: 20px;
        margin-top: 10px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.2);
    }

    div[data-testid="stMetric"] {
        background: transparent;
        border: none;
        box-shadow: none;
    }

    div[data-testid="stDataFrame"] {
        border-radius: 16px;
        overflow: hidden;
    }

    .small-note {
        color: #cbd5e1;
        font-size: 0.92rem;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="hero-card">
        <h1 style="margin:0;">FX Hustle Room Admin Panel</h1>
        <p class="small-note" style="margin-top:8px;">
            Web3-style admin dashboard for onboarding, deposit approval, and premium access control.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

engine = create_engine(settings.database_sync_url, future=True)


def load_users(search: str = "") -> pd.DataFrame:
    with Session(engine) as session:
        stmt = select(User)
        if search:
            term = f"%{search}%"
            stmt = stmt.where(
                (User.username.ilike(term))
                | (User.full_name.ilike(term))
                | (User.telegram_id.cast(String).ilike(term))
            )

        rows = session.execute(stmt.order_by(User.created_at.desc())).scalars().all()

        data = [
            {
                "telegram_id": u.telegram_id,
                "username": u.username or "",
                "full_name": u.full_name or "",
                "language": u.language,
                "deposit_confirmed": u.deposit_confirmed,
                "risk_completed": u.risk_completed,
                "premium_active": u.premium_active,
                "join_date": u.created_at,
                "deposit_proof_file_type": u.deposit_proof_file_type,
                "state": getattr(u, "state", None),
            }
            for u in rows
        ]
        return pd.DataFrame(data)


def metric_counts() -> tuple[int, int, int]:
    with Session(engine) as session:
        total = session.scalar(select(func.count()).select_from(User)) or 0
        deposit = (
            session.scalar(
                select(func.count()).select_from(User).where(User.deposit_confirmed.is_(True))
            )
            or 0
        )
        premium = (
            session.scalar(
                select(func.count()).select_from(User).where(User.premium_active.is_(True))
            )
            or 0
        )
        return total, deposit, premium


def manual_update(telegram_id: int, field: str, value: bool) -> bool:
    with Session(engine) as session:
        user = session.execute(
            select(User).where(User.telegram_id == telegram_id)
        ).scalar_one_or_none()

        if not user:
            return False

        setattr(user, field, value)

        if field == "premium_active" and value:
            user.deposit_confirmed = True
            user.risk_completed = True

        session.commit()
        return True


def deposit_proof_id(telegram_id: int) -> str | None:
    with Session(engine) as session:
        user = session.execute(
            select(User).where(User.telegram_id == telegram_id)
        ).scalar_one_or_none()

        if not user:
            return None

        return user.deposit_proof_path


total, deposit, premium = metric_counts()

m1, m2, m3 = st.columns(3)
with m1:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Total Users", total)
    st.markdown("</div>", unsafe_allow_html=True)
with m2:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Deposit Approved", deposit)
    st.markdown("</div>", unsafe_allow_html=True)
with m3:
    st.markdown('<div class="metric-card">', unsafe_allow_html=True)
    st.metric("Premium Active", premium)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("Users")

search = st.text_input("Search by username, full name, or Telegram ID")
df = load_users(search)

if not df.empty:
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("No users found.")
st.markdown("</div>", unsafe_allow_html=True)

left, right = st.columns(2)

with left:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Manual Actions")

    with st.form("manual_actions"):
        telegram_id = st.number_input("Telegram ID", step=1, format="%d")
        action = st.selectbox(
            "Action",
            ["deposit_confirmed", "risk_completed", "premium_active"],
        )
        value = st.checkbox("Set value to True", value=True)
        submitted = st.form_submit_button("Apply")

        if submitted:
            ok = manual_update(int(telegram_id), action, value)
            if ok:
                st.success("User updated successfully.")
            else:
                st.error("User not found.")
    st.markdown("</div>", unsafe_allow_html=True)

with right:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Deposit Proof Viewer")

    proof_user_id = st.number_input(
        "Telegram ID for deposit proof lookup",
        key="proof_lookup",
        step=1,
        format="%d",
    )

    if st.button("Load Deposit Proof ID"):
        deposit_proof = deposit_proof_id(int(proof_user_id))
        if deposit_proof:
            st.write({"deposit_proof_file_id": deposit_proof})
            st.info(
                "This is a Telegram file ID. Streamlit cannot directly preview Telegram-hosted files unless you download them through the Bot API."
            )
        else:
            st.warning("No deposit proof found for this user.")
    st.markdown("</div>", unsafe_allow_html=True)