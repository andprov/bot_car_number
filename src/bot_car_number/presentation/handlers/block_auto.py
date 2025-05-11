from aiogram import F, Router
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
from bot_car_number.presentation.keyboards.inline_keyboard import (
    back_kb,
    confirm_kb,
)
from bot_car_number.presentation.misc import msg
from bot_car_number.presentation.misc.cmd import Button as btn
from bot_car_number.presentation.misc.cmd import Command as cmd
from bot_car_number.presentation.states import BlockAutoState
from bot_car_number.value_objects.auto_number import AutoNumberValidationError

router = Router()

BACK_KB = back_kb(cmd.MAIN)


@router.callback_query(F.data == cmd.BLOCK_AUTO)
async def block_auto(
    call: CallbackQuery,
    state: FSMContext,
    user: UserDTO | None,
    check_search_access: FromDishka[CheckSearchAccess],
) -> None:
    if user is None:
        await call.answer(text=msg.MAIN_NO_DATA_MSG, show_alert=True)
        return

    if not await check_search_access(tg_id=user.tg_id):
        await call.answer(text=msg.SEARCH_ACCESS_DENIED_MSG, show_alert=True)
        return

    await call.message.edit_text(
        text=msg.AUTO_ENTER_NUMBER_MSG,
        reply_markup=BACK_KB,
    )

    await state.set_state(state=BlockAutoState.enter_number)


@router.message(BlockAutoState.enter_number, F.text)
async def enter_number(
    message: Message,
    state: FSMContext,
    user: UserDTO,
    check_search_access: FromDishka[CheckSearchAccess],
    get_auto_owner: FromDishka[GetAutoOwner],
    add_search_attempt: FromDishka[AddSearchAttempt],
) -> None:
    if not await check_search_access(tg_id=user.tg_id):
        await message.answer(
            text=msg.SEARCH_ACCESS_DENIED_MSG,
            show_alert=True,
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
            text=msg.OWNER_NOT_FOUND_MSG,
            reply_markup=BACK_KB,
        )
    else:
        await message.answer(
            text=msg.AUTO_CHECK_NUMBER_MSG.format(message.text.upper()),
            reply_markup=confirm_kb(
                btn.BLOCK_AUTO_CONFIRM_TXT,
                cmd.BLOCK_AUTO_CONFIRM,
                cmd.MAIN,
            ),
        )

        await state.update_data(owner_tg_id=owner.tg_id)
        await state.set_state(state=BlockAutoState.confirm)

    search_data = SearchAttemptDTO(tg_id=user.tg_id, number=message.text)
    await add_search_attempt(search_data=search_data)


@router.callback_query(
    BlockAutoState.confirm,
    F.data == cmd.BLOCK_AUTO_CONFIRM,
)
async def block_auto_confirm(
    call: CallbackQuery,
    state: FSMContext,
    user: UserDTO,
) -> None:
    data = await state.get_data()
    owner_tg_id = data.get("owner_tg_id")

    await call.bot.send_message(
        chat_id=owner_tg_id,
        text=msg.AUTO_IS_BLOCKED_MSG,
    )
    await call.bot.send_contact(
        chat_id=owner_tg_id,
        phone_number=user.phone,
        first_name=user.first_name,
    )

    await call.message.edit_text(text=msg.OWNER_HAS_BEEN_NOTIFIED)

    await state.clear()
