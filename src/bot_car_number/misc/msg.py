from aiogram.utils.markdown import hbold

from bot_car_number.db.models import Auto, User
from bot_car_number.misc.cmd import Button as btn

CANCEL_MSG = "Действие отменено."
STATE_CLEAR = "Нет активных команд для отмены."
EMPTY_MSG = "-пусто-"


# MAIN_MENU
MAIN_MSG = (
    "* Главное меню *\n"
    f"\n'{btn.USER_MENU_TXT}' - управление данными пользователя.\n"
    f"\n'{btn.AUTO_MENU_TXT}' - управление данными автомобилей."
)
NO_DATA_MSG = (
    f"Для получения доступа, добавьте свои данные в меню - "
    f"'{btn.USER_MENU_TXT}'."
)
NO_AUTO_MSG = f"Добавьте свой автомобиль в меню - '{btn.AUTO_MENU_TXT}'."


# USER_MENU
USER_CONTACT_MSG = "Нажмите Отправить или Отмена."
USER_WRONG_MSG = "Вы отправили данные другого пользователя!"
USER_ADD_MSG = "Ваши контактные данные добавлены."
USER_DELETE_MSG = "Ваши данные удалены."
USER_EXIST_MSG = "Ваши данные уже были добавлены ранее!"
USER_NOT_EXIST_MSG = "Пользователь не найден."
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
AUTO_MAX_COUNT_MSG = "Vаксимальное кол-во автомобилей уже добавлено."
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
AUTO_MODEL_LONG_MSG = (
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
AUTO_NOT_EXIST_MSG = (
    "Автомобиля с таким номером не существует!" f"\n\n{AUTO_ENTER_NUMBER_MSG}"
)
AUTO_NOT_YOURS_MSG = (
    "Данный номер автомобиля вам не принадлежит и вы не можете его удалить!\n"
    f"\n{AUTO_ENTER_NUMBER_MSG}"
)


# SEARCH
OWNER_YOUR_MSG = "Этот автомобильный номер принадлежит вам."
OWNER_MSG = "Телефон владельца:\n{}"
SEARCH_ACCESS_DENIED = (
    "Вы превысили количество запросов, повторите попытку позднее."
)


def start_msg(first_name: str) -> str:
    """Вернуть приветственное сообщение."""
    return (
        f"Привет {hbold(first_name)}! Я могу записать данные твоего "
        "автомобиля и поделиться с тобой контактными данными других "
        "автовладельцев.\n\n"
        f"Главное меню бота: /main"
    )


def autos_msg(autos: list[Auto] | None) -> str:
    """Вернуть сообщение Мои автомобили."""
    text = EMPTY_MSG
    if autos:
        text = "\n".join(map(str, autos))
    return (
        "* Мои автомобили *\n"
        f"\n{btn.ADD_TXT} данные автомобиля.\n"
        f"\n{btn.DELETE_TXT} данные автомобиля.\n"
        "----------\n" + text
    )


def user_msg(user: User | None = None) -> str:
    """Вернуть сообщение Мои данные."""
    msg = f"\n{btn.ADD_TXT} свои контактные данные."
    if user:
        msg = f"\n{btn.DELETE_TXT} свои контактные данные "
    return f"* Мои данные *\n{msg}"
