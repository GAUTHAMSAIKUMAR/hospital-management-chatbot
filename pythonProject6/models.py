import sqlite3

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password

    @staticmethod
    def username_exists(username):
        conn = sqlite3.connect('healthcare.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cursor.fetchone()
        conn.close()
        return user is not None

    @staticmethod
    def authenticate(username, password):
        conn = sqlite3.connect('healthcare.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
        user = cursor.fetchone()
        conn.close()
        if user:
            return User(user[1], user[2])
        return None

    @staticmethod
    def get_all():
        conn = sqlite3.connect('healthcare.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users")
        users = cursor.fetchall()
        conn.close()
        return users

    @staticmethod
    def delete(username):
        conn = sqlite3.connect('healthcare.db')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM users WHERE username=?", (username,))
        conn.commit()
        conn.close()

    def save(self):
        conn = sqlite3.connect('healthcare.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (self.username, self.password))
        conn.commit()
        conn.close()

class Appointment:
    def __init__(self, name, specialist, doctor):
        self.name = name
        self.specialist = specialist
        self.doctor = doctor

    @staticmethod
    def get_all():
        conn = sqlite3.connect('healthcare.db')
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM appointments")
        appointments = cursor.fetchall()
        conn.close()
        return appointments

    def save(self):
        conn = sqlite3.connect('healthcare.db')
        cursor = conn.cursor()
        cursor.execute("INSERT INTO appointments (name, specialist, doctor) VALUES (?, ?, ?)", (self.name, self.specialist, self.doctor))
        conn.commit()
        conn.close()
