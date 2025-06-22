# 🤖 AI Career Coach

A sophisticated, multi-stage web application designed to be a personal career assistant. This tool leverages Natural Language Processing (NLP) and Generative AI to provide users with a comprehensive suite of tools for their job search, from initial resume screening to in-depth, AI-driven interview practice.

This project demonstrates an end-to-end development lifecycle, including core NLP logic, advanced AI integration via APIs, a stateful web application backend, and a polished, modern user interface.

---

## ✨ Key Features

-   **Resume-to-Job-Description Analysis:**
    -   Calculates a "fit score" using **TF-IDF Vectorization** and **Cosine Similarity** to quantify how well a resume aligns with a specific job description.
    -   Provides instant feedback on the strength of the alignment.

-   **Intelligent Interview Chatbot:**
    -   **Dynamic Question Generation:** Creates a unique set of interview questions by combining standard behavioral questions with technical questions derived directly from keywords extracted from the job description.
    -   **Generative AI Feedback:** Utilizes the **Google Gemini API** to provide real-time, human-like feedback on each of the user's answers. The AI analyzes strengths, weaknesses, and relevance to the role.
    -   **Final Performance Summary:** After the interview, it calculates an overall "Fit Score" and provides a summary of the user's performance, highlighting whether they are a strong fit or need improvement.

-   **Modern Web Interface:**
    -   A clean, multi-page web application built with **Flask**.
    -   Uses server-side sessions to maintain user context across the resume analysis and chatbot stages.
    -   A responsive and aesthetically pleasing UI built with modern HTML and CSS.

---

## 🛠️ Technology Stack

-   **Backend:** Python, Flask
-   **Core NLP:** spaCy, Scikit-learn
-   **Generative AI:** Google Gemini Pro (via `google-generativeai` SDK)
-   **Frontend:** HTML5, CSS3
-   **Supporting Libraries:** python-dotenv, TextBlob

---

## 🚀 Getting Started

Follow these instructions to get the project running on your local machine.

### Prerequisites

-   Python 3.9+
-   Git
-   A **Google AI API Key**.

### Installation

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/Zaid2044/AI-Career-Coach.git
    cd AI-Career-Coach
    ```

2.  **Create and activate a Python virtual environment:**
    ```bash
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    ```

3.  **Install the required dependencies:**
    ```bash
    pip install flask spacy scikit-learn textblob google-generativeai python-dotenv
    ```

4.  **Download the spaCy language model:**
    ```bash
    python -m spacy download en_core_web_sm
    ```

5.  **Set up your API Key:**
    -   Create a file named `.env` in the root of the project directory.
    -   Add your Google AI API key to the file like this:
        ```
        GOOGLE_API_KEY=YOUR_API_KEY_HERE
        ```
    -   **Important:** The `.gitignore` file is configured to prevent the `.env` file from being uploaded.

---

## ⚡ Usage

To run the main web application, execute the `app.py` script from the project root:

```bash
python app.py
```
    -   The server will start, typically on http://127.0.0.1:5000.
    -   Open this URL in your web browser to begin.

## Workflow:

1. Homepage: Paste a resume and a job description into the text areas and click "Analyze and Start Coaching".
2. Dashboard: View your initial resume-fit score and feedback. Click "Start Interview Practice".
3. Chatbot: Answer the series of dynamically generated questions. After each answer, you will receive real-time feedback from the Gemini AI.
4. Final Report: Once all questions are answered, a final summary of your overall performance will be displayed.