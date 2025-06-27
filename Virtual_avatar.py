from flask import request, jsonify, Blueprint
import google.generativeai as genai
from dotenv import load_dotenv
import os
import json

virtual_avatar_bp = Blueprint('virtual_avatar', __name__)

load_dotenv()

with open("database.json", "r", encoding="utf-8") as f:
    user_database = json.load(f)

def format_context(data):
    context_parts = []
    def traverse(d, prefix=""):
        for key, value in d.items():
            new_prefix = f"{prefix} > {key}" if prefix else key
            if isinstance(value, dict):
                traverse(value, new_prefix)
            elif isinstance(value, list):
                context_parts.append(f"{new_prefix}: {', '.join(map(str, value))}")
            else:
                context_parts.append(f"{new_prefix}: {value}")
    traverse(data)
    return "\n".join(context_parts)

context_string = format_context(user_database)

genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel(model_name='gemini-1.5-flash')

def generate_response(user_query):
    try:
        prompt = f"""
                You are a friendly, emoji-using AI assistant and the virtual avatar of Siddharth Pratap Singh.

                You have full access to his professional database, which includes his skills, projects, goals, and current learning journey.

                Here is his data:
                {context_string}

                Your job is to answer *any* questions a user may have — whether they are about Siddharth’s professional life (like “What projects has he built?”), his experience, his tech stack, or casual questions (like “Tell me a joke”, “What inspires you?”, “Say something motivating”, or “Are you real?”).

                ✅ Be warm, clear, and concise.  
                ✅ Use 1–3 well-placed emojis to keep the tone light and engaging.  
                ✅ Keep answers accurate when responding based on the data, and creative when asked general/fun questions.  
                ✅ If a question doesn’t relate to Siddharth or the database, feel free to improvise like a helpful virtual buddy.

                User Query: {user_query}
                """
        response = model.generate_content(
            prompt,
            generation_config={
                "max_output_tokens": 1000,
                "temperature": 0.5,
                "top_p": 0.95,
                "top_k": 40
            }
        )
        return response
    except Exception as e:
        return f"Error generating response: {str(e)}"

@virtual_avatar_bp.route('/virtual-avatar-chat', methods=['POST'])
def chat():
    data = request.get_json()
    user_message = data.get('message', '')
    if not user_message:
        return jsonify({'error': 'No message provided'}), 400
    response = generate_response(user_message)
    if isinstance(response, str):
        # This is an error message
        return jsonify({'reply': response})
    else:
        return jsonify({'reply': response.text})