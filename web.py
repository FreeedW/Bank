from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('base.html')

@app.route('/register')
def register():
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
    app.run(host="localhost", port=8080, debug=True)
