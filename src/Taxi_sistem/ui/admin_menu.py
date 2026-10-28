from services import driver_service
from ui.utils import input_int, print_driver


def admin_menu(user):
    while True:
        print(f"\n===== Администратор ({user.login}) =====")
        print("1. Посмотреть список водителей")
        print("2. Открыть профиль водителя")
        print("0. Выход")

        choice = input("Выберите действие: ").strip()

        if choice == "1":
            show_drivers()
        elif choice == "2":
            driver_id = input_int("Введите ID водителя: ")
            if driver_id is not None:
                driver_profile_menu(user, driver_id)
        elif choice == "0":
            break
        else:
            print("Неверный пункт меню")


def show_drivers():
    drivers = driver_service.get_all_drivers()
    if not drivers:
        print("Водителей пока нет")
        return

    print("\n--- Список водителей ---")
    print(f"{'ID':<4}{'ФИО':<28}{'Возраст':<9}{'Стаж':<6}Статус")
    for d in drivers:
        print(
            f"{d.driver_id:<4}{d.full_name:<28}{d.age:<9}"
            f"{d.Data_drivers_expirience:<6}{d.status_name}"
        )


def driver_profile_menu(admin, driver_id: int):
    while True:
        try:
            driver = driver_service.get_driver(driver_id)
        except Exception as e:
            print(f"Ошибка: {e}")
            return

        print("\n--- Информация о водителе ---")
        print_driver(driver)

        print("\n1. Заблокировать водителя (уволить)")
        print("2. История блокировок")
        print("0. Назад")

        choice = input("Выберите действие: ").strip()

        if choice == "1":
            reason = input("Причина блокировки: ")
            try:
                driver_service.block_driver(admin.user_id, driver_id, reason)
                print("Водитель заблокирован")
            except Exception as e:
                print(f"Ошибка: {e}")

        elif choice == "2":
            blocks = driver_service.get_driver_blocks(driver_id)
            if not blocks:
                print("Блокировок не было")
            for b in blocks:
                print(f"  [{b.blocked_at}] админ {b.admin_login}: {b.reason}")

        elif choice == "0":
            break
        else:
            print("Неверный пункт меню")
