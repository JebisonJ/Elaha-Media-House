
from flask import Flask, request, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))

with app.app_context():
    db.create_all()

@app.route('/register', methods=['POST'])
def register():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()
    if user:
        return redirect(url_for('home', error='Email already exists'))

    new_user = User(
        email=email,
        name=name,
        password=generate_password_hash(password, method='sha256')
    )
    db.session.add(new_user)
    db.session.commit()
    return redirect(url_for('home', message='Registration successful'))

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return redirect(url_for('home', error='Invalid credentials'))

    session['user_id'] = user.id
    return redirect(url_for('home', message='Login successful'))

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000)
