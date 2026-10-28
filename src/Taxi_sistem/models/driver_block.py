from dataclasses import dataclass

@dataclass
class DriverBlock:
    block_id: int
    driver_id: int
    admin_id: int
    reason: str
    blocked_at: str

    # служебные поля: в таблице driver_blocks их нет
    driver_name: str | None = None
    admin_login: str | None = None