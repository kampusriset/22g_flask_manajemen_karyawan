import MySQLdb
from werkzeug.security import generate_password_hash, check_password_hash

class Database:
    def __init__(self):
        self.connection = MySQLdb.connect(
            host='localhost',
            user='root',
            password='',
            database='library'
        )
        self.cursor = self.connection.cursor()

    def close(self):
        self.cursor.close()
        self.connection.close()

class User:
    def __init__(self, username, password):
        self.username = username
        self.password_hash = generate_password_hash(password)

    @staticmethod
    def create_user(username, password):
        db = Database()
        password_hash = generate_password_hash(password)
        db.cursor.execute("INSERT INTO users (username, password_hash) VALUES (%s, %s)",
                        (username, password_hash))
        db.connection.commit()
        db.close()

    @staticmethod
    def get_user_by_username(username):
        db = Database()
        db.cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
        user = db.cursor.fetchone()
        db.close()
        return user

    @staticmethod
    def verify_password(username, password):
        db = Database()
        db.cursor.execute("SELECT password_hash FROM users WHERE username = %s", (username,))
        result = db.cursor.fetchone()
        db.close()
        if result:
            return check_password_hash(result[0], password)
        return False

    @staticmethod
    def update_password(username, new_password):
        db = Database()
        password_hash = generate_password_hash(new_password)
        db.cursor.execute("UPDATE users SET password_hash = %s WHERE username = %s",
                        (password_hash, username))
        db.connection.commit()
        db.close()

class Karyawan:
    def __init__(self, nama, jabatan, alamat):
        self.nama = nama
        self.jabatan = jabatan
        self.alamat = alamat

    @staticmethod
    def get_all_karyawan(page=1, per_page=10, sort_by='nama', sort_order='asc'):
        db = Database()
        offset = (page - 1) * per_page
        query = f"SELECT * FROM karyawan ORDER BY {sort_by} {sort_order} LIMIT %s OFFSET %s"
        db.cursor.execute(query, (per_page, offset))
        karyawan = db.cursor.fetchall()
        db.close()
        return karyawan

    @staticmethod
    def get_karyawan(karyawan_id):
        db = Database()
        db.cursor.execute("SELECT * FROM karyawan WHERE id = %s", (karyawan_id,))
        karyawan = db.cursor.fetchone()
        db.close()
        return karyawan

    @staticmethod
    def create_karyawan(karyawan):
        db = Database()
        db.cursor.execute("INSERT INTO karyawan (nama, jabatan, alamat) VALUES (%s, %s, %s)",
        (karyawan.nama, karyawan.jabatan, karyawan.alamat))
        db.connection.commit()
        db.close()

    @staticmethod
    def update_karyawan(karyawan_id, karyawan):
        db = Database()
        db.cursor.execute("UPDATE karyawan SET nama = %s, jabatan = %s, alamat = %s WHERE id = %s",
        (karyawan.nama, karyawan.jabatan, karyawan.alamat, karyawan_id))
        db.connection.commit()
        db.close()

    @staticmethod
    def delete_karyawan(karyawan_id):
        db = Database()
        db.cursor.execute("DELETE FROM karyawan WHERE id = %s", (karyawan_id,))
        db.connection.commit()
        db.close()

    @staticmethod
    def search_karyawan(query):
        db = Database()
        db.cursor.execute("SELECT * FROM karyawan WHERE nama LIKE %s OR jabatan LIKE %s OR alamat LIKE %s", 
                        ('%' + query + '%', '%' + query + '%', '%' + query + '%'))
        karyawan = db.cursor.fetchall()
        db.close()
        return karyawan

    @staticmethod
    def count_karyawan():
        db = Database()
        db.cursor.execute("SELECT COUNT(*) FROM karyawan")
        count = db.cursor.fetchone()[0]
        db.close()
        return count

    @staticmethod
    def nama_exists(nama):
        db = Database()
        db.cursor.execute("SELECT COUNT(*) FROM karyawan WHERE nama = %s", (nama,))
        exists = db.cursor.fetchone()[0] > 0
        db.close()
        return exists
