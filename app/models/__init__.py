import sqlite3
import os

# 取得專案根目錄 (位於 app/models/ 的上上層)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DB_PATH = os.path.join(BASE_DIR, 'instance', 'database.db')

def get_db():
    """與 SQLite 資料庫建立連線，啟動 Foreign Keys 並設定回傳 Row 格式供字典操作"""
    # 確保 instance 目錄存在
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    # 啟用 Foreign Key 支援 (SQLite 預設關閉)
    conn.execute('PRAGMA foreign_keys = ON;')
    return conn
