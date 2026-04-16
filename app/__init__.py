import os
import sqlite3
from flask import Flask

def create_app(test_config=None):
    # 建立與設定 Flask App
    app = Flask(__name__, instance_relative_config=True)
    
    # 載入 config.py
    app.config.from_object('config.Config')

    if test_config:
        app.config.from_mapping(test_config)

    # 確保 instance 資料夾存在
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    # 註冊 CLI 初始化資料庫的功能
    @app.cli.command('init-db')
    def init_db_command():
        """清除原有資料並建立新的資料表"""
        db_path = app.config['DATABASE']
        sql_path = os.path.join(app.root_path, '..', 'database', 'schema.sql')
        
        os.makedirs(os.path.dirname(db_path), exist_ok=True)
        conn = sqlite3.connect(db_path)
        with open(sql_path, 'r', encoding='utf-8') as f:
            conn.executescript(f.read())
        conn.commit()
        conn.close()
        print('成功初始化資料庫！')

    # 註冊 Blueprints
    from app.routes.auth import auth_bp
    from app.routes.recipe import recipe_bp
    from app.routes.collection import collection_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(recipe_bp)
    app.register_blueprint(collection_bp)

    return app
