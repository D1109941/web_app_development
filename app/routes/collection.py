from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from functools import wraps
from app.models.recipe import Collection, Checklist, Recipe

collection_bp = Blueprint('collection', __name__, url_prefix='/collection')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('存取此功能前請先登入！', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@collection_bp.route('/')
@login_required
def index():
    """查看已儲存的個人食譜清單"""
    recipes = Collection.get_by_user(session['user_id'])
    return render_template('collection/index.html', recipes=recipes)

@collection_bp.route('/save/<int:id>', methods=['POST'])
@login_required
def save_recipe(id):
    """將食譜加入收藏"""
    recipe = Recipe.get_by_id(id)
    if not recipe:
        flash('找不到該食譜！', 'danger')
    else:
        if Collection.add(session['user_id'], id):
            flash('已成功加入收藏！', 'success')
        else:
            flash('加入收藏過程發生錯誤。', 'danger')
    return redirect(url_for('recipe.detail', id=id))

@collection_bp.route('/remove/<int:id>', methods=['POST'])
@login_required
def remove_recipe(id):
    """將食譜從首選移除"""
    if Collection.remove(session['user_id'], id):
        flash('已從您的收藏清單中移除。', 'success')
    return redirect(url_for('collection.index'))

@collection_bp.route('/checklist', methods=['GET'])
@login_required
def checklist():
    """瀏覽目前的準備清單"""
    items = Checklist.get_by_user(session['user_id'])
    return render_template('collection/checklist.html', items=items)

@collection_bp.route('/checklist/add', methods=['POST'])
@login_required
def add_to_checklist():
    """批次將食材寫入準備庫"""
    names = request.form.getlist('ingredient_name[]')
    amounts = request.form.getlist('ingredient_amount[]')
    
    count = 0
    for name, amount in zip(names, amounts):
        if name.strip():
            Checklist.add_item(session['user_id'], name.strip(), amount.strip())
            count += 1
            
    if count > 0:
        flash(f'成功為您準備清單加入了 {count} 項食材！', 'success')
    else:
        flash('沒有選擇任何食材加入清單。', 'warning')
        
    return redirect(request.referrer or url_for('collection.checklist'))

@collection_bp.route('/checklist/<int:item_id>/toggle', methods=['POST'])
@login_required
def toggle_checklist_item(item_id):
    """切換打勾狀態 (支援 AJAX)"""
    success = Checklist.toggle_status(item_id, session['user_id'])
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'success': success})
    
    if not success:
        flash('無法更新清單狀態', 'danger')
    return redirect(url_for('collection.checklist'))
