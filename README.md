# Binge: Meet and Eat

<kbd>![alt text](extension/icon128.png)</kbd>

## Overview

Binge is a web application with a Chrome extension agent that allows users to create profiles, save their favorite restaurants, and find potential matches based on shared interests and preferences. The application provides a seamless user experience across both the web and the Chrome extension.

## Features

- **Profile Management**: Users can create and manage their profiles.
- **Restaurant Management**: Save and manage favorite restaurants based on Google Maps listings.
- **Matching System**: Find potential matches based on user preferences and interests.
- **Email Notifications**: Users receive email notifications when matched with another user.
- **Chrome Extension**: A browser extension that allows users to easily save restaurants while browsing.
- **Responsive Design**: Optimized for both mobile and desktop devices.

## Technologies Used

- **Backend**: Flask
- **Frontend**: HTML, CSS, JavaScript (jQuery)
- **Database**: Custom database implementation (db.py)
- **Natural Language Processing**: Cohere for generating personalized messages
- **Email Service**: SMTP for sending emails
- **Chrome Extension**: JavaScript for the extension functionality
- **Environment Variables**: dotenv for managing sensitive information

## User Profile Embeddings and Similarity Score Calculations

Cohere is used in the Binge application to create embeddings for user responses and calculate similarity scores between users. Here’s how it works:

### Creating Embeddings

1. **Embedding Generation**:
   - The `create_embeddings` function in `cohere_scripts.py` generates embeddings for various user responses related to relationship goals, affection expression, free time approach, motivation, and communication style.
   - Each response is embedded into a vector representation using Cohere's embedding model. This allows for a numerical representation of qualitative data, making it easier to compare user preferences.

2. **Embedding Structure**:
   - The embeddings are stored in a 3D NumPy array, where each dimension corresponds to a different question and its possible answers. This structure allows for efficient similarity calculations later on.

### Calculating Similarity Scores

1. **Cosine Similarity Calculation**:
   - The `calculate_similarity` function takes two vectors (representing two users' responses) as input.
   - It flattens the vectors to ensure they are one-dimensional and then calculates the cosine similarity between them.
   - Cosine similarity is a measure of similarity between two non-zero vectors, defined as the cosine of the angle between them. It is computed using the dot product of the vectors divided by the product of their magnitudes.

2. **Return Similarity Score**:
   - The function returns a scalar value representing the similarity score, which ranges from -1 (completely dissimilar) to 1 (identical).
   - A higher similarity score indicates that the users have more in common based on their responses.

### Example Code Snippet for Cohere Integration

Here’s a simplified version of the relevant code from `cohere_scripts.py`:

```python
def create_embeddings():
    # Generate embeddings for user responses
    # (Implementation details omitted for brevity)
    return embedding_matrix

def calculate_similarity(a, b):
    # Calculate cosine similarity between two vectors
    a_array = np.array(a)
    b_array = np.array(b)
    
    # Ensure vectors are 1-dimensional
    a_flat = a_array.flatten()
    b_flat = b_array.flatten()
    
    # Calculate cosine similarity
    similarity = np.dot(a_flat, b_flat) / (np.linalg.norm(a_flat) * np.linalg.norm(b_flat))
    
    return float(similarity)
```

## Getting Started

### Prerequisites

- Python 3.x
- Flask
- Flask-CORS
- dotenv
- jQuery

### Accessing the Program

Binge Web Page can be accessed at `http://www.bingeeating.study` or `https://deltahacks-git-main-sams-projects-71d5eb04.vercel.app/`.

## Chrome Extension Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/binge.git
   cd binge
   ```
2. Navigate to the `extension` directory in your cloned repository.
3. Open Chrome and go to `chrome://extensions/`.
4. Enable "Developer mode" in the top right corner.
5. Click on "Load unpacked" and select the `extension` directory.
6. The Binge extension should now be installed and ready to use.

## Usage

- **Login**: Click on the "Login" button to login to existing account.
- **Signup**: Create a new account by filling out the signup form and the questionaire.
- **Profile**: After logging in, you can view and edit your profile, including your saved restaurants.
- **Restaurant Matching**: Use the restaurant matching feature to find potential matches based on your preferences.
- **Email Notifications**: Users receive email notifications when matched with another user.
- **Chrome Extension**: Use the extension to save restaurants directly from your browser when restaurant is searched on Google Maps.

## Acknowledgments

- [Flask](https://flask.palletsprojects.com/) for the web framework.
- [Cohere](https://cohere.ai/) for natural language processing capabilities, embeddings score and similarity score calculations.
- [SMTP](https://docs.python.org/3/library/smtplib.html) for sending emails.
