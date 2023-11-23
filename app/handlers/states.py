from aiogram.fsm.state import StatesGroup, State


class AddUser(StatesGroup):
    add_user_contact = State()


class AddAuto(StatesGroup):
    enter_number = State()
    enter_model = State()
    confirm = State()


class DeleteAuto(StatesGroup):
    enter_number = State()
    confirm = State()


class SearchAuto(StatesGroup):
    enter_number = State()
