from aiogram.fsm.state import State, StatesGroup


class GameFSM(StatesGroup):
    waiting_for_name = State()
    waiting_for_item = State()
    waiting_for_location = State()
    waiting_for_fear = State()
    waiting_for_build_confirm = State()
    waiting_for_turn_action = State()
