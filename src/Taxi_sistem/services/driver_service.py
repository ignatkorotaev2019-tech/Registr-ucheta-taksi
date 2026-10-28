from config import ADMIN_ROLE_ID, STATUS_BLOCKED
from models.driver import Driver
from models.driver_block import DriverBlock
from repositories import (
    driver_block_repository,
    driver_repository,
    user_repository,
)


def get_driver_by_user(user_id: int) -> Driver:
    driver = driver_repository.get_by_user_id(user_id)
    if not driver:
        raise Exception("Профиль водителя не найден")
    return driver


def get_all_drivers() -> list[Driver]:
    return driver_repository.get_all()


def get_driver(driver_id: int) -> Driver:
    driver = driver_repository.get_by_id(driver_id)
    if not driver:
        raise Exception("Водитель не найден")
    return driver


def get_driver_blocks(driver_id: int) -> list[DriverBlock]:
    get_driver(driver_id)
    return driver_block_repository.get_by_driver(driver_id)


def block_driver(admin_id: int, driver_id: int, reason: str):
    """Блокировка (увольнение) водителя администратором."""
    admin = user_repository.get_by_id(admin_id)
    if not admin or admin.role_id != ADMIN_ROLE_ID:
        raise Exception("Блокировать водителей может только администратор")

    driver = get_driver(driver_id)

    if driver.status_id == STATUS_BLOCKED:
        raise Exception("Водитель уже заблокирован")

    if not reason.strip():
        raise Exception("Укажите причину блокировки")

    driver_block_repository.create(driver_id, admin_id, reason.strip())
    driver_repository.set_status(driver_id, STATUS_BLOCKED)
