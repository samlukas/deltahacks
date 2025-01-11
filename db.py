import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime
import os

class DB:
    def __init__(self):
        cred = credentials.Certificate(os.environ.get("FIREBASE_API_PATH"))
        firebase_admin.initialize_app(cred)
        
        try:
            self.db = firestore.client()
            print('Connected to Firebase')
        except Exception as e:
            print(f'Failed to connect to Firebase: {str(e)}')
            raise

    def get_userdb(self):
        return self.db.collection('user')
    
    def add_user(self, user):
        try: 
            if self.get_user_by_email(user['email']):
                print('User already exists')
                return False
            
            self.db.collection('user').add(user)
            return True
        except Exception as e:
            print(f'Error adding user: {str(e)}')
            return False

    def get_user_by_email(self, email):
        users = self.db.collection('user').where('email', '==', email).limit(1).get()
        for user in users:
            return user.to_dict()
        return None

    def add_restaurant(self, userid, restaurant):
        try:
            data = {
                'userid': userid,
                'restaurant': restaurant, 
                'date': datetime.now()
            }
            self.db.collection('restaurant').add(data)
            return True
        except Exception as e:
            print(f'Error adding restaurant: {str(e)}')
            return False
    
    def get_restaurant_by_user(self, userid):
        restaurants = self.db.collection('restaurant').where('userid', '==', userid).get()
        return [doc.to_dict() for doc in restaurants]
    
    def get_user_by_restaurant(self, restaurant):
        users = self.db.collection('restaurant').where('restaurant', '==', restaurant).get()
        return [doc.to_dict() for doc in users]