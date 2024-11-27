from flask import Flask, render_template, redirect, url_for, request, flash
from db import create_users_db, get_condition_db

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        # Создаем пользователя в БД
        create_users_db(username)
        # Получаем сгенерированный пасскод
        user = get_condition_db('users', f"username = '{username}'")[0]
        secret_key = user[2]  # Получаем secret_key из результата запроса
        # Показываем пасскод пользователю
        flash(secret_key)
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

if __name__ == '__main__':
    app.run(host="localhost", port=80, debug=True)
