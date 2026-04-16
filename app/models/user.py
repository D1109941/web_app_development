import sqlite3
from app.models import get_db

class User:
    @staticmethod
    def create(username, password_hash, is_admin=0):
        """
        建立新的使用者帳號
        
        :param username: 使用者名稱 (字串)
        :param password_hash: 加密過後的密碼 (字串)
        :param is_admin: 是否為管理員 (預設為 0)
        :return: 成功建立時回傳 user_id，若帳號已存在或發生錯誤則回傳 None
        """
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO users (username, password_hash, is_admin) VALUES (?, ?, ?)',
                (username, password_hash, is_admin)
            )
            conn.commit()
            user_id = cursor.lastrowid
            return user_id
        except sqlite3.IntegrityError:
            # 帳號重複
            return None
        except Exception as e:
            print(f"Error creating user: {e}")
            return None
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def get_by_username(username):
        """
        根據帳號名稱取得使用者資料
        
        :param username: 使用者名稱 (字串)
        :return: 成功時回傳包含資料的 dictionary，找不到或錯誤則回傳 None
        """
        try:
            conn = get_db()
            user = conn.execute(
                'SELECT * FROM users WHERE username = ?',
                (username,)
            ).fetchone()
            return dict(user) if user else None
        except Exception as e:
            print(f"Error getting user: {e}")
            return None
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def get_by_id(user_id):
        """
        根據 ID 取得使用者資料
        
        :param user_id: 使用者 ID (整數)
        :return: 成功時回傳包含資料的 dictionary，找不到或錯誤則回傳 None
        """
        try:
            conn = get_db()
            user = conn.execute(
                'SELECT * FROM users WHERE id = ?',
                (user_id,)
            ).fetchone()
            return dict(user) if user else None
        except Exception as e:
            print(f"Error getting user by id: {e}")
            return None
        finally:
            if 'conn' in locals():
                conn.close()
