from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)
DATABASE = 'tasks.db'

# Initialize database
def init_db():
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('''CREATE TABLE IF NOT EXISTS tasks (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        title TEXT NOT NULL,
                        due_date TEXT,
                        status TEXT DEFAULT 'Pending'
                        )''')

@app.route('/')
def index():
    with sqlite3.connect(DATABASE) as conn:
        tasks = conn.execute('SELECT * FROM tasks').fetchall()
    return render_template('index.html', tasks=tasks)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/add', methods=['POST'])
def add_task():
    title = request.form['title']
    due_date = request.form['due_date']
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('INSERT INTO tasks (title, due_date) VALUES (?, ?)', (title, due_date))
    return redirect(url_for('index'))

@app.route('/edit/<int:task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    if request.method == 'POST':
        title = request.form['title']
        due_date = request.form['due_date']
        status = request.form['status']
        with sqlite3.connect(DATABASE) as conn:
            conn.execute('UPDATE tasks SET title = ?, due_date = ?, status = ? WHERE id = ?', 
                         (title, due_date, status, task_id))
        return redirect(url_for('index'))
    else:
        with sqlite3.connect(DATABASE) as conn:
            task = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
        return render_template('edit_task.html', task=task)

@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    with sqlite3.connect(DATABASE) as conn:
        conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
    return redirect(url_for('index'))

@app.route('/filter/<string:status>')
def filter_tasks(status):
    with sqlite3.connect(DATABASE) as conn:
        tasks = conn.execute('SELECT * FROM tasks WHERE status = ?', (status,)).fetchall()
    return render_template('index.html', tasks=tasks)

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
