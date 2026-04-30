from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Create DB
def init_db():
    conn = sqlite3.connect('database.db')
    conn.execute('''CREATE TABLE IF NOT EXISTS donors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    age INTEGER,
                    blood_group TEXT,
                    contact TEXT)''')
    conn.commit()
    conn.close()

init_db()

# Home
@app.route('/')
def index():
    return render_template('index.html')

# Register donor
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        age = request.form['age']
        blood = request.form['blood']
        contact = request.form['contact']

        conn = sqlite3.connect('database.db')
        conn.execute("INSERT INTO donors (name, age, blood_group, contact) VALUES (?, ?, ?, ?)",
                     (name, age, blood, contact))
        conn.commit()
        conn.close()
        return redirect('/donors')

    return render_template('register.html')

# View donors
@app.route('/donors')
def donors():
    conn = sqlite3.connect('database.db')
    data = conn.execute("SELECT * FROM donors").fetchall()
    conn.close()
    return render_template('donors.html', donors=data)

# Search blood
@app.route('/request', methods=['GET', 'POST'])
def request_blood():
    donors = []
    if request.method == 'POST':
        blood = request.form['blood']
        conn = sqlite3.connect('database.db')
        donors = conn.execute("SELECT * FROM donors WHERE blood_group=?", (blood,)).fetchall()
        conn.close()

    return render_template('request.html', donors=donors)
@app.route('/delete/<int:id>')
def delete(id):
    conn = sqlite3.connect('database.db')
    conn.execute("DELETE FROM donors WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/donors')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=5000)
    