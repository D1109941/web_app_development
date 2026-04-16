from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.models.recipe import Recipe, Ingredient

recipe_bp = Blueprint('recipe', __name__)

@recipe_bp.route('/')
def index():
    """
    顯示食譜列表 (支援首頁顯示與關鍵字搜尋)。
    GET: 取出所有食譜或符合 keyword 的食譜，渲染 index.html。
    """
    keyword = request.args.get('q')
    recipes = Recipe.get_all(keyword)
    return render_template('recipe/index.html', recipes=recipes, keyword=keyword)

@recipe_bp.route('/recipe/new', methods=['GET', 'POST'])
def new_recipe():
    """
    新增食譜 (限管理員)。
    GET: 渲染 new.html 表單。
    POST: 接收表單存入 DB，重導向至首頁。
    """
    if not session.get('is_admin'):
        flash('只限管理員才能新增食譜。', 'danger')
        return redirect(url_for('recipe.index'))

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        instructions = request.form.get('instructions')
        category = request.form.get('category')

        if not title:
            flash('食譜名稱為必填欄位。', 'danger')
            return redirect(url_for('recipe.new_recipe'))

        recipe_id = Recipe.create(title, description, instructions, category)
        if recipe_id:
            ingredient_names = request.form.getlist('ingredient_name[]')
            ingredient_amounts = request.form.getlist('ingredient_amount[]')
            for name, amount in zip(ingredient_names, ingredient_amounts):
                if name.strip():
                    Ingredient.add_to_recipe(recipe_id, name.strip(), amount.strip())
            
            flash('成功新增食譜！', 'success')
            return redirect(url_for('recipe.detail', id=recipe_id))
        else:
            flash('新增食譜發生錯誤。', 'danger')

    return render_template('recipe/new.html')

@recipe_bp.route('/recipe/<int:id>')
def detail(id):
    """
    檢視食譜完整圖文步驟與食材。
    GET: 渲染 detail.html，載入 Recipe 與 Incident 資料。
    """
    recipe = Recipe.get_by_id(id)
    if not recipe:
        flash('找不到該食譜。', 'danger')
        return redirect(url_for('recipe.index'))
        
    ingredients = Ingredient.get_by_recipe(id)
    return render_template('recipe/detail.html', recipe=recipe, ingredients=ingredients)

@recipe_bp.route('/recipe/<int:id>/edit', methods=['GET', 'POST'])
def edit_recipe(id):
    """
    編輯既有食譜 (限管理員)。
    GET: 取出食譜資料，渲染 edit.html 表單。
    POST: 更新資料，重導向至 detail 頁面。
    """
    if not session.get('is_admin'):
        flash('無權限進行編輯。', 'danger')
        return redirect(url_for('recipe.index'))
        
    recipe = Recipe.get_by_id(id)
    if not recipe:
        flash('找不到該食譜！', 'danger')
        return redirect(url_for('recipe.index'))

    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        instructions = request.form.get('instructions')
        category = request.form.get('category')
        
        if not title:
            flash('食譜名稱不可空白。', 'danger')
            return redirect(url_for('recipe.edit_recipe', id=id))

        if Recipe.update(id, title, description, instructions, category):
            Ingredient.clear_by_recipe(id)
            ingredient_names = request.form.getlist('ingredient_name[]')
            ingredient_amounts = request.form.getlist('ingredient_amount[]')
            for name, amount in zip(ingredient_names, ingredient_amounts):
                if name.strip():
                    Ingredient.add_to_recipe(id, name.strip(), amount.strip())
            flash('更新成功！', 'success')
            return redirect(url_for('recipe.detail', id=id))
        else:
            flash('更新失敗。', 'danger')

    ingredients = Ingredient.get_by_recipe(id)
    return render_template('recipe/edit.html', recipe=recipe, ingredients=ingredients)

@recipe_bp.route('/recipe/<int:id>/delete', methods=['POST'])
def delete_recipe(id):
    """
    刪除食譜 (限管理員)。
    """
    if not session.get('is_admin'):
        flash('無權限進行刪除。', 'danger')
        return redirect(url_for('recipe.index'))
        
    if Recipe.delete(id):
        flash('食譜已刪除。', 'success')
    else:
        flash('刪除發生錯誤。', 'danger')
        
    return redirect(url_for('recipe.index'))
