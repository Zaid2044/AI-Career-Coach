# src/analyzer.py

import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load the spaCy model we downloaded
# We disable 'parser' and 'ner' to make it faster as we only need word vectors and lemmas.
nlp = spacy.load("en_core_web_sm", disable=['parser', 'ner'])

def preprocess_text(text):
    """
    Cleans and tokenizes the input text.
    - Removes stopwords (common words like 'the', 'is')
    - Lemmatizes words (reduces them to their base form, e.g., 'running' -> 'run')
    """
    doc = nlp(text.lower())
    processed_tokens = [
        token.lemma_ for token in doc if not token.is_stop and not token.is_punct
    ]
    return " ".join(processed_tokens)

def calculate_similarity(resume_text, job_description_text):
    """
    Calculates the cosine similarity between a resume and a job description.
    Returns a score between 0 and 1.
    """
    # Preprocess both texts
    processed_resume = preprocess_text(resume_text)
    processed_jd = preprocess_text(job_description_text)
    
    # Create a list of the two documents to vectorize
    text_corpus = [processed_resume, processed_jd]
    
    # Use TF-IDF Vectorizer to convert text into numerical vectors
    # TF-IDF gives more weight to words that are important to a document
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(text_corpus)
    
    # Calculate the cosine similarity between the two vectors
    # The result is a 2x2 matrix; we want the value at [0, 1]
    similarity_matrix = cosine_similarity(tfidf_matrix)
    similarity_score = similarity_matrix[0][1]
    
    return similarity_score

# --- Main execution block to test the functionality ---
if __name__ == "__main__":
    try:
        # Load the sample files
        with open('data/sample_resume.txt', 'r', encoding='utf-8') as f:
            resume = f.read()
        
        with open('data/sample_jd.txt', 'r', encoding='utf-8') as f:
            job_description = f.read()
            
        # Calculate the similarity
        score = calculate_similarity(resume, job_description)
        
        # Print the result
        print("--- Resume to Job Description Fit Analysis ---")
        print(f"Similarity Score: {score:.2f}")
        
        # Give some basic feedback based on the score
        if score > 0.5:
            print("Feedback: Excellent fit! The resume keywords strongly match the job description.")
        elif score > 0.3:
            print("Feedback: Good fit. The resume shows relevant skills for the job.")
        else:
            print("Feedback: Needs improvement. Consider tailoring your resume with more keywords from the job description.")
            
    except FileNotFoundError:
        print("Error: Make sure 'sample_resume.txt' and 'sample_jd.txt' are in the 'data' folder.")