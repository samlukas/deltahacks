from flask import Flask, render_template, request, redirect, url_for, flash, session
from db import DB
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
db = DB()

def is_ajax_request():
    return request.headers.get('X-Requested-With') == 'XMLHttpRequest'

@app.route('/')
def index():
    session.clear()
    if is_ajax_request():
        return render_template('home_content.html')
    return render_template('base.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = db.get_user_by_email(email)
        if user and password == user.get('password'):
            session['email'] = email
            flash('Successfully logged in!')
            return render_template('profile.html', user=user)
        else:
            return 'Invalid email or password', 400
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        user_data = {
            'name': request.form.get('name'),
            'email': request.form.get('email'),
            'password': request.form.get('password'),

            'relationship_goals': request.form.get('relationship_goals'),
            'affection_expression': request.form.get('affection_expression'),
            'free_time': request.form.get('free_time'),
            'motivation': request.form.get('motivation'),
            'communication_style': request.form.get('communication_style'),

            'saved_restaurants': []
        }
        
        if db.get_user_by_email(user_data['email']):
            flash('Email already exists')
            return render_template('signup.html')
        
        if db.add_user(user_data):
            session['email'] = user_data['email']
            flash('Account created successfully!')
            return render_template('profile.html', user=user_data)
        else:
            return 'Error creating account', 400
    
    return render_template('signup.html')

@app.route('/profile', methods=['GET'])
def profile():
    if 'email' not in session:
        flash('Please login first')
        return redirect(url_for('login'))
    
    user = db.get_user_by_email(session['email'])
    if not user:
        session.clear()
        flash('User not found')
        return redirect(url_for('login'))
    
    restaurants = db.get_restaurant_by_user(user['email'])
    user['saved_restaurants'] = restaurants
    
    return render_template('profile.html', user=user)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route('/restaurant', methods=['GET'])
def restaurant():
    if request.method == 'GET':
        restaurant = request.args.get('name')
    # session['restaurant'] = restaurant

    if 'email' not in session:
        flash('Please login first')
        return redirect(url_for('login'))

    user = db.get_user_by_email(session['email'])
    if not user:
        session.clear()
        flash('User not found')
        return redirect(url_for('login'))

    db.add_restaurant(session['email'], restaurant)
    flash('Successfully added restaurant')

    return render_template('restaurant.html', user=user, restaurant=restaurant)

if __name__ == '__main__':
    app.run(debug=True)