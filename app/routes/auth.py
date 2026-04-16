from flask import Blueprint, render_template, request, redirect, url_for, session, flash

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    處理會員註冊。
    GET: 渲染 register.html
    POST: 接收表單參數、驗證密碼一致性、建立帳號並重導向登入頁。
    """
    pass

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    處理會員登入。
    GET: 渲染 login.html
    POST: 驗證帳號密碼，成功則設定 session['user_id'] 並重導向首頁。
    """
    pass

@auth_bp.route('/logout', methods=['POST'])
def logout():
    """
    處理會員登出。
    POST: 清除 session 資料，重導向至登入頁或首頁。
    """
    pass
