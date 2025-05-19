from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from dishka.integrations.aiogram import FromDishka

from bot_car_number.application.dto.search import SearchAttemptDTO
from bot_car_number.application.dto.user import UserDTO
from bot_car_number.application.exceptions import (
    AutoNotFoundError,
    UserNotFoundError,
)
from bot_car_number.application.use_case.add_search_attempt import (
    AddSearchAttempt,
)
from bot_car_number.application.use_case.check_search_access import (
    CheckSearchAccess,
)
from bot_car_number.application.use_case.get_auto_owner import GetAutoOwner
from bot_car_number.application.use_case.get_autos_by_user_id import (
    GetAutosByUserId,
)
from bot_car_number.presentation.keyboards.inline_keyboard import back_kb
from bot_car_number.presentation.misc import msg
from bot_car_number.presentation.misc.cmd import Command as cmd
from bot_car_number.presentation.states import SearchAutoState
from bot_car_number.value_objects.auto_number import AutoNumberValidationError

router = Router()

BACK_KB = back_kb(cmd.MAIN)


@router.callback_query(StateFilter(None), F.data == cmd.SEARCH)
async def search(
    call: CallbackQuery,
    state: FSMContext,
    user: UserDTO | None,
    get_autos_by_user_id: FromDishka[GetAutosByUserId],
    check_search_access: FromDishka[CheckSearchAccess],
) -> None:
    if user is None:
        await call.answer(text=msg.MAIN_NO_DATA_MSG, show_alert=True)
        return

    if not await check_search_access(tg_id=user.tg_id):
        await call.answer(text=msg.SEARCH_ACCESS_DENIED_MSG, show_alert=True)
        return

    if not await get_autos_by_user_id(user_id=user.id):
        await call.answer(text=msg.MAIN_NO_AUTO_MSG, show_alert=True)
        return

    await call.message.edit_text(
        text=msg.AUTO_ENTER_NUMBER_MSG,
        reply_markup=BACK_KB,
    )

    await state.set_state(state=SearchAutoState.enter_number)


@router.message(SearchAutoState.enter_number, F.text)
async def enter_number(
    message: Message,
    state: FSMContext,
    user: UserDTO | None,
    check_search_access: FromDishka[CheckSearchAccess],
    get_auto_owner: FromDishka[GetAutoOwner],
    add_search_attempt: FromDishka[AddSearchAttempt],
) -> None:
    if not await check_search_access(tg_id=user.tg_id):
        await message.answer(
            text=msg.SEARCH_ACCESS_DENIED_MSG, show_alert=True
        )
        await state.clear()
        return

    try:
        owner = await get_auto_owner(number=message.text)
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
    except UserNotFoundError:
        await message.answer(
            text=msg.USER_NOT_FOUND_MSG,
            reply_markup=BACK_KB,
        )
    else:
        await message.answer(text=msg.OWNER_DATA_MSG)
        await message.answer_contact(
            phone_number=owner.phone,
            first_name=owner.first_name,
        )

        await state.clear()

    search_data = SearchAttemptDTO(tg_id=user.tg_id, number=message.text)
    await add_search_attempt(search_data=search_data)
