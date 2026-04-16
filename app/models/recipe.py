import sqlite3
from app.models import get_db

class Recipe:
    @staticmethod
    def create(title, description, instructions, category):
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute(
            'INSERT INTO recipes (title, description, instructions, category) VALUES (?, ?, ?, ?)',
            (title, description, instructions, category)
        )
        conn.commit()
        recipe_id = cursor.lastrowid
        conn.close()
        return recipe_id

    @staticmethod
    def get_all(keyword=None):
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
        conn.close()
        return [dict(r) for r in recipes]

    @staticmethod
    def get_by_id(recipe_id):
        conn = get_db()
        recipe = conn.execute(
            'SELECT * FROM recipes WHERE id = ?',
            (recipe_id,)
        ).fetchone()
        conn.close()
        return dict(recipe) if recipe else None

    @staticmethod
    def update(recipe_id, title, description, instructions, category):
        conn = get_db()
        conn.execute(
            'UPDATE recipes SET title = ?, description = ?, instructions = ?, category = ? WHERE id = ?',
            (title, description, instructions, category, recipe_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def delete(recipe_id):
        conn = get_db()
        conn.execute('DELETE FROM recipes WHERE id = ?', (recipe_id,))
        conn.commit()
        conn.close()


class Ingredient:
    @staticmethod
    def add_to_recipe(recipe_id, name, amount):
        conn = get_db()
        conn.execute(
            'INSERT INTO ingredients (recipe_id, name, amount) VALUES (?, ?, ?)',
            (recipe_id, name, amount)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def get_by_recipe(recipe_id):
        conn = get_db()
        ingredients = conn.execute(
            'SELECT * FROM ingredients WHERE recipe_id = ?',
            (recipe_id,)
        ).fetchall()
        conn.close()
        return [dict(i) for i in ingredients]

    @staticmethod
    def clear_by_recipe(recipe_id):
        conn = get_db()
        conn.execute('DELETE FROM ingredients WHERE recipe_id = ?', (recipe_id,))
        conn.commit()
        conn.close()


class Collection:
    @staticmethod
    def add(user_id, recipe_id):
        conn = get_db()
        try:
            conn.execute(
                'INSERT INTO user_collections (user_id, recipe_id) VALUES (?, ?)',
                (user_id, recipe_id)
            )
            conn.commit()
        except sqlite3.IntegrityError:
            pass # Already collected
        finally:
            conn.close()

    @staticmethod
    def remove(user_id, recipe_id):
        conn = get_db()
        conn.execute(
            'DELETE FROM user_collections WHERE user_id = ? AND recipe_id = ?',
            (user_id, recipe_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def get_by_user(user_id):
        conn = get_db()
        recipes = conn.execute('''
            SELECT r.* FROM recipes r
            JOIN user_collections c ON r.id = c.recipe_id
            WHERE c.user_id = ?
            ORDER BY c.created_at DESC
        ''', (user_id,)).fetchall()
        conn.close()
        return [dict(r) for r in recipes]

    @staticmethod
    def is_collected(user_id, recipe_id):
        conn = get_db()
        result = conn.execute(
            'SELECT 1 FROM user_collections WHERE user_id = ? AND recipe_id = ?',
            (user_id, recipe_id)
        ).fetchone()
        conn.close()
        return bool(result)


class Checklist:
    @staticmethod
    def add_item(user_id, name, amount):
        conn = get_db()
        conn.execute(
            'INSERT INTO checklist_items (user_id, name, amount) VALUES (?, ?, ?)',
            (user_id, name, amount)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def get_by_user(user_id):
        conn = get_db()
        items = conn.execute(
            'SELECT * FROM checklist_items WHERE user_id = ? ORDER BY created_at ASC',
            (user_id,)
        ).fetchall()
        conn.close()
        return [dict(i) for i in items]

    @staticmethod
    def toggle_status(item_id, user_id):
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
        conn.close()

    @staticmethod
    def remove_item(item_id, user_id):
        conn = get_db()
        conn.execute(
            'DELETE FROM checklist_items WHERE id = ? AND user_id = ?',
            (item_id, user_id)
        )
        conn.commit()
        conn.close()

    @staticmethod
    def clear_checked(user_id):
        conn = get_db()
        conn.execute(
            'DELETE FROM checklist_items WHERE user_id = ? AND is_checked = 1',
            (user_id,)
        )
        conn.commit()
        conn.close()
