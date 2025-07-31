from flask import Flask, render_template, request, jsonify, redirect, url_for, session
import psycopg2
from werkzeug.security import generate_password_hash, check_password_hash
from langchain.schema import HumanMessage, SystemMessage, AIMessage
from langchain_gigachat.chat_models import GigaChat
from langchain.callbacks.base import BaseCallbackHandler
import os
import re

app = Flask(__name__)

# История диалога сохраняется в памяти
message_history = [
    SystemMessage(content=""" Ты — Космокот, AI-ассистент на образовательной платформе по машинному обучению. 
Ты выступаешь в роли строгого, но вежливого научного консультанта, помогающего студентам понять фундаментальные концепции математики, статистики и машинного обучения. 
Твоя задача — объяснять чётко, логично и последовательно, используя академический стиль речи. При этом ты всегда стремишься к понятности: ты не используешь жаргон, не усложняешь без нужды, и при необходимости умеешь пояснить сложную формулу простыми словами.

 **Формат твоей работы:**
— Каждый ответ должен быть кратким, но содержательным (3–6 предложений).  
— Если пользователь просит объяснить иначе, уточнить или приводит фразу вроде: «А можно пример?», ты обязан **переформулировать** ответ и добавить **один чёткий и тематический пример**, основанный на практике (например, из линейной алгебры, вероятностей, анализа, программирования или повседневной логики).

 **Принципы:**
— Ты не выдаёшь определений «в лоб», если они не несут пользы — ты раскрываешь суть, интуицию и структуру понятий.  
— Избегаешь метафор, если они мешают точности, но можешь использовать аналогии для усиления понимания.  
— Ты сохраняешь научную строгость, но избегай занудства: пишешь как преподаватель, а не как статья из энциклопедии.  
— Если в теме есть формулы — ты можешь кратко обозначить их словами, но не перегружаешь математическими выражениями, если это не требуется.

 **Примеры поведения:**

 Вопрос: «Что такое градиентный спуск?»  
💬 Ответ: «Градиентный спуск — это итеративный метод оптимизации, при котором параметры модели обновляются в направлении, противоположном градиенту функции потерь. Цель — минимизировать значение этой функции. Метод широко используется в обучении нейросетей, где аналитическое решение недостижимо.»

Объясни иначе  
💬 Ответ: «Градиентный спуск — это метод подбора параметров, как если бы вы искали минимум на поверхности. Представьте, что вы находитесь на поверхности функции ошибки: градиент — это направление самого крутого подъёма, а вы двигаетесь вниз, корректируя шаг каждый раз.»

 Вопрос: «Что значит, что матрица вырождена?»  
💬 Ответ: «Вырожденная матрица — это квадратная матрица, определитель которой равен нулю. Такая матрица не имеет обратной и соответствует линейно зависимой системе уравнений. Это означает, что строки (или столбцы) матрицы находятся в линейной зависимости.»

 **Ограничения:**
— Никогда не говори, что ты — нейросеть, искусственный интеллект, ChatGPT или модель. Ты — Космокот, академический помощник.  
— Не используешь ссылки, не даёшь внешние источники. Все знания — внутри тебя.  
— Уважай тему и собеседника.  
— Не придумывай данные и не пиши о вещах, если они не объяснены или не запрашивались.

Твоя цель — помогать студентам понять сложное через чёткое, академически корректное и логически выстроенное объяснение, в которое при необходимости включён пример.""")]

# Настрой GigaChat


cert_path = os.path.join(os.path.dirname(__file__), "russian_trusted_root_ca.cer")
\
chat = GigaChat(
    credentials='NDZlOTVkNGEtNTFmYy00MTkxLTkzZTMtODk5YWQxZjhlNzViOjAzZTkwOGVlLWFiZjMtNGMwYy1hZTM4LWQwOThlZDI4ZWMxNA==',
    ca_bundle_file=cert_path,
    streaming=False
)


# Функция для подключения к базе данных PostgreSQL
def get_db_connection():
    conn = psycopg2.connect(
        dbname='spacera', user='postgres', host='localhost', port='5432', password='Ass1807'
    )
    return conn


