from aiogram.fsm.state import State, StatesGroup


class UserFlow(StatesGroup):
    selecting_language = State()
    terms = State()
    create_account = State()
    verify_identity = State()
    fund_account = State()
    waiting_deposit_proof = State()
    deposit_under_review = State()
    risk_step = State()
    premium_active = State()


class AdminFlow(StatesGroup):
    waiting_trading_video = State()
    waiting_first_signal_text = State()
