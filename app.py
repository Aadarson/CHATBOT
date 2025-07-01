from flask import Flask, request, jsonify, send_from_directory
import openai

app = Flask(__name__)

# 🔐 OpenRouter API Setup
openai.api_key = "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"
openai.api_base = "https://openrouter.ai/api/v1"

# 📄 Serve the chatbot HTML
@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

# 💬 Handle chat messages
@app.route('/chat', methods=['POST'])
def chat():
    user_msg = request.json.get("message", "").strip()

    if not user_msg:
        return jsonify({'reply': "❗ Please enter a message."})

    try:
        # 🌐 Call OpenRouter LLM (change model if needed)
        response = openai.ChatCompletion.create(
            model="mistralai/mistral-7b-instruct",  # or try: meta-llama/llama-3-8b-instruct
            messages=[
                {"role": "system", "content": "You are AskMe AI, a smart assistant that answers user questions clearly and concisely."},
                {"role": "user", "content": user_msg}
            ],
            temperature=0.7,
            max_tokens=300
        )

        reply = response.choices[0].message.content.strip()
        print(f"✅ OpenRouter reply: {reply}")
        return jsonify({'reply': reply})

    except Exception as e:
        print(f"❌ OpenRouter error: {e}")
        return jsonify({'reply': f"⚠️ AI error: {e}"})  # Show full error in browser for debugging

# 🚀 Start Flask server
if __name__ == '__main__':
    app.run(debug=True)