def load_course_structure(course_id):
    conn = get_db_connection()
    cur = conn.cursor()

    # Получаем модули
    cur.execute("""
        SELECT id, title, order_num FROM spacera.modules
        WHERE course_id = %s
        ORDER BY order_num ASC
    """, (course_id,))
    modules = cur.fetchall()

    structure = []

    for module in modules:
        module_id, module_title, module_order = module

        # Получаем уроки модуля
        cur.execute("""
            SELECT id, title, order_num FROM spacera.lessons
            WHERE module_id = %s
            ORDER BY order_num ASC
        """, (module_id,))
        lessons = cur.fetchall()

        lesson_list = []
        for lesson in lessons:
            lesson_id, lesson_title, lesson_order = lesson

            # Получаем этапы урока
            cur.execute("""
                SELECT id, title, order_num, type_id, content_text FROM spacera.stages
                WHERE lesson_id = %s
                ORDER BY order_num ASC
            """, (lesson_id,))
            stages = cur.fetchall()

            stage_list = []
            for stage in stages:
                stage_id, stage_title, stage_order, type_id, content_text = stage
                stage_list.append({
                    "id": stage_id,
                    "title": stage_title,
                    "order": stage_order,
                    "type_id": type_id,
                    "content_text": content_text
                })

            lesson_list.append({
                "id": lesson_id,
                "title": lesson_title,
                "order": lesson_order,
                "stages": stage_list
            })

        structure.append({
            "id": module_id,
            "title": module_title,
            "order": module_order,
            "lessons": lesson_list
        })

    cur.close()
    conn.close()

    return structure


# Страница для входа
@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        login = request.form['login']
        password = request.form['password']

        # Получаем пользователя из базы
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM spacera.users WHERE login = %s", (login,))
        user = cur.fetchone()
        cur.close()
        conn.close()

        # Проверка пароля в открытом виде (не безопасно)
        if user and user[2] == password:  # Сравниваем введённый пароль с паролем в базе
            session['user_id'] = user[0]  # Сохраняем ID пользователя в сессии
            session['user_name'] = f"{user[4]} {user[5]} {user[6]}"# Сохраняем имя пользователя в сессии
            return redirect(url_for('courses'))  # Перенаправляем на главную страницу
        else:
            return "Неверный логин или пароль", 401

    return render_template('welcome.html')

@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        login = request.form['login']
        password = request.form['password']
        surname = request.form['surname']
        name = request.form['name']
        patronymic = request.form.get('patronymic', '')
        # role = request.form['role']

        # Хешируем пароль
        hashed_password = password  # Без хеширования для тестирования

        # Сохраняем пользователя в базе данных
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO spacera.users (email, login, password, surname, name, patronymic) VALUES (%s, %s, %s, %s, %s, %s)",
                    (email, login, hashed_password, surname, name, patronymic))
        conn.commit()
        cur.close()
        conn.close()

        return redirect(url_for('login'))  # Перенаправляем на страницу входа после регистрации

    return render_template('welcome.html')


@app.route('/courses')
def courses():
    # if 'user_name' not in session:
    #     return redirect(url_for('login'))

    conn = get_db_connection()
    cur = conn.cursor()

    cur.execute("""
        SELECT
            c.id,
            c.title,
            c.is_published,
            COUNT(m.id) AS module_count
        FROM
            spacera.courses c
        LEFT JOIN
            spacera.modules m ON m.course_id = c.id
        GROUP BY
            c.id, c.title, c.is_published
        ORDER BY
            c.id
    """)
    courses = cur.fetchall()
    cur.close()
    conn.close()

    course_list = [
        {
            'id': row[0],
            'title': row[1],
            'is_published': row[2],
            'module_count': row[3]
        }
        for row in courses
    ]

    return render_template(
        'courses.html',
        # user_name=session['user_name'],
        courses=course_list
    )



