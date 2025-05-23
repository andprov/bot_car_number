from aiogram.utils.markdown import hbold

from bot_car_number.application.dto.auto import AutoDTO
from bot_car_number.application.dto.user import UserDTO
from bot_car_number.presentation.misc.cmd import Button as btn

CANCEL_MSG = "Действие отменено."
STATE_CLEAR = "Нет активных команд для отмены."
EMPTY_MSG = "-пусто-"


# MAIN_MENU
MAIN_MSG = (
    "* Главное меню *\n"
    f"\n{hbold(btn.USER_MENU_TXT)}: управление данными пользователя."
    f"\n{hbold(btn.AUTO_MENU_TXT)}: управление данными автомобилей."
    f"\n{hbold(btn.BLOCK_AUTO_TXT)}: уведомить владельца о перекрытии."
    f"\n{hbold(btn.SEARCH_TXT)}: поиск владельца по номеру автомобиля."
)
MAIN_NO_DATA_MSG = (
    f"Для получения доступа, добавьте свои данные в меню - "
    f"{btn.USER_MENU_TXT}."
)
MAIN_NO_AUTO_MSG = f"Добавьте свой автомобиль в меню - '{btn.AUTO_MENU_TXT}'."


# USER_MENU
USER_CONTACT_MSG = (
    "Нажмите 'Отправить', что бы передать боту номер телефона или"
    " нажмите 'Отмена'."
)
USER_WRONG_MSG = "Вы отправили данные другого пользователя!"
USER_ADD_MSG = "Ваши контактные данные добавлены."
USER_DELETE_MSG = "Ваши данные удалены."
USER_NOT_FOUND_MSG = "Пользователь не найден."
USER_DEL_CONFIRM_MSG = (
    "После нажатия кнопки подтверждения, ваши контактные данные и данные "
    "всех ваших автомобилей будут удалены.\n"
    "Это действие невозможно отменить!"
)
USER_MAX_COUNT_REGISTRATIONS_MSG = (
    "Вы превысили количество регистраций и были заблокированы."
    "\nДля разблокировки обратитесь к администратору группы."
)


# AUTO_MENU
AUTO_MAX_COUNT_MSG = "Максимальное кол-во автомобилей уже добавлено."
AUTO_NONE_MSG = "Автомобилей не найдено."
AUTO_ENTER_NUMBER_MSG = (
    f"Введите номер автомобиля в формате {hbold('е001кх199')}. "
    "Буквы русского алфавита без учёта регистра и цифры."
)
AUTO_EXIST_MSG = (
    "Автомобиль с таким номером уже существует!" f"\n\n{AUTO_ENTER_NUMBER_MSG}"
)
AUTO_FORMAT_ERR_MSG = (
    f"Формат номера не соответствует шаблону!\n\n{AUTO_ENTER_NUMBER_MSG}"
)
AUTO_ADD_MODEL_MSG = (
    "Введите марку и модель автомобиля в произвольной форме не более "
    "50 символов.\n"
    "Например Моя ласточка или Lamborghini Diablo.\n"
    "Марка и модель будут доступны только вам, в вашем списке автомобилей."
)
AUTO_MODEL_ERR_MSG = (
    "Количество символов в названии автомобиля превышает допустимое!\n\n"
    f"{AUTO_ADD_MODEL_MSG}"
)
AUTO_CHECK_DATA_MSG = (
    "Проверьте введенные данные вашего автомобиля.\n"
    "Номер: {}\n"
    "Марка модель: {}\n"
)
AUTO_DEL_CONFIRM_MSG = (
    "После нажатия кнопки подтверждения, данные автомобиля будут удалены.\n"
    "Это действие невозможно отменить!"
)
AUTO_NOT_FOUND_MSG = (
    "Автомобиль с таким номером не найден!" f"\n\n{AUTO_ENTER_NUMBER_MSG}"
)
AUTO_NOT_YOURS_MSG = (
    "Невозможно удалить данный номер.\n" f"\n{AUTO_ENTER_NUMBER_MSG}"
)


# SEARCH
OWNER_DATA_MSG = "Контактные данные владельца."
SEARCH_ACCESS_DENIED_MSG = (
    "Вы превысили количество запросов, повторите попытку позднее."
)


# BLOCK_AUTO
OWNER_NOT_FOUND_MSG = "Владелец автомобиля не найден."
AUTO_CHECK_NUMBER_MSG = (
    "Проверьте номер автомобиля.\n"
    "Номер: {}\n\n"
    "После нажатия кнопки подтверждения, ваши контактные данные будут "
    "отправлены владельцу перекрытого автомобиля."
)
OWNER_HAS_BEEN_NOTIFIED = (
    "Владельцу отправлено сообщение с вашими контактными данными."
)
AUTO_IS_BLOCKED_MSG = "Ваш автомобиль перекрыли."


def start_msg(first_name: str) -> str:
    return (
        f"Привет {hbold(first_name)}! Я могу записать данные твоего "
        "автомобиля и поделиться контактными данными других "
        "автовладельцев.\n\n"
        f"Главное меню бота: /main"
    )


def autos_msg(autos: list[AutoDTO] | list[None]) -> str:
    text = EMPTY_MSG
    if autos:
        text = "\n".join(f"{auto.number} - {auto.model}" for auto in autos)
    return "* Мои автомобили *\n" "\n----------\n" + text


def user_msg(user: UserDTO) -> str:
    text = EMPTY_MSG
    if user:
        text = f"Имя: {user.first_name}\n" f"Телефон: {user.phone}"
    return "* Мои данные *\n" "\n----------\n" + text
