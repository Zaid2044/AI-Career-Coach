from flask import Flask, render_template, request, session
from src.analyzer import calculate_similarity
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

INTERVIEW_QUESTIONS = [
    "Tell me about yourself.",
    "What are your biggest strengths?",
    "What is your biggest weakness?",
    "Where do you see yourself in five years?",
    "Why do you want to work for this company?"
]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        resume_text = request.form.get('resume')
        jd_text = request.form.get('job_description')
        
        if resume_text and jd_text:
            score = calculate_similarity(resume_text, jd_text)
            
            feedback = ""
            if score > 0.5:
                feedback = "Excellent fit! The resume keywords strongly match the job description."
            elif score > 0.3:
                feedback = "Good fit. The resume shows relevant skills for the job."
            else:
                feedback = "Needs improvement. Consider tailoring your resume with more keywords from the job description."
                
            return render_template('index.html', score=round(score, 2), feedback=feedback, resume=resume_text, jd=jd_text)

    return render_template('index.html', score=None, feedback=None)

@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    if 'question_index' not in session or 'chat_history' not in session:
        session['question_index'] = 0
        session['chat_history'] = []
        session['chat_history'].append({'speaker': 'bot', 'message': INTERVIEW_QUESTIONS[0]})

    if request.method == 'POST':
        user_answer = request.form.get('answer')
        if user_answer:
            session['chat_history'].append({'speaker': 'user', 'message': user_answer})
            
            session['question_index'] += 1
            
            if session['question_index'] < len(INTERVIEW_QUESTIONS):
                next_question = INTERVIEW_QUESTIONS[session['question_index']]
                session['chat_history'].append({'speaker': 'bot', 'message': next_question})
            else:
                session['chat_history'].append({'speaker': 'bot', 'message': "That's all the questions for now. Great practice!"})

    session.modified = True
    return render_template('chatbot.html', chat_history=session.get('chat_history', []))

@app.route('/chatbot/reset')
def reset_chatbot():
    session.pop('question_index', None)
    session.pop('chat_history', None)
    return "<p>Chatbot session reset. Please <a href='/chatbot'>return to the chatbot</a>.</p>"


if __name__ == '__main__':
    app.run(debug=True)