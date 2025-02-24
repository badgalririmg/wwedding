from flask import Flask, request, render_template, redirect
import sqlite3

app = Flask(__name__)

# Создаём таблицу, если её нет
def init_db():
    conn = sqlite3.connect("wishes.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS wishes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            wish TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        wish = request.form["wish"]  # Исправлено: теперь соответствует полю в index.html

        # Сохраняем в базу данных
        conn = sqlite3.connect("wishes.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO wishes (name, wish) VALUES (?, ?)", (name, wish))
        conn.commit()
        conn.close()

        return redirect("/")  # Обновляем страницу после отправки

    # Загружаем сохранённые пожелания
    conn = sqlite3.connect("wishes.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM wishes")
    wishes = cursor.fetchall()
    conn.close()

    return render_template("index.html", wishes=wishes)

if __name__ == "__main__":
    init_db()  # Инициализация базы при запуске
    app.run(debug=True)
