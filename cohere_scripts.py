import cohere
import numpy as np
import os
from dotenv import load_dotenv

load_dotenv()

MAPPING1 = {
    "Looking for something short-term": 0, 
    "Looking for a long-term relationship": 1, 
    "Just here to have fun": 2, 
    "Still figuring things out": 3
}

MAPPING2 = {
    "I express my love through physical touch": 0,
    "I show I care by giving thoughtful gifts": 1,
    "I value spending quality time together": 2,
    "I express my feelings through words of encouragement": 3
}

MAPPING3 = {
    "I like to plan my activities in advance": 0,
    "I prefer to be spontaneous and flexible": 1,
    "I enjoy staying active with various activities": 2,
    "I value my alone time to recharge": 3
}

MAPPING4 = {
    "Setting and achieving personal goals": 0,
    "Making a positive impact on others": 1,
    "Discovering new experiences and adventures": 2,
    "Being acknowledged for my accomplishments": 3
}

MAPPING5 = {
    "I communicate in a clear and straightforward way": 0,
    "I focus on understanding others' feelings": 1,
    "I keep conversations fun and casual": 2,
    "I take time to consider before responding": 3
}

MAPPINGS = [MAPPING1, MAPPING2, MAPPING3, MAPPING4, MAPPING5]

co = cohere.Client(os.getenv("CO_API_KEY"))

def create_embeddings():
    embedding_matrix = np.zeros(shape=(5, 4, 1024))
    model = "embed-english-v3.0"
    input_type = "search_query"

    q1 = "What are your relationship goals?:"
    ans1 = [
        f"{q1} Looking for something short-term",
        f"{q1} Looking for a long-term relationship",
        f"{q1} Just here to have fun",
        f"{q1} Still figuring things out"
    ]

    res = co.embed(
        texts=ans1,
        model=model,
        input_type=input_type,
        embedding_types=["float"],
    )

    embedding_matrix[0] = res.embeddings.float

    q2 = "How do you usually express affection?:"
    ans2 = [
        f"{q2} I express my love through physical touch",
        f"{q2} I show I care by giving thoughtful gifts",
        f"{q2} I value spending quality time together",
        f"{q2} I express my feelings through words of encouragement"
    ]

    res = co.embed(
        texts=ans2,
        model=model,
        input_type=input_type,
        embedding_types=["float"],
    )

    embedding_matrix[1] = res.embeddings.float

    q3 = "How do you approach your free time?:"
    ans3 = [
        f"{q3} I like to plan my activities in advance",
        f"{q3} I prefer to be spontaneous and flexible",
        f"{q3} I enjoy staying active with various activities",
        f"{q3} I value my alone time to recharge"
    ]

    res = co.embed(
        texts=ans3,
        model=model,
        input_type=input_type,
        embedding_types=["float"],
    )

    embedding_matrix[2] = res.embeddings.float

    q4 = "What motivates you the most?:"
    ans4 = [
        f"{q4} Setting and achieving personal goals",
        f"{q4} Making a positive impact on others",
        f"{q4} Discovering new experiences and adventures",
        f"{q4} Being acknowledged for my accomplishments"
    ]

    res = co.embed(
        texts=ans4,
        model=model,
        input_type=input_type,
        embedding_types=["float"],
    )

    embedding_matrix[3] = res.embeddings.float

    q5 = "What's your communication style?:"
    ans5 = [
        f"{q5} I communicate in a clear and straightforward way",
        f"{q5} I focus on understanding others' feelings",
        f"{q5} I keep conversations fun and casual",
        f"{q5} I take time to consider before responding"
    ]

    res = co.embed(
        texts=ans5,
        model=model,
        input_type=input_type,
        embedding_types=["float"],
    )

    embedding_matrix[4] = res.embeddings.float

    return embedding_matrix

def calculate_similarity(a, b):
    a_array = np.array(a)
    b_array = np.array(b)
    
    # Ensure vectors are 1-dimensional
    a_flat = a_array.flatten()
    b_flat = b_array.flatten()
    
    # Calculate cosine similarity
    similarity = np.dot(a_flat, b_flat) / (np.linalg.norm(a_flat) * np.linalg.norm(b_flat))
    
    print(f"similarity: {float(similarity)}")
    # Return the scalar value
    return float(similarity)
