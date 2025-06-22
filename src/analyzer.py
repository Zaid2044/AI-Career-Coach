import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nlp = spacy.load("en_core_web_sm", disable=['parser', 'ner'])

def preprocess_text(text):
    doc = nlp(text.lower())
    processed_tokens = [
        token.lemma_ for token in doc if not token.is_stop and not token.is_punct
    ]
    return " ".join(processed_tokens)

def calculate_similarity(resume_text, job_description_text):
    processed_resume = preprocess_text(resume_text)
    processed_jd = preprocess_text(job_description_text)
    
    text_corpus = [processed_resume, processed_jd]
    
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(text_corpus)
    
    similarity_matrix = cosine_similarity(tfidf_matrix)
    similarity_score = similarity_matrix[0][1]
    
    return similarity_score

if __name__ == "__main__":
    try:
        with open('data/sample_resume.txt', 'r', encoding='utf-8') as f:
            resume = f.read()
        
        with open('data/sample_jd.txt', 'r', encoding='utf-8') as f:
            job_description = f.read()
            
        score = calculate_similarity(resume, job_description)
        
        print("--- Resume to Job Description Fit Analysis ---")
        print(f"Similarity Score: {score:.2f}")
        
        if score > 0.5:
            print("Feedback: Excellent fit! The resume keywords strongly match the job description.")
        elif score > 0.3:
            print("Feedback: Good fit. The resume shows relevant skills for the job.")
        else:
            print("Feedback: Needs improvement. Consider tailoring your resume with more keywords from the job description.")
            
    except FileNotFoundError:
        print("Error: Make sure 'sample_resume.txt' and 'sample_jd.txt' are in the 'data' folder.")