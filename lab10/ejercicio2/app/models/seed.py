import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "retailnova.db")
SQL_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "retailnova_db.sql")


def seed_database():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    for enc in ("utf-8-sig", "utf-8", "utf-16", "latin-1"):
        try:
            with open(SQL_PATH, "r", encoding=enc) as f:
                sql_script = f.read()
            break
        except UnicodeDecodeError:
            continue

    cursor.executescript(sql_script)
    conn.commit()
    conn.close()
    print(f"Base de datos creada en {DB_PATH}")


if __name__ == "__main__":
    seed_database()
