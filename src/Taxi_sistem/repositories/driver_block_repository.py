from database.database import get_connection
from models.driver_block import DriverBlock

_SELECT = """
    SELECT b.block_id,
           b.driver_id,
           b.admin_id,
           b.reason,
           b.blocked_at,
           d.full_name,
           u.login
    FROM driver_blocks b
    JOIN drivers d ON d.driver_id = b.driver_id
    JOIN users u ON u.user_id = b.admin_id
"""


def _map(row) -> DriverBlock:
    return DriverBlock(*row)


def create(driver_id: int, admin_id: int, reason: str) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        """
        INSERT INTO driver_blocks(driver_id, admin_id, reason, blocked_at)
        VALUES (?, ?, ?, datetime('now', 'localtime'))
        """,
        (driver_id, admin_id, reason),
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id


def get_by_id(block_id: int) -> DriverBlock | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(_SELECT + " WHERE b.block_id = ?", (block_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None


def get_all() -> list[DriverBlock]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(_SELECT + " ORDER BY b.blocked_at DESC")
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]


def get_by_driver(driver_id: int) -> list[DriverBlock]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        _SELECT + " WHERE b.driver_id = ? ORDER BY b.blocked_at DESC",
        (driver_id,),
    )
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]


def update_reason(block_id: int, reason: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE driver_blocks SET reason = ? WHERE block_id = ?",
        (reason, block_id),
    )
    conn.commit()
    conn.close()


def delete(block_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM driver_blocks WHERE block_id = ?", (block_id,))
    conn.commit()
    conn.close()
