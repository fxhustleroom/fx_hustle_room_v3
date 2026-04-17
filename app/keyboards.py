from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from app.languages import LANGUAGES


def language_keyboard() -> InlineKeyboardMarkup:
    rows = []
    items = list(LANGUAGES.items())
    for i in range(0, len(items), 2):
        row = [InlineKeyboardButton(text=label, callback_data=f"lang:{code}") for code, label in items[i:i + 2]]
        rows.append(row)
    return InlineKeyboardMarkup(inline_keyboard=rows)


def single_button(text: str, callback_data: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text=text, callback_data=callback_data)]])


def fund_account_keyboard(language_texts: dict[str, str] | None = None) -> InlineKeyboardMarkup:
    upload = (language_texts or {}).get("upload", "Upload Deposit Proof")
    status = (language_texts or {}).get("status", "Check Deposit Status")
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=upload, callback_data="deposit:upload")],
            [InlineKeyboardButton(text=status, callback_data="deposit:status")],
        ]
    )


def yes_no_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="YES", callback_data="risk:yes")],
            [InlineKeyboardButton(text="NO", callback_data="risk:no")],
        ]
    )


def admin_deposit_keyboard(user_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Approve Deposit", callback_data=f"admin:deposit:approve:{user_id}")],
            [InlineKeyboardButton(text="Reject Deposit", callback_data=f"admin:deposit:reject:{user_id}")],
        ]
    )


def admin_trade_keyboard(user_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Approve Trade", callback_data=f"admin:trade:approve:{user_id}")],
            [InlineKeyboardButton(text="Reject Trade", callback_data=f"admin:trade:reject:{user_id}")],
        ]
    )


def join_premium_keyboard(invite_link: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Join Premium Group", url=invite_link)]])
