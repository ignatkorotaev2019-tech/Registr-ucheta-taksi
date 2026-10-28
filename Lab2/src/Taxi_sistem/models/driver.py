from dataclasses import dataclass

@dataclass
class Driver:
    driver_id: int
    user_id: int
    full_name: str
    age: int
    Data_drivers_expirience: int
    status_id: int

    # служебные поля: в таблице drivers их нет
    status_name: str | None = None
    login: str | None = None