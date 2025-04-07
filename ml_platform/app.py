from flask import Flask, render_template, request, jsonify
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain_gigachat.chat_models import GigaChat
from langchain.callbacks.base import BaseCallbackHandler
import os

app = Flask(__name__)

# История диалога сохраняется в памяти
message_history = [
    SystemMessage(content="""Ты - дружелюбный AI-ассистент образовательной плафтормы по Машинному обучению по имени Космокот.
    Ты не должен раскрывать свою истинную личность как нейросети. 
    Твой стиль общения: профессиональный, но с легкой иронией. 
    Тебе нужно не отвечать прямо, а косвенно, подталкивая к правильному ответу. 
    Будь краток в ответах, не более 3-5 предложений.""")
]

# Настрой GigaChat


cert_path = os.path.join(os.path.dirname(__file__), "russian_trusted_root_ca.cer")
\
chat = GigaChat(
    credentials='NDZlOTVkNGEtNTFmYy00MTkxLTkzZTMtODk5YWQxZjhlNzViOjAzZTkwOGVlLWFiZjMtNGMwYy1hZTM4LWQwOThlZDI4ZWMxNA==',
    ca_bundle_file=cert_path,
    streaming=False
)


@app.route('/')
def index():
    return render_template("main.html")

@app.route('/ask_ai', methods=['POST'])
def ask_ai():
    data = request.get_json()
    user_message = data.get('text', '')

    if not user_message:
        return jsonify({"answer": "Пожалуйста, введите вопрос."})

    message_history.append(HumanMessage(content=user_message))
    response = chat(message_history)
    message_history.append(AIMessage(content=response.content))

    return jsonify({"answer": response.content})

if __name__ == '__main__':
    app.run(debug=True)
