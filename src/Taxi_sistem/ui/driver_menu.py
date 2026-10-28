from services import driver_service
from ui.utils import print_driver


def driver_menu(user):
    while True:
        print(f"\n===== Водитель такси ({user.login}) =====")
        print("1. Открыть профиль водителя")
        print("0. Выход")

        choice = input("Выберите действие: ").strip()

        if choice == "1":
            try:
                driver = driver_service.get_driver_by_user(user.user_id)
                print("\n--- Информация о водителе ---")
                print_driver(driver)
            except Exception as e:
                print(f"Ошибка: {e}")

        elif choice == "0":
            break
        else:
            print("Неверный пункт меню")
