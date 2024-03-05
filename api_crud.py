from flask import Flask, render_template, redirect, request, url_for
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('demo.db')
    conn.row_factory = sqlite3.Row
    return conn



# register - home, active -> log out -> removes from active add to non active table

@app.route("/",methods=["GET", "POST"])
def login():
    if request.method == "POST":
        conn = get_db_connection()
        curr = conn.cursor()
        curr.execute("INSERT INTO users (name, age) VALUES (?,?);",(request.form['username'],request.form['age']))
        conn.commit()
        return redirect(url_for('home'))

    return render_template("register.html")

@app.route("/home")
def home():
    conn = get_db_connection()
    curr = conn.cursor()
    curr.execute("Select id,name,age from users")
    rows = curr.fetchall()
    return render_template('user.html', users = rows)

@app.route("/update/<int:u_id>", methods=["GET", "POST"])
def up_users(u_id):
    if request.method == 'POST':
        conn = get_db_connection()
        curr = conn.cursor()
        curr.execute("UPDATE users SET name = ?, age = ? WHERE id = ?", (request.form['name'],request.form['age'],u_id))
        conn.commit()
        return redirect(url_for('home'))
    return render_template('update.html',uid = u_id)


@app.route("/delete/<int:d_id>")
def del_users(d_id):
    conn = get_db_connection()
    curr = conn.cursor()
    curr.execute("DELETE FROM users where id = ?",(d_id,))
    conn.commit()
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)