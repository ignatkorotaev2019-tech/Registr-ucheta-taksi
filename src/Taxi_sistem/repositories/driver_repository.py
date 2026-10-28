from database.database import get_connection
from models.driver import Driver

_SELECT = """
    SELECT d.driver_id,
           d.user_id,
           d.full_name,
           d.age,
           d.Data_drivers_expirience,
           d.status_id,
           s.name,
           u.login
    FROM drivers d
    JOIN driver_statuses s ON s.status_id = d.status_id
    JOIN users u ON u.user_id = d.user_id
"""


def _map(row) -> Driver:
    return Driver(*row)


def create(
    user_id: int,
    full_name: str,
    age: int,
    Data_drivers_expirience: int,
    status_id: int,
) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO drivers(user_id, full_name, age, Data_drivers_expirience, status_id)
        VALUES (?, ?, ?, ?, ?)
        """,
        (user_id, full_name, age, Data_drivers_expirience, status_id),
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id


def get_by_id(driver_id: int) -> Driver | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(_SELECT + " WHERE d.driver_id = ?", (driver_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None


def get_by_user_id(user_id: int) -> Driver | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(_SELECT + " WHERE d.user_id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None


def get_all() -> list[Driver]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(_SELECT + " ORDER BY d.driver_id")
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]


def update(
    driver_id: int, full_name: str, age: int, Data_drivers_expirience: int
):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE drivers
        SET full_name = ?,
            age = ?,
            Data_drivers_expirience = ?
        WHERE driver_id = ?
        """,
        (full_name, age, Data_drivers_expirience, driver_id),
    )
    conn.commit()
    conn.close()


def set_status(driver_id: int, status_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE drivers SET status_id = ? WHERE driver_id = ?",
        (status_id, driver_id),
    )
    conn.commit()
    conn.close()


def delete(driver_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM drivers WHERE driver_id = ?", (driver_id,))
    conn.commit()
    conn.close()
