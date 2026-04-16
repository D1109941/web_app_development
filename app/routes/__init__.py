"""
這個模組包含了應用程式的 Flask Blueprints (包含各種路由視圖)。
由上層 application 負責引入這些 bp 並執行 app.register_blueprint()。
"""
from .auth import auth_bp
from .recipe import recipe_bp
from .collection import collection_bp

__all__ = ['auth_bp', 'recipe_bp', 'collection_bp']
