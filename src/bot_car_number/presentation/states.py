from aiogram.fsm.state import State, StatesGroup


class AddUserState(StatesGroup):
    add_user_contact = State()


class AddAutoState(StatesGroup):
    enter_number = State()
    enter_model = State()
    confirm = State()


class RemoveAutoState(StatesGroup):
    enter_number = State()
    confirm = State()


class SearchAutoState(StatesGroup):
    enter_number = State()


class BlockAutoState(StatesGroup):
    enter_number = State()
    confirm = State()
