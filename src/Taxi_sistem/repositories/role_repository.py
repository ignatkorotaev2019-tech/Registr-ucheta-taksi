from database.database import get_connection
from models.role import Role

def _map(row):
    # превращаем кортеж из базы в объект Role
    return Role(*row)

def create(name: str):
    # Добавление новой роли
    conn = get_connection()
    cur = conn.cursor()
    # вставить в таблицу roles новую запись со значением name
    cur.execute("INSERT INTO roles(name) VALUES (?)", (name,))
    conn.commit()          # сохраняем изменения в базе
    new_id = cur.lastrowid  # номер только что созданной записи
    conn.close()
    return new_id

def get_by_id(role_id: int):
    # Получение одной роли по номеру
    conn = get_connection()
    cur = conn.cursor()
    # выбрать role_id и name из roles, где role_id равен заданному
    cur.execute("SELECT role_id, name FROM roles WHERE role_id = ?", (role_id,))
    row = cur.fetchone()   # одна строка или None
    conn.close()
    return _map(row) if row else None

def get_all():
    # Получение всех ролей
    conn = get_connection()
    cur = conn.cursor()
    # выбрать все роли, упорядочив по номеру
    cur.execute("SELECT role_id, name FROM roles ORDER BY role_id")
    rows = cur.fetchall()  # список всех строк
    conn.close()
    return [_map(r) for r in rows]

def update(role_id: int, name: str):
    # Изменение названия роли
    conn = get_connection()
    cur = conn.cursor()
    # обновить roles: установить новое name для записи с этим role_id
    cur.execute("UPDATE roles SET name = ? WHERE role_id = ?", (name, role_id))
    conn.commit()
    conn.close()

def delete(role_id: int):
    # Удаление роли
    conn = get_connection()
    cur = conn.cursor()
    # удалить из roles запись с этим role_id
    cur.execute("DELETE FROM roles WHERE role_id = ?", (role_id,))
    conn.commit()
    conn.close()