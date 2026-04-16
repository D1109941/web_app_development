import sqlite3
from app.models import get_db

class Recipe:
    @staticmethod
    def create(title, description, instructions, category):
        """
        新增單筆食譜
        
        :param title: 食譜標題
        :param description: 食譜簡介
        :param instructions: 步驟說明
        :param category: 料理種類
        :return: 新增成功的 recipe_id，失敗則回傳 None
        """
        try:
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute(
                'INSERT INTO recipes (title, description, instructions, category) VALUES (?, ?, ?, ?)',
                (title, description, instructions, category)
            )
            conn.commit()
            return cursor.lastrowid
        except Exception as e:
            print(f"Error creating recipe: {e}")
            return None
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def get_all(keyword=None):
        """
        取得所有食譜清單，可搭配關鍵字搜尋標題與分類
        
        :param keyword: 搜尋關鍵字 (預設 None)
        :return: 包含所有食譜 dictionary 的 list，錯誤則回傳空 list
        """
        try:
            conn = get_db()
            if keyword:
                recipes = conn.execute(
                    'SELECT * FROM recipes WHERE title LIKE ? OR category LIKE ? ORDER BY created_at DESC',
                    (f'%{keyword}%', f'%{keyword}%')
                ).fetchall()
            else:
                recipes = conn.execute(
                    'SELECT * FROM recipes ORDER BY created_at DESC'
                ).fetchall()
            return [dict(r) for r in recipes]
        except Exception as e:
            print(f"Error fetching recipes: {e}")
            return []
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def get_by_id(recipe_id):
        """
        取得單筆食譜詳細資料
        
        :param recipe_id: 食譜 ID
        :return: 食譜資料字典，找不到或錯誤則回傳 None
        """
        try:
            conn = get_db()
            recipe = conn.execute(
                'SELECT * FROM recipes WHERE id = ?',
                (recipe_id,)
            ).fetchone()
            return dict(recipe) if recipe else None
        except Exception as e:
            print(f"Error getting recipe: {e}")
            return None
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def update(recipe_id, title, description, instructions, category):
        """
        更新現有單筆食譜
        
        :param recipe_id: 食譜 ID
        :param title: 食譜標題
        :param description: 食譜簡介
        :param instructions: 步驟說明
        :param category: 料理種類
        :return: 成功回傳 True，失敗回傳 False
        """
        try:
            conn = get_db()
            conn.execute(
                'UPDATE recipes SET title = ?, description = ?, instructions = ?, category = ? WHERE id = ?',
                (title, description, instructions, category, recipe_id)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error updating recipe: {e}")
            return False
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def delete(recipe_id):
        """
        刪除特定食譜
        
        :param recipe_id: 食譜 ID
        :return: 成功回傳 True，失敗回傳 False
        """
        try:
            conn = get_db()
            conn.execute('DELETE FROM recipes WHERE id = ?', (recipe_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error deleting recipe: {e}")
            return False
        finally:
            if 'conn' in locals():
                conn.close()


class Ingredient:
    @staticmethod
    def add_to_recipe(recipe_id, name, amount):
        """
        將食材綁定到特定食譜
        
        :param recipe_id: 食譜 ID
        :param name: 食材名稱
        :param amount: 份量
        :return: 成功回傳 True，失敗回傳 False
        """
        try:
            conn = get_db()
            conn.execute(
                'INSERT INTO ingredients (recipe_id, name, amount) VALUES (?, ?, ?)',
                (recipe_id, name, amount)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error adding ingredient: {e}")
            return False
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def get_by_recipe(recipe_id):
        """
        取得特定食譜的食材清單
        
        :param recipe_id: 食譜 ID
        :return: 此食譜關聯的食材 dict 之 list
        """
        try:
            conn = get_db()
            ingredients = conn.execute(
                'SELECT * FROM ingredients WHERE recipe_id = ?',
                (recipe_id,)
            ).fetchall()
            return [dict(i) for i in ingredients]
        except Exception as e:
            print(f"Error fetching ingredients: {e}")
            return []
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def clear_by_recipe(recipe_id):
        """
        清除特定食譜的所有食材資料(通常配合更新使用)
        
        :param recipe_id: 食譜 ID
        :return: 成功回傳 True，失敗回傳 False
        """
        try:
            conn = get_db()
            conn.execute('DELETE FROM ingredients WHERE recipe_id = ?', (recipe_id,))
            conn.commit()
            return True
        except Exception as e:
            print(f"Error clearing ingredients: {e}")
            return False
        finally:
            if 'conn' in locals():
                conn.close()


class Collection:
    @staticmethod
    def add(user_id, recipe_id):
        """
        將食譜加入到使用者的收藏
        
        :param user_id: 使用者 ID
        :param recipe_id: 食譜 ID
        :return: 成功回傳 True，失敗回傳 False
        """
        try:
            conn = get_db()
            conn.execute(
                'INSERT INTO user_collections (user_id, recipe_id) VALUES (?, ?)',
                (user_id, recipe_id)
            )
            conn.commit()
            return True
        except sqlite3.IntegrityError:
            # 已經收藏過了
            return True
        except Exception as e:
            print(f"Error adding to collection: {e}")
            return False
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def remove(user_id, recipe_id):
        """
        將食譜從使用者收藏中移除
        
        :param user_id: 使用者 ID
        :param recipe_id: 食譜 ID
        :return: 成功回傳 True，失敗回傳 False
        """
        try:
            conn = get_db()
            conn.execute(
                'DELETE FROM user_collections WHERE user_id = ? AND recipe_id = ?',
                (user_id, recipe_id)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error removing from collection: {e}")
            return False
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def get_by_user(user_id):
        """
        取得特定使用者的所有儲存食譜
        
        :param user_id: 使用者 ID
        :return: 食譜 dict 之 list
        """
        try:
            conn = get_db()
            recipes = conn.execute('''
                SELECT r.* FROM recipes r
                JOIN user_collections c ON r.id = c.recipe_id
                WHERE c.user_id = ?
                ORDER BY c.created_at DESC
            ''', (user_id,)).fetchall()
            return [dict(r) for r in recipes]
        except Exception as e:
            print(f"Error fetching user collections: {e}")
            return []
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def is_collected(user_id, recipe_id):
        """
        判斷特定使用者是否收藏了某食譜
        
        :param user_id: 使用者 ID
        :param recipe_id: 食譜 ID
        :return: 若有收藏回傳 True，否則 False
        """
        try:
            conn = get_db()
            result = conn.execute(
                'SELECT 1 FROM user_collections WHERE user_id = ? AND recipe_id = ?',
                (user_id, recipe_id)
            ).fetchone()
            return bool(result)
        except Exception as e:
            print(f"Error checking collected status: {e}")
            return False
        finally:
            if 'conn' in locals():
                conn.close()


class Checklist:
    @staticmethod
    def add_item(user_id, name, amount):
        """
        將食材加入到個人的準備清單
        
        :param user_id: 使用者 ID
        :param name: 食材名稱
        :param amount: 食材份量
        :return: 成功回傳 True，失敗回傳 False
        """
        try:
            conn = get_db()
            conn.execute(
                'INSERT INTO checklist_items (user_id, name, amount) VALUES (?, ?, ?)',
                (user_id, name, amount)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error adding checklist item: {e}")
            return False
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def get_by_user(user_id):
        """
        取得特定使用者的所有採買清單項目
        
        :param user_id: 使用者 ID
        :return: 清單 dict 的 list
        """
        try:
            conn = get_db()
            items = conn.execute(
                'SELECT * FROM checklist_items WHERE user_id = ? ORDER BY created_at ASC',
                (user_id,)
            ).fetchall()
            return [dict(i) for i in items]
        except Exception as e:
            print(f"Error fetching checklist: {e}")
            return []
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def toggle_status(item_id, user_id):
        """
        切換採買清單的準備狀態 (打勾/取消打勾)
        
        :param item_id: 清單項目 ID
        :param user_id: 擁有此清單的使用者 ID (安全防護)
        :return: 成功回傳 True，發生錯誤回傳 False
        """
        try:
            conn = get_db()
            item = conn.execute(
                'SELECT is_checked FROM checklist_items WHERE id = ? AND user_id = ?',
                (item_id, user_id)
            ).fetchone()
            if item:
                new_status = 0 if item['is_checked'] else 1
                conn.execute(
                    'UPDATE checklist_items SET is_checked = ? WHERE id = ?',
                    (new_status, item_id)
                )
                conn.commit()
            return True
        except Exception as e:
            print(f"Error toggling checklist status: {e}")
            return False
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def remove_item(item_id, user_id):
        """
        刪除特定準備清單項目
        
        :param item_id: 清單項目 ID
        :param user_id: 使用者 ID
        :return: 成功回傳 True，發生錯誤回傳 False
        """
        try:
            conn = get_db()
            conn.execute(
                'DELETE FROM checklist_items WHERE id = ? AND user_id = ?',
                (item_id, user_id)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error removing checklist item: {e}")
            return False
        finally:
            if 'conn' in locals():
                conn.close()

    @staticmethod
    def clear_checked(user_id):
        """
        清除目前已打勾確認完成的所有準備項目
        
        :param user_id: 使用者 ID
        :return: 成功回傳 True，發生錯誤回傳 False
        """
        try:
            conn = get_db()
            conn.execute(
                'DELETE FROM checklist_items WHERE user_id = ? AND is_checked = 1',
                (user_id,)
            )
            conn.commit()
            return True
        except Exception as e:
            print(f"Error clearing checked items: {e}")
            return False
        finally:
            if 'conn' in locals():
                conn.close()
