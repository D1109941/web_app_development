from app.models import get_db

class User:
    @staticmethod
    def create(username, password_hash, is_admin=0):
        conn = get_db()
        cursor = conn.cursor()
        try:
            cursor.execute(
                'INSERT INTO users (username, password_hash, is_admin) VALUES (?, ?, ?)',
                (username, password_hash, is_admin)
            )
            conn.commit()
            user_id = cursor.lastrowid
        except sqlite3.IntegrityError:
            # Username already exists
            user_id = None
        finally:
            conn.close()
        return user_id

    @staticmethod
    def get_by_username(username):
        conn = get_db()
        user = conn.execute(
            'SELECT * FROM users WHERE username = ?',
            (username,)
        ).fetchone()
        conn.close()
        return dict(user) if user else None

    @staticmethod
    def get_by_id(user_id):
        conn = get_db()
        user = conn.execute(
            'SELECT * FROM users WHERE id = ?',
            (user_id,)
        ).fetchone()
        conn.close()
        return dict(user) if user else None
