from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from dishka.integrations.aiogram import FromDishka, inject

from bot_car_number.application.dto.auto import AutoDTO
from bot_car_number.application.use_case.add_auto_model import AddAutoModel
from bot_car_number.application.use_case.add_auto_number import AddAutoNumber
from bot_car_number.application.use_case.check_add_auto import (
    CheckUserAutosCount,
)
from bot_car_number.application.use_case.create_auto import CreateAuto
from bot_car_number.application.use_case.delete_auto import DeleteAuto
from bot_car_number.application.use_case.get_auto_for_delete import (
    GetAutoForDelete,
)
from bot_car_number.application.use_case.get_autos_by_user_id import (
    GetAutosByUserId,
)
from bot_car_number.application.use_case.get_user_by_telegram_id import (
    GetUserByTelegramId,
)
from bot_car_number.presentation.keyboards.inline_keyboard import (
    add_del_back_kb,
    back_kb,
    confirm_del_kb,
    save_kb,
)
from bot_car_number.presentation.misc import msg
from bot_car_number.presentation.misc.cmd import Command as cmd
from bot_car_number.presentation.states import AddAuto, RemoveAuto

router = Router()

AUTO_KB = add_del_back_kb(cmd.AUTO_ADD, cmd.AUTO_DEL, cmd.MAIN)
BACK_KB = back_kb(cmd.AUTO_MENU)


@router.callback_query(F.data == cmd.AUTO_MENU)
@inject
async def auto_menu(
    call: CallbackQuery,
    state: FSMContext,
    get_user_by_telegram_id: FromDishka[GetUserByTelegramId],
    get_autos_by_user_id: FromDishka[GetAutosByUserId],
) -> None:
    """Вызов меню управления автомобилями пользователя."""
    user = await get_user_by_telegram_id(tg_id=call.from_user.id)
    if user is None:
        await call.answer(text=msg.NO_DATA_MSG, show_alert=True)
        return

    user_autos = await get_autos_by_user_id(user_id=user.id)
    await call.message.edit_text(
        text=msg.autos_msg(autos=user_autos),
        reply_markup=AUTO_KB,
    )

    await state.clear()


@router.callback_query(StateFilter(None), F.data == cmd.AUTO_ADD)
@inject
async def add_auto(
    call: CallbackQuery,
    state: FSMContext,
    check_user_autos_count: FromDishka[CheckUserAutosCount],
) -> None:
    """Переход к добавлению автомобиля."""
    user, err_msg = await check_user_autos_count(tg_id=call.from_user.id)
    if err_msg:
        await call.answer(text=err_msg, show_alert=True)
        return

    await call.message.edit_text(
        text=msg.AUTO_ENTER_NUMBER_MSG,
        reply_markup=BACK_KB,
    )

    await state.update_data(user_id=user.id)
    await state.set_state(state=AddAuto.enter_number)


@router.message(AddAuto.enter_number)
@inject
async def add_number(
    message: Message,
    state: FSMContext,
    add_auto_number: FromDishka[AddAutoNumber],
) -> None:
    """Ввод номера автомобиля при добавлении."""
    number, err_msg = await add_auto_number(number=message.text.upper())
    if err_msg:
        await message.answer(text=err_msg, reply_markup=BACK_KB)
        return

    await message.answer(text=msg.AUTO_ADD_MODEL_MSG, reply_markup=BACK_KB)

    await state.update_data(number=number)
    await state.set_state(state=AddAuto.enter_model)


@router.message(AddAuto.enter_model)
@inject
async def add_model(
    message: Message,
    state: FSMContext,
    add_auto_model: FromDishka[AddAutoModel],
) -> None:
    """Ввод марки автомобиля."""
    model, err_msg = await add_auto_model(model=message.text)
    if err_msg:
        await message.answer(text=err_msg, reply_markup=BACK_KB)
        return

    data = await state.get_data()
    await message.answer(
        text=msg.AUTO_CHECK_DATA_MSG.format(data["number"], model),
        reply_markup=save_kb(cmd.AUTO_MENU),
    )

    await state.update_data(model=model)
    await state.set_state(state=AddAuto.confirm)


@router.callback_query(AddAuto.confirm, F.data == cmd.AUTO_SAVE)
@inject
async def add_auto_confirm(
    call: CallbackQuery,
    state: FSMContext,
    get_autos_by_user_id: FromDishka[GetAutosByUserId],
    create_auto: FromDishka[CreateAuto],
) -> None:
    """Добавление автомобиля."""
    data = await state.get_data()
    auto = AutoDTO(
        id=None,
        number=data["number"],
        model=data["model"],
        user_id=data["user_id"],
    )
    await create_auto(auto=auto)

    user_autos = await get_autos_by_user_id(user_id=data["user_id"])
    await call.message.edit_text(
        text=msg.autos_msg(autos=user_autos),
        reply_markup=AUTO_KB,
    )

    await state.clear()


@router.callback_query(StateFilter(None), F.data == cmd.AUTO_DEL)
@inject
async def delete_auto(
    call: CallbackQuery,
    state: FSMContext,
    get_user_by_telegram_id: FromDishka[GetUserByTelegramId],
    get_autos_by_user_id: FromDishka[GetAutosByUserId],
) -> None:
    """Нажатие кнопки удаления автомобиля."""
    user = await get_user_by_telegram_id(tg_id=call.from_user.id)
    if user:
        autos = await get_autos_by_user_id(user_id=user.id)
        if not autos:
            await call.answer(text=msg.AUTO_NONE_MSG, show_alert=True)
            return
        await call.message.edit_text(
            text=msg.AUTO_ENTER_NUMBER_MSG,
            reply_markup=BACK_KB,
        )

        await state.update_data(user_id=user.id)
        await state.set_state(state=RemoveAuto.enter_number)


@router.message(RemoveAuto.enter_number)
@inject
async def enter_number_for_delete(
    message: Message,
    state: FSMContext,
    get_auto_for_delete: FromDishka[GetAutoForDelete],
) -> None:
    """Ввод номера автомобиля при удалении."""
    auto, err_msg = await get_auto_for_delete(
        number=message.text.upper(),
        tg_id=message.from_user.id,
    )
    if err_msg:
        await message.answer(text=err_msg, reply_markup=BACK_KB)
        return

    keyboard = confirm_del_kb(cmd.AUTO_DEL_CONFIRM, cmd.AUTO_MENU)
    await message.answer(text=msg.AUTO_DEL_CONFIRM_MSG, reply_markup=keyboard)

    await state.update_data(auto_id=auto.id)
    await state.set_state(state=RemoveAuto.confirm)


@router.callback_query(RemoveAuto.confirm, F.data == cmd.AUTO_DEL_CONFIRM)
@inject
async def delete_auto_confirm(
    call: CallbackQuery,
    state: FSMContext,
    get_autos_by_user_id: FromDishka[GetAutosByUserId],
    delete_auto: FromDishka[DeleteAuto],
) -> None:
    """Подтверждение удаления автомобиля."""
    data = await state.get_data()
    auto_id = data.get("auto_id")
    if auto_id:
        await delete_auto(id=auto_id)

    user_autos = await get_autos_by_user_id(user_id=data["user_id"])
    await call.message.edit_text(
        text=msg.autos_msg(autos=user_autos),
        reply_markup=AUTO_KB,
    )

    await state.clear()
