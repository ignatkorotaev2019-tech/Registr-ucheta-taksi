from database.database import get_connection
from models.driver_status import DriverStatus


def _map(row):
    # превращаем кортеж из базы в объект DriverStatus
    return DriverStatus(*row)


def create(name: str):
    # Добавление нового статуса
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO driver_statuses(name) VALUES (?)", (name,))
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id


def get_by_id(status_id: int):
    # Получение одного статуса по номеру
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "SELECT status_id, name FROM driver_statuses WHERE status_id = ?",
        (status_id,),
    )
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None


def get_all():
    # Получение всех статусов
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT status_id, name FROM driver_statuses ORDER BY status_id")
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]


def update(status_id: int, name: str):
    # Изменение названия статуса
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE driver_statuses SET name = ? WHERE status_id = ?",
        (name, status_id),
    )
    conn.commit()
    conn.close()


def delete(status_id: int):
    # Удаление статуса
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM driver_statuses WHERE status_id = ?", (status_id,))
    conn.commit()
    conn.close()