from flask import Flask, render_template, request, redirect, url_for, flash, session
from db import DB
import os
from dotenv import load_dotenv
from authlib.integrations.flask_client import OAuth

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
db = DB()

# Auth0 Configuration
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
oauth = OAuth(app)
auth0 = oauth.register(
    'auth0',
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    api_base_url=f'https://{AUTH0_DOMAIN}',
    access_token_url=f'https://{AUTH0_DOMAIN}/oauth/token',
    authorize_url=f'https://{AUTH0_DOMAIN}/authorize',
    client_kwargs={'scope': 'openid profile email'},
)

def is_ajax_request():
    return request.headers.get('X-Requested-With') == 'XMLHttpRequest'

@app.route('/')
def index():
    session.clear()
    if is_ajax_request():
        return render_template('home_content.html')
    return render_template('base.html')

@app.route('/login')
def login():
    return auth0.authorize_redirect(redirect_uri=url_for('callback', _external=True))

@app.route('/callback')
def callback():
    token = auth0.authorize_access_token()
    user_info = auth0.get('userinfo').json()
    
    session['email'] = user_info['email']
    session['name'] = user_info['name']
    
    # You can also save user info to your database if needed
    # Check if user exists in your DB and create if not
    user = db.get_user_by_email(user_info['email'])
    if not user:
        db.add_user({
            'name': user_info['name'],
            'email': user_info['email'],
            'saved_restaurants': []
        })

    return redirect(url_for('profile'))

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
    return redirect(auth0.logout())

@app.route('/restaurant', methods=['GET'])
def restaurant():
    if request.method == 'GET':
        restaurant = request.args.get('name')

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