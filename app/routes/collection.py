from flask import Blueprint, render_template, request, redirect, url_for, session, flash

collection_bp = Blueprint('collection', __name__, url_prefix='/collection')

@collection_bp.route('/')
def index():
    """
    查看已儲存的個人食譜清單。
    GET: 根據 session 裡的 user_id 取得收藏列表，渲染 collection/index.html
    """
    pass

@collection_bp.route('/save/<int:id>', methods=['POST'])
def save_recipe(id):
    """
    儲存/收藏特定食譜。
    POST: 驗證登入後，將該 recipe_id 紀錄到 user_collections 中，回原本頁面。
    """
    pass

@collection_bp.route('/remove/<int:id>', methods=['POST'])
def remove_recipe(id):
    """
    移除特定食譜的收藏。
    POST: 將該 recipe_id 的對應 user_collections 紀錄刪除。
    """
    pass

@collection_bp.route('/checklist', methods=['GET'])
def checklist():
    """
    瀏覽與勾選準備狀態。
    GET: 取得使用者的 checklist_items，渲染 checklist.html。
    """
    pass

@collection_bp.route('/checklist/add', methods=['POST'])
def add_to_checklist():
    """
    將多個食材批次加入準備清單。
    POST: 接收表單中的陣列資料，逐筆寫入 checkklist_items 提供未來採買。
    """
    pass

@collection_bp.route('/checklist/<int:item_id>/toggle', methods=['POST'])
def toggle_checklist_item(item_id):
    """
    切換食材準備 (打勾/取消) 的狀態。
    POST: 使用 AJAX 或是表單觸發，更新資料庫的 is_checked 狀態。
    """
    pass
