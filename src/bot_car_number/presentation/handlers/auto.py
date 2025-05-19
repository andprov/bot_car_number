from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from dishka.integrations.aiogram import FromDishka

from bot_car_number.application.dto.auto import AutoDTO
from bot_car_number.application.dto.user import UserDTO
from bot_car_number.application.exceptions import (
    AutoAlreadyExistsError,
    AutoNotFoundError,
    AutoOwnerError,
)
from bot_car_number.application.use_case.add_auto import AddAuto
from bot_car_number.application.use_case.add_auto_model import AddAutoModel
from bot_car_number.application.use_case.add_auto_number import AddAutoNumber
from bot_car_number.application.use_case.check_add_auto import (
    CheckUserAutosCount,
)
from bot_car_number.application.use_case.delete_auto import DeleteAuto
from bot_car_number.application.use_case.get_auto_for_delete import (
    GetAutoForDelete,
)
from bot_car_number.application.use_case.get_autos_by_user_id import (
    GetAutosByUserId,
)
from bot_car_number.presentation.keyboards.inline_keyboard import (
    add_del_back_kb,
    back_kb,
    confirm_kb,
)
from bot_car_number.presentation.misc import msg
from bot_car_number.presentation.misc.cmd import Button as btn
from bot_car_number.presentation.misc.cmd import Command as cmd
from bot_car_number.presentation.states import AddAutoState, RemoveAutoState
from bot_car_number.value_objects.auto_model import AutoModelValidationError
from bot_car_number.value_objects.auto_number import AutoNumberValidationError

router = Router()

AUTO_KB = add_del_back_kb(cmd.AUTO_ADD, cmd.AUTO_DEL, cmd.MAIN)
BACK_KB = back_kb(cmd.AUTO_MENU)


async def get_user_autos_menu(
    call: CallbackQuery,
    user_id: int,
    get_autos_by_user_id: GetAutosByUserId,
) -> None:
    user_autos = await get_autos_by_user_id(user_id=user_id)
    await call.message.edit_text(
        text=msg.autos_msg(autos=user_autos),
        reply_markup=AUTO_KB,
    )


@router.callback_query(F.data == cmd.AUTO_MENU)
async def auto_menu(
    call: CallbackQuery,
    state: FSMContext,
    user: UserDTO | None,
    get_autos_by_user_id: FromDishka[GetAutosByUserId],
) -> None:
    if user is None:
        await call.answer(text=msg.MAIN_NO_DATA_MSG, show_alert=True)
        return

    await get_user_autos_menu(
        call=call,
        user_id=user.id,
        get_autos_by_user_id=get_autos_by_user_id,
    )

    await state.clear()


@router.callback_query(StateFilter(None), F.data == cmd.AUTO_ADD)
async def crete_auto(
    call: CallbackQuery,
    state: FSMContext,
    user: UserDTO,
    check_user_autos_count: FromDishka[CheckUserAutosCount],
) -> None:
    if not await check_user_autos_count(user_id=user.id):
        await call.answer(text=msg.AUTO_MAX_COUNT_MSG, show_alert=True)
        return

    await call.message.edit_text(
        text=msg.AUTO_ENTER_NUMBER_MSG,
        reply_markup=BACK_KB,
    )

    await state.set_state(state=AddAutoState.enter_number)


@router.message(AddAutoState.enter_number, F.text)
async def enter_number(
    message: Message,
    state: FSMContext,
    add_auto_number: FromDishka[AddAutoNumber],
) -> None:
    try:
        number = await add_auto_number(number=message.text)
    except AutoNumberValidationError:
        await message.answer(
            text=msg.AUTO_FORMAT_ERR_MSG,
            reply_markup=BACK_KB,
        )
    except AutoAlreadyExistsError:
        await message.answer(text=msg.AUTO_EXIST_MSG, reply_markup=BACK_KB)
    else:
        await message.answer(text=msg.AUTO_ADD_MODEL_MSG, reply_markup=BACK_KB)

        await state.update_data(number=number)
        await state.set_state(state=AddAutoState.enter_model)


