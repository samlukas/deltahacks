import cohere_scripts
import numpy as np
import os

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

def create_embeddings():
    co = cohere_scripts.Client(api_key=os.environ.get("COHERE"))
    
    embedding_matrix = []
    model = "embed-english-v3.0"
    input_type = "search_query"

    q1 = "What are your relationship goals?:"
    ans1 = [
        q1 + "Looking for something short-term",
        q1 + "Looking for a long-term relationship",
        q1 + "Just here to have fun",
        q1 + "Still figuring things out"
    ]

    res = co.embed(
        texts=ans1,
        model=model,
        input_type=input_type,
        embedding_types=["float"],
    )

    embedding_matrix.append(res.embeddings.float)

    q2 = "How do you usually express affection?:"
    ans2 = [
        q2 + "I express my love through physical touch",
        q2 + "I show I care by giving thoughtful gifts",
        q2 + "I value spending quality time together",
        q2 + "I express my feelings through words of encouragement"
    ]

    res = co.embed(
        texts=ans2,
        model=model,
        input_type=input_type,
        embedding_types=["float"],
    )

    embedding_matrix.append(res.embeddings.float)

    q3 = "How do you approach your free time?:"
    ans3 = [
        q3 + "I like to plan my activities in advance",
        q3 + "I prefer to be spontaneous and flexible",
        q3 + "I enjoy staying active with various activities",
        q3 + "I value my alone time to recharge"
    ]

    res = co.embed(
        texts=ans3,
        model=model,
        input_type=input_type,
        embedding_types=["float"],
    )

    embedding_matrix.append(res.embeddings.float)

    q4 = "What motivates you the most?:"
    ans4 = [
        q4 + "Setting and achieving personal goals",
        q4 + "Making a positive impact on others",
        q4 + "Discovering new experiences and adventures",
        q4 + "Being acknowledged for my accomplishments"
    ]

    res = co.embed(
        texts=ans4,
        model=model,
        input_type=input_type,
        embedding_types=["float"],
    )

    embedding_matrix.append(res.embeddings.float)

    q5 = "What's your communication style?:"
    ans5 = [
        q5 + "I communicate in a clear and straightforward way",
        q5 + "I focus on understanding others' feelings",
        q5 + "I keep conversations fun and casual",
        q5 + "I take time to consider before responding"
    ]

    res = co.embed(
        texts=ans5,
        model=model,
        input_type=input_type,
        embedding_types=["float"],
    )

    embedding_matrix.append(res.embeddings.float)

    return embedding_matrix

def calculate_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
