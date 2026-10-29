import auth
from config import ADMIN_ROLE_ID, DRIVER_ROLE_ID
from ui.admin_menu import admin_menu
from ui.driver_menu import driver_menu


def main():
    while True:
        print("\n===== Регистрация учёта такси =====")
        print("1. Вход в систему")
        print("2. Регистрация водителя")
        print("0. Выход")

        choice = input("Выберите действие: ").strip()

        if choice == "1":
            user = auth.login()
            if not user:
                continue
            if user.role_id == ADMIN_ROLE_ID:
                admin_menu(user)
            elif user.role_id == DRIVER_ROLE_ID:
                driver_menu(user)

        elif choice == "2":
            auth.register_driver()

        elif choice == "0":
            print("До свидания!")
            break
        else:
            print("Неверный пункт меню")


if __name__ == "__main__":
    main()

"""admin01 - логин и пароль для администратора"""