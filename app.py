from flask import Flask, render_template, request, redirect
# from flask_sqlalchemy import SQLAlchemy     FUCK YOU
import sqlite3
from datetime import datetime

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///project.db"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# db = SQLAlchemy(app)

# class Todo(db.Model):
#     sno =  db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String(200), nullable = False)
#     content = db.Column(db.String(1000), nullable = False)
#     data_created = db.Column(db.DateTime, default=datetime.now())

#     def __repr__(self):
#         return f"{self.sno} - {self.title}"

def connect_db():
    return sqlite3.connect("project.db")


def column_exists(cursor, table_name, column_name):
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [row[1] for row in cursor.fetchall()]  # Extract column names
    return column_name in columns

def init_db():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS Todo(
    Id INTEGER PRIMARY KEY AUTOINCREMENT,
    Title TEXT NOT NULL,
    Description TEXT NOT NULL,
    priority INTEGER DEFAULT 0, 
    Date_Time TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
    ''') #-- 0 for not importaint, 1 for importaint
    if not column_exists(cursor, "Todo", "priority"):
        cursor.execute('''ALTER TABLE Todo ADD COLUMN priority INTEGER''')
        conn.commit()
        conn.close()
    conn.commit()
    conn.close()
    
init_db()

@app.route("/")
def hello():
    page = request.args.get('page', 1, type=int)
    per_page = 6
    offset = (page - 1) * per_page

    conn = connect_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM Todo WHERE priority == 1")
    todos = cursor.fetchall()   # will store the data in list of tuples

    cursor.execute("SELECT * FROM Todo")
    alltodos = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) FROM Todo")
    total_rows = cursor.fetchone()[0]

    cursor.execute("SELECT * FROM Todo LIMIT ? OFFSET ?", (per_page, offset))
    todoa = cursor.fetchall()

    # print("what is this",total_rows)
    total_pages = ( total_rows + per_page - 1) // per_page
    conn.close()    

    # return render_template("index.html", todos=todos, alltodos=alltodos, page=page, total_rows=total_rows, per_page=per_page)

    return render_template('index.html', todos=todos, alltodos=alltodos, todoa=todoa, total_pages=total_pages, page=page) 
#"Hello, World!"

@app.route("/add-todo", methods=['POST'])
def add_todo():
    title = request.form.get("title")
    desc = request.form.get("desc")
    a = request.form.get("imp")
    print(f"Checkbox value: {a}")
    if a == "on":
        priority = 1 
    else:
        priority = 0
    if title and desc:
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Todo (Title, Description,priority) VALUES (?,?,?)",(title, desc, priority))
        conn.commit()
        conn.close()

    return redirect("/")



if __name__ == '__main__':
    app.run(debug=True, port =8000)