from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user
from werkzeug.security import generate_password_hash, check_password_hash
import os

# Flaskオブジェクト生成
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SECRET_KEY'] = os.urandom(24)

# ログインマネージャ
login_manager = LoginManager()
login_manager.init_app(app)

# DBオブジェクト生成
db = SQLAlchemy(app)

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    passwd = db.Column(db.String(25))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def top():
    users = User.query.all()
    return render_template('top.html', users=users)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    print('signup method', request.method)
    if request.method == 'POST':
        # リクエスト取得
        name = request.form.get('name')
        passwd = request.form.get('passwd')
        
        # インスタンス生成
        user = User(name=name, passwd=generate_password_hash(passwd, method='sha256'))
        
        # トランザクション処理
        db.session.add(user)
        db.session.commit()
        print('1')
        # return render_template('home.html', user=user)
        return redirect(url_for('login', user=user))
    else:
        return render_template('top.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    print('login method', request.method)
    # if request.method == 'POST':
    # リクエスト取得
    name = request.form.get('name')
    passwd = request.form.get('passwd')
    print('passwd', passwd)
    
    # ユーザ取得
    user = User.query.filter_by(name=name).first()
    
    # パスワードチェック
    if check_password_hash(user.passwd, passwd):
        return redirect(url_for('home'))
    # else:
    #     print('login else')
    #     return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, port=5050)