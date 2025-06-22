import spacy
from textblob import TextBlob
import re

nlp = spacy.load("en_core_web_sm", disable=['parser', 'ner'])

def extract_keywords(text, top_n=10):
    doc = nlp(text.lower())
    keywords = [
        token.lemma_
        for token in doc
        if not token.is_stop and not token.is_punct and token.pos_ in ['NOUN', 'PROPN', 'ADJ']
    ]
    
    from collections import Counter
    keyword_freq = Counter(keywords)
    return [kw for kw, _ in keyword_freq.most_common(top_n)]

def analyze_interview(chat_history, job_description_keywords):
    feedback = {
        "strengths": [],
        "weaknesses": [],
        "keyword_coverage": 0,
        "overall_sentiment": 0
    }
    
    user_answers = [entry['message'] for entry in chat_history if entry['speaker'] == 'user']
    if not user_answers:
        return feedback
        
    full_transcript = " ".join(user_answers)
    
    mentioned_keywords = {
        kw for kw in job_description_keywords if kw in full_transcript.lower()
    }
    feedback["keyword_coverage"] = round((len(mentioned_keywords) / len(job_description_keywords)) * 100) if job_description_keywords else 100

    if feedback["keyword_coverage"] > 70:
        feedback["strengths"].append("Excellent use of relevant keywords from the job description.")
    elif feedback["keyword_coverage"] > 40:
        feedback["strengths"].append("Good alignment with job description keywords.")
    else:
        feedback["weaknesses"].append("Could better align answers with keywords from the job description.")

    star_words = ['situation', 'task', 'action', 'result', 'example', 'achieved', 'managed', 'led']
    star_mentions = [word for word in star_words if word in full_transcript.lower()]
    if len(star_mentions) > 2:
        feedback["strengths"].append("Demonstrated use of specific examples and action-oriented language (STAR method).")
    else:
        feedback["weaknesses"].append("Answers could be strengthened by providing more specific examples using the STAR method (Situation, Task, Action, Result).")

    avg_answer_length = sum(len(answer.split()) for answer in user_answers) / len(user_answers)
    if avg_answer_length < 20:
        feedback["weaknesses"].append("Answers were very brief. Try to elaborate more on your experiences.")
    elif avg_answer_length > 150:
        feedback["weaknesses"].append("Answers were quite long. Aim for concise yet comprehensive responses.")

    blob = TextBlob(full_transcript)
    feedback["overall_sentiment"] = round(blob.sentiment.polarity, 2)
    if feedback["overall_sentiment"] > 0.2:
        feedback["strengths"].append("Maintained a positive and confident tone throughout the interview.")
    
    return feedback