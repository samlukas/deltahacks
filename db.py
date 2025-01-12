import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timedelta
import os
from cohere_scripts import MAPPINGS, create_embeddings, calculate_similarity

class DB:
    def __init__(self):
        cred = credentials.Certificate(os.environ.get("FIREBASE_API_PATH"))
        firebase_admin.initialize_app(cred)
        embeddings = create_embeddings()
        
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
            match = self.check_matches(restaurant)
            if match is not None:
                pass # email function here
            return True
        except Exception as e:
            print(f'Error adding restaurant: {str(e)}')
            return False
    
    def get_restaurant_by_user(self, email):
        restaurants = self.db.collection('restaurant').where('email', '==', email).get()
        return [doc.to_dict() for doc in restaurants]
    
    def get_user_by_restaurant(self, restaurant):
        users = self.db.collection('restaurant').where('restaurant', '==', restaurant).get()
        return [doc.to_dict() for doc in users]
    
    def check_matches(self, restaurant):
        user_data = self.get_user_by_restaurant(restaurant)
        now = datetime.now()
        time_24_hours_ago = now - timedelta(hours=24)

        filtered_data = [entry for entry in user_data if entry['date'] >= time_24_hours_ago]
        users = [self.get_user_by_email(entry['email']) for entry in filtered_data]
        filtered_users = [user for user in users if user is not None]

        user_answers = [[user['relationship_goals'], user['affection_expression'], user['free_time'], user['motivation'], user['communication_style']] for user in filtered_users]
        user_embeddings = self.answers_to_embeddings(user_answers)

        if len(user_embeddings) < 2:
            return None
        else:
            return self.find_max_similarity(user_embeddings)
 
    def answers_to_embeddings(self, answers):
        matrix = []
        for user in answers:
            user_embeddings = [
                self.embeddings[i, MAPPINGS[i][answer]] for i, answer in enumerate(user)
            ]
            matrix.append(user_embeddings)
        return matrix
    

    def find_max_similarity(self, user_embeddings):
        max_similarity = float('-inf')  # Initialize with a very low value
        max_pair = None

        # Iterate over all pairs of embeddings
        for i in range(len(user_embeddings)):
            for j in range(i + 1, len(user_embeddings)):  # Only consider pairs (i, j) where i < j
                sim = calculate_similarity(user_embeddings[i], user_embeddings[j])
                if sim > max_similarity:
                    max_similarity = sim
                    max_pair = (i, j)

        return max_pair

