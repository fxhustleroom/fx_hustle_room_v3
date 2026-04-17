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
    layout="wide",
    initial_sidebar_state="collapsed",
)

engine = create_engine(settings.database_sync_url, future=True)


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
        max-width: 1400px;
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

    .status-pill {
        display: inline-block;
        padding: 0.35rem 0.7rem;
        border-radius: 999px;
        font-size: 0.76rem;
        font-weight: 700;
        margin-right: 6px;
    }

    .ok-pill {
        background: rgba(27, 212, 164, 0.14);
        color: #7cf7d4;
        border: 1px solid rgba(124, 247, 212, 0.20);
    }

    .warn-pill {
        background: rgba(255, 183, 77, 0.12);
        color: #ffce73;
        border: 1px solid rgba(255, 183, 77, 0.18);
    }

    .danger-pill {
        background: rgba(255, 90, 95, 0.12);
        color: #ff8a8f;
        border: 1px solid rgba(255, 90, 95, 0.20);
    }

    h2, h3 {
        color: #f8fbff !important;
    }
    </style>
    """,
    unsafe_allow_html=True,
)


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

        data = []
        for u in rows:
            access_status = "Premium" if u.premium_active else "Pending"
            deposit_status = "Approved" if u.deposit_confirmed else "Pending"
            risk_status = "Completed" if u.risk_completed else "Pending"

            data.append(
                {
                    "telegram_id": u.telegram_id,
                    "username": u.username or "",
                    "full_name": u.full_name or "",
                    "language": u.language,
                    "deposit_status": deposit_status,
                    "risk_status": risk_status,
                    "premium_status": access_status,
                    "join_date": u.created_at,
                    "deposit_proof_type": u.deposit_proof_file_type or "",
                    "trade_proof_type": u.first_trade_proof_file_type or "",
                }
            )

        return pd.DataFrame(data)


def metric_counts() -> tuple[int, int, int, int]:
    with Session(engine) as session:
        total = session.scalar(select(func.count()).select_from(User)) or 0
        deposit = (
            session.scalar(
                select(func.count()).select_from(User).where(User.deposit_confirmed.is_(True))
            )
            or 0
        )
        risk = (
            session.scalar(
                select(func.count()).select_from(User).where(User.risk_completed.is_(True))
            )
            or 0
        )
        premium = (
            session.scalar(
                select(func.count()).select_from(User).where(User.premium_active.is_(True))
            )
            or 0
        )
        return total, deposit, risk, premium


def manual_update(telegram_id: int, field: str, value: bool) -> bool:
    with Session(engine) as session:
        user = session.execute(
            select(User).where(User.telegram_id == telegram_id)
        ).scalar_one_or_none()

        if not user:
            return False

        setattr(user, field, value)

        # premium access now depends on deposit + risk only
        if field == "premium_active" and value:
            user.deposit_confirmed = True
            user.risk_completed = True

        session.commit()
        return True


def proof_ids(telegram_id: int) -> tuple[str | None, str | None]:
    with Session(engine) as session:
        user = session.execute(
            select(User).where(User.telegram_id == telegram_id)
        ).scalar_one_or_none()

        if not user:
            return None, None

        return user.deposit_proof_path, user.first_trade_proof_path


st.markdown(
    """
    <div class="hero-card">
        <div class="mini-label">Admin Dashboard</div>
        <div class="hero-title">FX Hustle Room Control Center</div>
        <div class="hero-subtitle">
            Manage user onboarding, deposit approval, risk-step completion, premium activation,
            and proof lookup from a cleaner web3-style dashboard.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

total, deposit, risk, premium = metric_counts()
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Users", total)
col2.metric("Deposit Approved", deposit)
col3.metric("Risk Completed", risk)
col4.metric("Premium Active", premium)

st.markdown('<div class="section-card">', unsafe_allow_html=True)
st.subheader("User Explorer")
search = st.text_input("Search by username, full name, or Telegram ID")
df = load_users(search)

if not df.empty:
    st.dataframe(df, use_container_width=True, hide_index=True)
else:
    st.info("No users found.")
st.markdown("</div>", unsafe_allow_html=True)

left, right = st.columns([1.15, 0.85])

with left:
    st.markdown('<div class="section-card">', unsafe_allow_html=True)
    st.subheader("Manual Actions")
    st.caption("Trade approval has been removed from this admin page.")

    with st.form("manual_actions"):
        telegram_id = st.number_input("Telegram ID", min_value=1, step=1, format="%d")
        action = st.selectbox(
            "Action",
            [
                "deposit_confirmed",
                "risk_completed",
                "premium_active",
            ],
        )
        value = st.checkbox("Set value to True", value=True)
        submitted = st.form_submit_button("Apply Update")

        if submitted:
            ok = manual_update(int(telegram_id), action, value)
            if ok:
                st.success("User updated successfully.")
            else:
                st.error("User not found.")
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