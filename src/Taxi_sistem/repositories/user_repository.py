from database.database import get_connection
from models.user import User

_SELECT = """
    SELECT u.user_id,
           u.login,
           u.password_hash,
           u.role_id,
           r.name
    FROM users u
    JOIN roles r ON r.role_id = u.role_id
"""


def _map(row) -> User:
    return User(*row)


def create(login: str, password_hash: str, role_id: int) -> int:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO users(login, password_hash, role_id) VALUES (?, ?, ?)",
        (login, password_hash, role_id),
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id


def get_by_id(user_id: int) -> User | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(_SELECT + " WHERE u.user_id = ?", (user_id,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None


def get_by_login(login: str) -> User | None:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(_SELECT + " WHERE u.login = ?", (login,))
    row = cur.fetchone()
    conn.close()
    return _map(row) if row else None


def get_all() -> list[User]:
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(_SELECT + " ORDER BY u.user_id")
    rows = cur.fetchall()
    conn.close()
    return [_map(r) for r in rows]


def update(user_id: int, login: str, role_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE users SET login = ?, role_id = ? WHERE user_id = ?",
        (login, role_id, user_id),
    )
    conn.commit()
    conn.close()


def update_password(user_id: int, password_hash: str):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(
        "UPDATE users SET password_hash = ? WHERE user_id = ?",
        (password_hash, user_id),
    )
    conn.commit()
    conn.close()


def delete(user_id: int):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM users WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()
