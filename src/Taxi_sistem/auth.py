from services import auth_service
from ui.utils import input_int


def login():
    login_value = input("Логин: ")
    password_value = input("Пароль: ")

    try:
        user = auth_service.authenticate(login_value, password_value)
    except Exception as e:
        print(f"Ошибка: {e}")
        return None

    if not user:
        print("Неверный логин или пароль")
        return None
    return user


def register_driver():
    print("\n--- Регистрация водителя ---")
    login_value = input("Логин: ")
    password_value = input("Пароль: ")
    full_name = input("ФИО: ")
    age = input_int("Возраст: ")
    experience = input_int("Стаж за рулём (лет): ")

    if age is None or experience is None:
        return

    try:
        auth_service.register_driver(
            login_value, password_value, full_name, age, experience
        )
        print("Регистрация прошла успешно. Теперь можно войти в систему.")
    except Exception as e:
        print(f"Ошибка: {e}")
