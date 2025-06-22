import os
import google.generativeai as genai
from dotenv import load_dotenv
import json

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("ERROR: GOOGLE_API_KEY environment variable not found.")
    print("Please create a .env file and add your key: GOOGLE_API_KEY=your_key_here")
    genai.configure(api_key="NO_KEY")
else:
    genai.configure(api_key=api_key)

generation_config = {
    "temperature": 0.7,
    "top_p": 1,
    "top_k": 1,
    "max_output_tokens": 2048,
}

safety_settings = [
    {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
    {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
]

# The only change is on the line below
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash-latest",
    generation_config=generation_config,
    safety_settings=safety_settings
)

def get_ai_feedback(job_description, question, answer):
    if not answer or not answer.strip():
        return {
            "strengths": ["No answer was provided."],
            "weaknesses": ["Please provide a response to the question."],
            "suitability_score": 0.0
        }

    try:
        prompt = f"""
        You are an expert career coach conducting a practice interview.
        Your task is to provide feedback on a candidate's answer.

        **Job Description Context:**
        ---
        {job_description}
        ---

        **Interview Question:**
        "{question}"

        **Candidate's Answer:**
        "{answer}"

        **Your Instructions:**
        Analyze the candidate's answer based on the job description and the question asked.
        Provide concise, constructive feedback.
        Identify specific strengths and areas for improvement.
        Your entire response MUST be in a valid JSON format, like this example:
        {{
            "strengths": [
                "A clear and concise strength found in the answer.",
                "Another positive point observed."
            ],
            "weaknesses": [
                "A specific area where the answer could be improved.",
                "A suggestion for a better approach."
            ],
            "suitability_score": 0.8
        }}
        The suitability_score should be a float between 0.0 (very poor fit) and 1.0 (excellent fit) for this specific question.
        Do not include any text or formatting outside of the JSON structure.
        """
        
        response = model.generate_content(prompt)
        
        if not response.parts:
            print(f"ERROR: AI response was blocked. Reason: {response.prompt_feedback.block_reason.name}")
            raise ValueError("Blocked by safety filters")

        cleaned_response = response.text.strip().replace("```json", "").replace("```", "")
        feedback_json = json.loads(cleaned_response)
        return feedback_json

    except Exception as e:
        print(f"An error occurred while getting AI feedback: {e}")
        return {
            "strengths": ["Could not generate AI feedback due to an error."],
            "weaknesses": [f"Please try again. The server reported: {e}"],
            "suitability_score": 0.0
        }