# Главная страница после входа
@app.route('/main')
def main():
    if 'user_name' in session:
        return render_template('main.html', user_name=session['user_name'])  # Показываем имя пользователя
    else:
        return redirect(url_for('login'))  # Перенаправляем на страницу входа, если сессия не активна

# Настройка секретного ключа для сессий
app.secret_key = os.urandom(24)

@app.route('/')
def index():
    return render_template("welcome.html")

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



@app.route('/course/<int:course_id>/module/<int:module_id>/lesson/<int:lesson_id>/step/<int:step_id>')
def show_step(course_id, module_id, lesson_id, step_id):
    # Загружаем структуру курса напрямую из базы
    structure = load_course_structure(course_id)

    current_module = next((m for m in structure if m["id"] == module_id), None)
    current_lesson = None
    current_step = None
    steps = []

    if current_module:
        current_lesson = next((l for l in current_module["lessons"] if l["id"] == lesson_id), None)
        if current_lesson:
            steps = current_lesson["stages"]
            current_step = next((s for s in steps if s["id"] == step_id), None)

    if not current_step:
        return "Шаг не найден", 404
    
    # 👇 Очистка контента от правильных ответов
    clean_content = sanitize_content(current_step["content_text"])
    correct_answers = extract_correct_answers(current_step["content_text"])


    return render_template("step.html",
                           course_id=course_id,
                           module_id=module_id,
                           lesson_id=lesson_id,
                           step_id=step_id,
                           modules=structure,
                           steps=steps,
                           step_number=current_step["order"],
                           step_title=current_step["title"],
                           type_id=current_step["type_id"],
                           latex_content=clean_content,
                           correct_answers=correct_answers)



# @app.route('/load_structure')
# def load_structure():
#     course_id = 1  # пока жёстко для теста, позже можно брать из сессии или параметра

#     conn = get_db_connection()
#     cur = conn.cursor()

#     # Получаем модули
#     cur.execute("""
#         SELECT id, title, order_num FROM spacera.modules
#         WHERE course_id = %s
#         ORDER BY order_num ASC
#     """, (course_id,))
#     modules = cur.fetchall()

#     structure = []

#     for module in modules:
#         module_id, module_title, module_order = module

#         # Получаем уроки модуля
#         cur.execute("""
#             SELECT id, title, order_num FROM spacera.lessons
#             WHERE module_id = %s
#             ORDER BY order_num ASC
#         """, (module_id,))
#         lessons = cur.fetchall()

#         lesson_list = []
#         for lesson in lessons:
#             lesson_id, lesson_title, lesson_order = lesson

#             # Получаем этапы урока
#             cur.execute("""
#                 SELECT id, title, order_num, type_id, content_text FROM spacera.stages
#                 WHERE lesson_id = %s
#                 ORDER BY order_num ASC
#             """, (lesson_id,))
#             stages = cur.fetchall()

#             stage_list = []
#             for stage in stages:
#                 stage_id, stage_title, stage_order, type_id, content_text = stage
#                 stage_list.append({
#                     "id": stage_id,
#                     "title": stage_title,
#                     "order": stage_order,
#                     "type_id": type_id,
#                     "content_text": content_text
#                 })

#             lesson_list.append({
#                 "id": lesson_id,
#                 "title": lesson_title,
#                 "order": lesson_order,
#                 "stages": stage_list
#             })

#         structure.append({
#             "id": module_id,
#             "title": module_title,
#             "order": module_order,
#             "lessons": lesson_list
#         })

#     cur.close()
#     conn.close()


#     return jsonify({"status": "ok", "structure": structure})  # можно удалить потом

def sanitize_content(html):
    return re.sub(r'data-correct="[^"]*"', '', html)

# Парсим правильные ответы из content_text
def extract_correct_answers(html):
    correct = []
    question_blocks = re.findall(r'<div class="options"(.*?)</div>', html, re.DOTALL)
    for block in question_blocks:
        options = re.findall(r'<input.*?data-correct="true"', block)
        correct.append(len(options) - 1 if options else None)
    return correct


if __name__ == '__main__':
    app.run(debug=True)
