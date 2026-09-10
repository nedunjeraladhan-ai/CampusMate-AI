from flask import Flask, render_template, request, jsonify
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

app = Flask(__name__)

# Get API key
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("ERROR: GEMINI_API_KEY not found in .env file")

client = genai.Client(api_key=api_key)


SYSTEM_PROMPT = """
You are CampusMate AI.

You are a domain-specific chatbot for
Sir Issac Newton Arts and Science College, Nagapattinam.

You must answer ONLY questions related to:
- Sir Issac Newton College
- Courses
- Departments
- Admission
- Campus
- Facilities
- Faculty
- Student activities
- College events
- Contact information
- College location
- General college information

For unrelated questions, reply:
"Sorry, I can answer only questions related to
Sir Issac Newton College, Nagapattinam."

Do not invent information.
If you don't know something, say:
"I don't have that information right now."

Keep answers simple and helpful.
"""


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():

    data = request.get_json()
    user_message = data.get("message", "").strip()

    if not user_message:
        return jsonify({
            "reply": "Please enter a question."
        })

    try:

        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=SYSTEM_PROMPT + "\n\nUser: " + user_message
        )

        return jsonify({
            "reply": response.text
        })

    except Exception as e:

        print("Gemini Error:", e)

        return jsonify({
            "reply": "Gemini API Error. Please check your API key and terminal message."
        })


if __name__ == "__main__":
    app.run(debug=True)
    
