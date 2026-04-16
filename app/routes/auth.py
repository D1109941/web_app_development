from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    處理會員註冊。
    GET: 渲染 register.html
    POST: 接收參數、驗證密碼、建立帳號並重導向登入頁。
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        if not username or not password:
            flash('請輸入帳號與密碼。', 'danger')
            return redirect(url_for('auth.register'))
        
        if password != confirm_password:
            flash('兩次輸入的密碼不一致。', 'danger')
            return redirect(url_for('auth.register'))
            
        password_hash = generate_password_hash(password)
        # 預設把 admin 帳號設為 1 為了測試方便，實務上可根據需求限制
        is_admin = 1 if username == 'admin' else 0
        
        user_id = User.create(username, password_hash, is_admin)
        
        if user_id is None:
            flash('該帳號已經被註冊過了，請換一個名稱。', 'danger')
            return redirect(url_for('auth.register'))
            
        flash('註冊成功！請登入。', 'success')
        return redirect(url_for('auth.login'))

    return render_template('auth/register.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    處理會員登入。
    GET: 渲染 login.html
    POST: 驗證帳密，設定 session['user_id'] 並重導向首頁。
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('請輸入帳號與密碼。', 'danger')
            return redirect(url_for('auth.login'))

        user = User.get_by_username(username)
        if user is None or not check_password_hash(user['password_hash'], password):
            flash('帳號或密碼錯誤。', 'danger')
            return redirect(url_for('auth.login'))
            
        session.clear()
        session['user_id'] = user['id']
        session['username'] = user['username']
        session['is_admin'] = user['is_admin']
        
        flash('登入成功！', 'success')
        return redirect(url_for('recipe.index'))

    return render_template('auth/login.html')

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """
    處理會員登出，清除 session。
    """
    session.clear()
    flash('已成功登出。', 'success')
    return redirect(url_for('recipe.index'))
