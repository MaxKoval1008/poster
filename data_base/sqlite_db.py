import sqlite3


class UsersBase:

    def __init__(self, database) -> object:
        self.conn = sqlite3.connect(database)
        self.cur = self.conn.cursor()

    def create_table_announcement(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS poster(
                         id INTEGER PRIMARY KEY AUTOINCREMENT, 
                         town TEXT, 
                         type TEXT, 
                         title TEXT, 
                         description TEXT, 
                         place TEXT, 
                         date_time INTEGER,
                         cost TEXT, 
                         telephone TEXT,
                         approved TEXT)''')

    def add_to_db_announcement(self, list):
        self.cur.execute('''INSERT INTO poster(town, type, title, description, place, date_time, cost, 
        telephone, approved) VALUES(?,?,?,?,?,?,?,?,?)''', list)
        self.conn.commit()

    def approved_user_announcement(self, town):
        self.cur.execute("SELECT * FROM poster WHERE town=? AND approved='Approved'", (town,))
        return self.cur.fetchall()

    def disapproved_user_announcement(self):
        self.cur.execute("SELECT * FROM poster WHERE approved='Disapproved'",)
        return self.cur.fetchall()

    def check_announcement(self, id):
        return bool(self.cur.execute("SELECT * FROM poster WHERE id=?", (id,)).fetchone())

    def one_announcement(self, id):
        self.cur.execute("SELECT * FROM poster WHERE id=?", (id,))
        return self.cur.fetchone()

    def approving_announcement(self, id):
        self.cur.execute('''UPDATE poster SET approved='Approved' WHERE id=?''', (id,))
        self.conn.commit()

    def disapproving_announcement(self, id):
        self.cur.execute('''DELETE FROM poster WHERE id=?''', (id,))
        self.conn.commit()

    def all_announcements(self):
        self.cur.execute("SELECT * FROM poster")
        return self.cur.fetchall()

    def update_announcement(self, id, id_data, data):
        self.cur.execute(f'''UPDATE poster SET {id_data}={data} WHERE id=?''', (id,))
        self.conn.commit()
