from flask import Flask, render_template, request, session, redirect, url_for
from src.analyzer import calculate_similarity
from src.interview_analyzer import extract_keywords, analyze_interview
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

BEHAVIORAL_QUESTIONS = [
    "Tell me about a time you had to handle a difficult stakeholder.",
    "Describe a challenging project you worked on and how you handled it.",
    "What are your long-term career goals?",
    "How do you handle pressure or stressful situations?",
    "Why should we hire you?"
]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        session['resume_text'] = request.form.get('resume')
        session['jd_text'] = request.form.get('job_description')
        
        if session['resume_text'] and session['jd_text']:
            score = calculate_similarity(session['resume_text'], session['jd_text'])
            
            feedback = ""
            if score > 0.5:
                feedback = "Excellent fit! Your resume strongly aligns with the job description."
            elif score > 0.3:
                feedback = "Good fit. There's a solid overlap between your skills and the job requirements."
            else:
                feedback = "Needs improvement. Consider tailoring your resume with more keywords."
            
            session['resume_feedback'] = feedback
            session['resume_score'] = round(score, 2)
            
            return redirect(url_for('coach_dashboard'))

    return render_template('index.html')

@app.route('/coach')
def coach_dashboard():
    return render_template(
        'coach_dashboard.html',
        resume_score=session.get('resume_score'),
        resume_feedback=session.get('resume_feedback')
    )

def generate_questions(job_description):
    jd_keywords = extract_keywords(job_description, top_n=3)
    technical_questions = [
        "Can you describe your experience with {kw}?",
        "Tell me about a project where you used {kw}.",
        "How would you approach a task involving {kw}?"
    ]
    
    questions = BEHAVIORAL_QUESTIONS[:2]
    
    for i, keyword in enumerate(jd_keywords):
        if i < len(technical_questions):
            questions.append(technical_questions[i].format(kw=keyword))
            
    questions.append(BEHAVIORAL_QUESTIONS[2])
    return questions

@app.route('/chatbot', methods=['GET', 'POST'])
def chatbot():
    if 'jd_text' not in session:
        return redirect(url_for('index'))

    if 'questions' not in session:
        session['questions'] = generate_questions(session['jd_text'])
        session['question_index'] = 0
        session['chat_history'] = [{'speaker': 'bot', 'message': session['questions'][0]}]
        session['interview_finished'] = False
        session['feedback_report'] = None

    if request.method == 'POST' and not session.get('interview_finished'):
        user_answer = request.form.get('answer')
        if user_answer:
            session['chat_history'].append({'speaker': 'user', 'message': user_answer})
            session['question_index'] += 1
            
            if session['question_index'] < len(session['questions']):
                next_question = session['questions'][session['question_index']]
                session['chat_history'].append({'speaker': 'bot', 'message': next_question})
            else:
                session['interview_finished'] = True
                jd_keywords = extract_keywords(session['jd_text'])
                feedback_report = analyze_interview(session['chat_history'], jd_keywords)
                session['feedback_report'] = feedback_report
                
                final_message = "That's all the questions for now. Here is your feedback report:"
                session['chat_history'].append({'speaker': 'bot', 'message': final_message})

    session.modified = True
    return render_template(
        'chatbot.html', 
        chat_history=session.get('chat_history', []),
        feedback_report=session.get('feedback_report'),
        interview_finished=session.get('interview_finished')
    )

@app.route('/reset')
def reset_session():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)