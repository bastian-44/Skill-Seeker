import sqlite3

def get_db():
    db = sqlite3.connect('database.db', check_same_thread=False)
    return db


def init_db():
    db = get_db()
    cur = db.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Planner (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            rut TEXT,
            password TEXT
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT,
            planner_id INTEGER,
            FOREIGN KEY(planner_id) REFERENCES Planner(id)
        )
    ''')
    cur.execute('''
        CREATE TABLE IF NOT EXISTS WorkshopLeader (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            description TEXT,
            phone TEXT,
            email TEXT,
            networks TEXT,
            request_id INTEGER,
            favorite INTEGER DEFAULT 0,
            contacted INTEGER DEFAULT 0,
            FOREIGN KEY(request_id) REFERENCES Requests(id)
        )
    ''')
    db.commit()
    db.close()