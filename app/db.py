import sqlite3

class Database:
    def __init__(self):
        self.connection = sqlite3.connect("base.db")
        self.cursor = self.connection.cursor()

    def is_user_exists(self, user_id: int) -> bool:
        self.cursor.execute('SELECT 1 FROM user WHERE id = ?', (user_id,))
        return bool(self.cursor.fetchone())

    def add_user(self, user_id: int, username: str) -> bool:
        try:
            self.cursor.execute('''
                INSERT INTO user (id, username)
                VALUES (?, ?)
            ''', (user_id, username))
            self.connection.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def add_recipe(self, user_id: int, recipe: str) -> bool:
        try:
            self.cursor.execute('''
                INSERT INTO recipes (user_id, recipe)
                VALUES (?, ?)
            ''', (user_id, recipe))
            self.connection.commit()
            return True
        except Exception as e:
            print(f"Error adding recipe: {e}")
            return False
    
    def get_user_recipes(self, user_id: int) -> list:
        self.cursor.execute('SELECT recipe FROM recipes WHERE user_id = ?', (user_id,))
        return [row[0] for row in self.cursor.fetchall()]
    
    def close(self):
        if self.connection:
            self.connection.close()
            
    def __del__(self):
        self.close()