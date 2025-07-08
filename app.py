from flask import Flask, request, jsonify, send_from_directory
from openai import OpenAI

app = Flask(__name__)

# 🔐 OpenRouter API Setup
client = OpenAI(
    api_key="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",
    base_url="https://openrouter.ai/api/v1"
)

# 🧠 Global memory (temporary per session)
chat_history = []
user_name = None

# ✅ System prompt with placeholder for dynamic name
def get_system_prompt():
    global user_name
    base = (
        "You are Zack, a highly intelligent, emotionally aware AI assistant. "
        "You adapt to the user's tone—professional or casual. "
        "Avoid repeating, connect your replies with context from previous conversation. "
        "Be concise and helpful."
    )
    if user_name:
        base += f" The user's name is {user_name}. Address them by name in a friendly way."
    else:
        base += " Ask for the user's name if it hasn't been provided yet."
    return {"role": "system", "content": base}

# 📄 Serve frontend
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# 💬 Chat route
@app.route('/chat', methods=['POST'])
def chat():
    global chat_history, user_name

    user_msg = request.json.get("message", "").strip()
    if not user_msg:
        return jsonify({'reply': "❗ Please enter a message."})

    # Detect and extract user name (very basic method)
    if "my name is" in user_msg.lower():
        possible_name = user_msg.lower().split("my name is")[-1].strip().split()[0].capitalize()
        if possible_name.isalpha():
            user_name = possible_name

    # (Re)build the conversation starting with updated system prompt
    messages = [get_system_prompt()] + chat_history
    messages.append({"role": "user", "content": user_msg})

    try:
        response = client.chat.completions.create(
            model="meta-llama/llama-3-8b-instruct",  # or mistralai/mistral-7b-instruct
            messages=messages,
            temperature=0.7,
            max_tokens=350
        )

        reply = response.choices[0].message.content.strip()

        # Store the conversation
        chat_history.append({"role": "user", "content": user_msg})
        chat_history.append({"role": "assistant", "content": reply})

        print(f"✅ Zack reply: {reply}")
        return jsonify({'reply': reply})

    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({'reply': f"⚠️ Zack ran into a problem: {e}"})


# 🔄 Optional: Clear history + forget name
@app.route('/clear', methods=['POST'])
def clear():
    global chat_history, user_name
    chat_history = []
    user_name = None
    return jsonify({'status': 'Zack memory cleared.'})


# 🚀 Run server
if __name__ == '__main__':
    app.run(debug=True)
