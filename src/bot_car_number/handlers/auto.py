from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from bot_car_number.config import MAX_AUTO_COUNT, MAX_AUTO_NAME_LEN
from bot_car_number.db.gateways.auto import DatabaseAutoGateway
from bot_car_number.db.gateways.user import DatabaseUserGateway
from bot_car_number.entities.auto import Auto
from bot_car_number.handlers.menu import get_autos_menu
from bot_car_number.handlers.states import AddAuto, DeleteAuto
from bot_car_number.keyboards.inline_keyboard import (
    back_kb,
    confirm_del_kb,
    save_kb,
)
from bot_car_number.misc import msg
from bot_car_number.misc.cmd import Command as cmd
from bot_car_number.services.auto_service import AutoService
from bot_car_number.services.user_service import UserService

router = Router(name="auto_commands-router")

BACK_KB = back_kb(cmd.AUTO_MENU)


@router.callback_query(F.data == cmd.AUTO_MENU)
async def auto_menu(
    call: CallbackQuery,
    state: FSMContext,
    user_service: UserService,
    user_dao: DatabaseUserGateway,
    auto_service: AutoService,
    auto_dao: DatabaseAutoGateway,
) -> None:
    """Обработчик вызова меню управления автомобилями пользователя."""
    await get_autos_menu(
        call,
        state,
        user_service,
        user_dao,
        auto_service,
        auto_dao,
    )


@router.callback_query(StateFilter(None), F.data == cmd.AUTO_ADD)
async def add_auto(
    call: CallbackQuery,
    state: FSMContext,
    user_service: UserService,
    auto_service: AutoService,
    user_dao: DatabaseUserGateway,
    auto_dao: DatabaseAutoGateway,
) -> None:
    """Обработчик перехода к добавлению автомобиля."""
    user = await user_service.get_user_by_telegram_id(
        user_dao, call.from_user.id
    )
    if user:
        autos = await auto_service.get_user_autos(auto_dao, user.id)
        if len(autos) >= MAX_AUTO_COUNT:
            await call.answer(msg.AUTO_MAX_COUNT_MSG, True)
            return
        await call.message.edit_text(
            msg.AUTO_ENTER_NUMBER_MSG, reply_markup=BACK_KB
        )
        await state.update_data(user_id=user.id)
        await state.set_state(AddAuto.enter_number)


@router.message(AddAuto.enter_number)
async def add_number(
    message: Message,
    state: FSMContext,
    auto_dao: DatabaseAutoGateway,
    auto_service: AutoService,
) -> None:
    """Обработчик ввода номера автомобиля при добавлении."""
    number = message.text.upper()
    if not auto_service.validate_number(number):
        await message.answer(msg.AUTO_FORMAT_ERR_MSG, reply_markup=BACK_KB)
        return
    if await auto_service.get_auto_by_number(auto_dao, number):
        await message.answer(msg.AUTO_EXIST_MSG, reply_markup=BACK_KB)
        return
    await message.answer(msg.AUTO_ADD_MODEL_MSG, reply_markup=BACK_KB)
    await state.update_data(number=number)
    await state.set_state(AddAuto.enter_model)


@router.message(AddAuto.enter_model)
async def add_model(
    message: Message,
    state: FSMContext,
) -> None:
    """Обработчик ввода марки автомобиля."""
    if len(message.text) > MAX_AUTO_NAME_LEN:
        await message.answer(msg.AUTO_MODEL_LONG_MSG, reply_markup=BACK_KB)
        return
    data = await state.get_data()
    model = message.text
    await message.answer(
        msg.AUTO_CHECK_DATA_MSG.format(data["number"], model),
        reply_markup=save_kb(cmd.AUTO_MENU),
    )
    await state.update_data(model=model)
    await state.set_state(AddAuto.confirm)


@router.callback_query(AddAuto.confirm, F.data == cmd.AUTO_SAVE)
async def add_auto_confirm(
    call: CallbackQuery,
    state: FSMContext,
    user_service: UserService,
    auto_service: AutoService,
    user_dao: DatabaseUserGateway,
    auto_dao: DatabaseAutoGateway,
) -> None:
    """Обработчик подтверждения добавления автомобиля в БД."""
    data = await state.get_data()
    if not await auto_service.get_auto_by_number(auto_dao, data["number"]):
        auto = Auto(
            id=None,
            number=data["number"],
            model=data["model"],
            user_id=data["user_id"],
        )
        await auto_service.add_auto(auto_dao, auto)
    await get_autos_menu(
        call,
        state,
        user_service,
        user_dao,
        auto_service,
        auto_dao,
    )


@router.callback_query(StateFilter(None), F.data == cmd.AUTO_DEL)
async def delete_auto(
    call: CallbackQuery,
    state: FSMContext,
    user_dao: DatabaseUserGateway,
    auto_dao: DatabaseAutoGateway,
    user_service: UserService,
    auto_service: AutoService,
) -> None:
    """Обработчик нажатия кнопки удаления автомобиля."""
    user = await user_service.get_user_by_telegram_id(
        user_dao, call.from_user.id
    )
    if user:
        autos = await auto_service.get_user_autos(auto_dao, user.id)
        if not autos:
            await call.answer(msg.AUTO_NONE_MSG, True)
            return
        await call.message.edit_text(
            msg.AUTO_ENTER_NUMBER_MSG, reply_markup=BACK_KB
        )
        await state.set_state(state=DeleteAuto.enter_number)


@router.message(DeleteAuto.enter_number)
async def enter_number(
    message: Message,
    state: FSMContext,
    user_service: UserService,
    user_dao: DatabaseUserGateway,
    auto_dao: DatabaseAutoGateway,
    auto_service: AutoService,
) -> None:
    """Обработчик ввода номера автомобиля при удалении."""
    number = message.text.upper()
    if not auto_service.validate_number(number):
        await message.answer(msg.AUTO_FORMAT_ERR_MSG, reply_markup=BACK_KB)
        return

    auto = await auto_service.get_auto_by_number(auto_dao, number)
    if auto is None:
        await message.answer(msg.AUTO_NOT_EXIST_MSG, reply_markup=BACK_KB)
        return

    user = await user_service.get_user_by_telegram_id(
        user_dao, tg_id=message.from_user.id
    )
    if user.id != auto.user_id:
        await message.answer(msg.AUTO_NOT_YOURS_MSG, reply_markup=BACK_KB)
        return

    keyboard = confirm_del_kb(cmd.AUTO_DEL_CONFIRM, cmd.AUTO_MENU)
    await message.answer(msg.AUTO_DEL_CONFIRM_MSG, reply_markup=keyboard)
    await state.update_data(auto_id=auto.id)
    await state.set_state(DeleteAuto.confirm)


@router.callback_query(DeleteAuto.confirm, F.data == cmd.AUTO_DEL_CONFIRM)
async def delete_auto_confirm(
    call: CallbackQuery,
    state: FSMContext,
    user_service: UserService,
    auto_service: AutoService,
    user_dao: DatabaseUserGateway,
    auto_dao: DatabaseAutoGateway,
) -> None:
    """Обработчик подтверждения удаления автомобиля из БД."""
    data = await state.get_data()
    auto_id = data.get("auto_id")
    if auto_id:
        await auto_service.delete_auto(auto_dao, auto_id)
    await get_autos_menu(
        call,
        state,
        user_service,
        user_dao,
        auto_service,
        auto_dao,
    )
