from flask import Blueprint, render_template, request, redirect, url_for, session, flash

recipe_bp = Blueprint('recipe', __name__)

@recipe_bp.route('/')
def index():
    """
    顯示食譜列表 (支援首頁顯示與關鍵字搜尋)。
    GET: 取出所有食譜或符合 keyword 的食譜，並渲染 index.html。
    """
    pass

@recipe_bp.route('/recipe/new', methods=['GET', 'POST'])
def new_recipe():
    """
    新增食譜 (限管理員)。
    GET: 渲染 new.html 表單。
    POST: 接收表單資料、儲存食譜及相關食材至資料庫，完成後重導向至首頁。
    """
    pass

@recipe_bp.route('/recipe/<int:id>')
def detail(id):
    """
    檢視食譜完整圖文步驟與食材。
    GET: 根據參數 id 取得單筆 Recipe 與關聯 Ingredient 列表，渲染 detail.html。
    """
    pass

@recipe_bp.route('/recipe/<int:id>/edit', methods=['GET', 'POST'])
def edit_recipe(id):
    """
    編輯既有食譜 (限管理員)。
    GET: 取出舊食譜資料，渲染 edit.html 準備進行修改。
    POST: 更新表單傳來的資料 (包含清空舊食材重新建立)，完成後重導回詳細頁。
    """
    pass

@recipe_bp.route('/recipe/<int:id>/delete', methods=['POST'])
def delete_recipe(id):
    """
    刪除食譜 (限管理員)。
    POST: 依據 id 把該食譜刪除 (連帶移除收藏紀錄與食材)，完成後重導向至首頁。
    """
    pass
