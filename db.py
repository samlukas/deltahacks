import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timedelta
import os
import base64
from cohere_scripts import MAPPINGS, create_embeddings, calculate_similarity
from dotenv import load_dotenv
from email_service import *

load_dotenv()

class DB:
    def __init__(self):
        encoded_cred = os.getenv("FIREBASE_API_B64")
        if not encoded_cred:
            raise ValueError("FIREBASE_API_B64 environment variable is not set")

        try:
            decoded_cred = base64.b64decode(encoded_cred)
        except base64.binascii.Error as e:
            raise ValueError("Failed to decode FIREBASE_API_B64. Ensure it is a valid Base64 string.") from e

        temp_file_path = "/tmp/firebase-credentials.json"

        with open(temp_file_path, "wb") as f:
            f.write(decoded_cred)

        cred = credentials.Certificate(temp_file_path)
        firebase_admin.initialize_app(cred)
        self.embeddings = create_embeddings()
        
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

    def add_restaurant(self, email, restaurant):
        # print(self.embeddings)
        try:
            data = {
                'email': email,
                'restaurant': restaurant, 
                'date': datetime.now()
            }
            self.db.collection('restaurant').add(data)
            match = self.check_matches(restaurant)
            if match is not None:
                print("match found")
                print(match[0])
                print(match[1])
                print(restaurant)
                send_email(match[0], match[1], restaurant)
                send_email(match[1], match[0], restaurant)
            else:
                print("no match found")
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
        print(f"userdata: {user_data}")
        now = datetime.now()
        time_24_hours_ago = now - timedelta(hours=24)

        filtered_data = [
            entry for entry in user_data 
            if datetime.fromtimestamp(entry['date'].timestamp()) >= time_24_hours_ago
        ]

        print(f"filtered_data: {filtered_data}")
        users = [self.get_user_by_email(entry['email']) for entry in filtered_data]
        print(f"users: {users}")
        filtered_users = [user for user in users if user is not None]

        user_answers = [[user['relationship_goals'], user['affection_expression'], user['free_time'], user['motivation'], user['communication_style']] for user in filtered_users]
        user_embeddings = self.answers_to_embeddings(user_answers)

        if len(user_embeddings) < 2:
            print("returned None")
            return None
        else:
            i, j = self.find_max_similarity(user_embeddings)
            if i < 0 or j < 0 or i >= len(filtered_users) or j >= len(filtered_users):
                print("returned None")
                return None
            
            return (filtered_users[i], filtered_users[j])
 
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