@router.message(AddAutoState.enter_model, F.text)
async def enter_model(
    message: Message,
    state: FSMContext,
    add_auto_model: FromDishka[AddAutoModel],
) -> None:
    try:
        model = await add_auto_model(model=message.text)
    except AutoModelValidationError:
        await message.answer(text=msg.AUTO_MODEL_ERR_MSG, reply_markup=BACK_KB)
    else:
        data = await state.get_data()
        await message.answer(
            text=msg.AUTO_CHECK_DATA_MSG.format(data["number"], model),
            reply_markup=confirm_kb(
                btn.SAVE_TXT,
                cmd.AUTO_SAVE,
                cmd.AUTO_MENU,
            ),
        )

        await state.update_data(model=model)
        await state.set_state(state=AddAutoState.confirm)


@router.callback_query(AddAutoState.confirm, F.data == cmd.AUTO_SAVE)
async def create_auto_confirm(
    call: CallbackQuery,
    state: FSMContext,
    user: UserDTO,
    add_auto: FromDishka[AddAuto],
    get_autos_by_user_id: FromDishka[GetAutosByUserId],
) -> None:
    data = await state.get_data()
    auto = AutoDTO(
        id=None,
        number=data["number"],
        model=data["model"],
        user_id=user.id,
    )
    await add_auto(auto=auto)

    await get_user_autos_menu(
        call=call,
        user_id=user.id,
        get_autos_by_user_id=get_autos_by_user_id,
    )

    await state.clear()


@router.callback_query(StateFilter(None), F.data == cmd.AUTO_DEL)
async def remove_auto(
    call: CallbackQuery,
    state: FSMContext,
    user: UserDTO,
    get_autos_by_user_id: FromDishka[GetAutosByUserId],
) -> None:
    autos = await get_autos_by_user_id(user_id=user.id)
    if len(autos) == 0:
        await call.answer(text=msg.AUTO_NONE_MSG, show_alert=True)
        return
    await call.message.edit_text(
        text=msg.AUTO_ENTER_NUMBER_MSG,
        reply_markup=BACK_KB,
    )

    await state.set_state(state=RemoveAutoState.enter_number)


@router.message(RemoveAutoState.enter_number, F.text)
async def enter_number_for_delete(
    message: Message,
    state: FSMContext,
    user: UserDTO,
    get_auto_for_delete: FromDishka[GetAutoForDelete],
) -> None:
    try:
        auto = await get_auto_for_delete(number=message.text, user=user)
    except AutoNumberValidationError:
        await message.answer(
            text=msg.AUTO_FORMAT_ERR_MSG,
            reply_markup=BACK_KB,
        )
    except AutoNotFoundError:
        await message.answer(
            text=msg.AUTO_NOT_FOUND_MSG,
            reply_markup=BACK_KB,
        )
    except AutoOwnerError:
        await message.answer(
            text=msg.AUTO_NOT_YOURS_MSG,
            reply_markup=BACK_KB,
        )
    else:
        keyboard = confirm_kb(
            btn.DEL_CONFIRM_TXT,
            cmd.AUTO_DEL_CONFIRM,
            cmd.AUTO_MENU,
        )
        await message.answer(
            text=msg.AUTO_DEL_CONFIRM_MSG,
            reply_markup=keyboard,
        )

        await state.update_data(auto_id=auto.id)
        await state.set_state(state=RemoveAutoState.confirm)


@router.callback_query(RemoveAutoState.confirm, F.data == cmd.AUTO_DEL_CONFIRM)
async def remove_auto_confirm(
    call: CallbackQuery,
    state: FSMContext,
    user: UserDTO,
    delete_auto: FromDishka[DeleteAuto],
    get_autos_by_user_id: FromDishka[GetAutosByUserId],
) -> None:
    data = await state.get_data()
    auto_id = data.get("auto_id")
    if auto_id:
        await delete_auto(id=auto_id)

    await get_user_autos_menu(
        call=call,
        user_id=user.id,
        get_autos_by_user_id=get_autos_by_user_id,
    )

    await state.clear()
