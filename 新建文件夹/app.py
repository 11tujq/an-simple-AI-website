from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# 初始化数据库
def init_db():
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS chat
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  question TEXT NOT NULL,
                  answer TEXT)''')
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    c.execute("SELECT * FROM chat")
    questions = c.fetchall()
    conn.close()
    return render_template('index.html', questions=questions)

@app.route('/submit_question', methods=['POST'])
def submit_question():
    question = request.form['question']
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    c.execute("INSERT INTO chat (question) VALUES (?)", (question,))
    conn.commit()
    conn.close()
    return redirect('/')

@app.route('/admin')
def admin():
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    c.execute("SELECT * FROM chat")
    questions = c.fetchall()
    conn.close()
    return render_template('admin.html', questions=questions)

@app.route('/answer_question', methods=['POST'])
def answer_question():
    id = request.form['id']
    answer = request.form['answer']
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    c.execute("UPDATE chat SET answer = ? WHERE id = ?", (answer, id))
    conn.commit()
    conn.close()
    return redirect('/admin')

if __name__ == '__main__':
    app.run(debug=True)

