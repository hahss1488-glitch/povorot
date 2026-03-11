from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def start_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Начать", callback_data="start_game")]])


def refreshable_options(options: list[str], prefix: str) -> InlineKeyboardMarkup:
    rows = [[InlineKeyboardButton(text=opt, callback_data=f"{prefix}:{opt}")] for opt in options]
    rows.append([InlineKeyboardButton(text="Обновить варианты", callback_data=f"refresh:{prefix}")])
    return InlineKeyboardMarkup(inline_keyboard=rows)


def build_confirm_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Начать игру", callback_data="confirm_build")],
            [InlineKeyboardButton(text="Пересобрать", callback_data="rebuild")],
        ]
    )


def action_keyboard(actions: list[tuple[str, str]]) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text=label, callback_data=f"act:{aid}")] for aid, label in actions]
    )


def new_game_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Новая игра", callback_data="start_game")]])
