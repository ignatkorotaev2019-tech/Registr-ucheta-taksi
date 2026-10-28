def input_int(prompt: str) -> int | None:
    value = input(prompt).strip()
    try:
        return int(value)
    except ValueError:
        print("Ошибка: нужно ввести целое число")
        return None


def years(n: int) -> str:
    if 11 <= n % 100 <= 14:
        word = "лет"
    elif n % 10 == 1:
        word = "год"
    elif 2 <= n % 10 <= 4:
        word = "года"
    else:
        word = "лет"
    return f"{n} {word}"


def print_driver(driver):
    print(f"  ID водителя : {driver.driver_id}")
    print(f"  Логин       : {driver.login}")
    print(f"  ФИО         : {driver.full_name}")
    print(f"  Возраст     : {driver.age}")
    print(f"  Стаж за рулём: {years(driver.Data_drivers_expirience)}")
    print(f"  Статус      : {driver.status_name}")
