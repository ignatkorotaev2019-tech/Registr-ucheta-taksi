import hashlib

from config import DRIVER_ROLE_ID, STATUS_ACTIVE, STATUS_BLOCKED
from models.user import User
from repositories import driver_repository, user_repository


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def authenticate(login: str, password: str) -> User | None:
    """Возвращает пользователя или None, если логин/пароль неверны.
    Заблокированному водителю вход запрещён (исключение)."""
    user = user_repository.get_by_login(login.strip())

    if not user or user.password_hash != hash_password(password):
        return None

    if user.role_id == DRIVER_ROLE_ID:
        driver = driver_repository.get_by_user_id(user.user_id)
        if driver and driver.status_id == STATUS_BLOCKED:
            raise Exception("Ваш аккаунт заблокирован администратором")

    return user


def register_driver(
    login: str,
    password: str,
    full_name: str,
    age: int,
    experience_years: int,
):
    login = login.strip()
    full_name = full_name.strip()

    if not login:
        raise Exception("Логин не может быть пустым")
    if len(password) < 4:
        raise Exception("Пароль должен содержать не менее 4 символов")
    if not full_name:
        raise Exception("ФИО не может быть пустым")
    if age < 18:
        raise Exception("Водитель должен быть старше 18 лет")
    if experience_years < 0:
        raise Exception("Стаж не может быть отрицательным")
    if experience_years > age - 18:
        raise Exception("Стаж не может превышать (возраст - 18) лет")

    if user_repository.get_by_login(login):
        raise Exception("Пользователь с таким логином уже существует")

    user_id = user_repository.create(
        login, hash_password(password), DRIVER_ROLE_ID
    )

    try:
        driver_repository.create(
            user_id, full_name, age, experience_years, STATUS_ACTIVE
        )
    except Exception:
        # откатываем созданного пользователя, чтобы не оставлять "пустой" аккаунт
        user_repository.delete(user_id)
        raise Exception("Не удалось сохранить данные водителя")
