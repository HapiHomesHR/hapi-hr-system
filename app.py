from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "change_this_to_something_secure"

# ---------------- DB INIT ----------------
def init_db():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    # USERS TABLE
    c.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        password TEXT,
        role TEXT
    )
    """)

    # TIME ENTRIES TABLE
    c.execute("""
    CREATE TABLE IF NOT EXISTS time_entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        work_date TEXT,
        total_hours REAL
    )
    """)

    conn.commit()
    conn.close()

# ---------------- CREATE DEFAULT USER ----------------
def create_default_user():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    # check if admin exists
    c.execute("SELECT * FROM users WHERE name=?", ("admin",))
    exists = c.fetchone()

    if not exists:
        c.execute("""
        INSERT INTO users (name, password, role)
        VALUES (?, ?, ?)
        """, ("admin", "1234", "admin"))

    conn.commit()
    conn.close()

# run setup on startup
init_db()
create_default_user()

# ---------------- LOGIN ----------------
@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        name = request.form["name"]
        password = request.form["password"]

        conn = sqlite3.connect("database.db")
        c = conn.cursor()

        c.execute(
            "SELECT * FROM users WHERE name=? AND password=?",
            (name, password)
        )

        user = c.fetchone()
        conn.close()

        if user:
            session["user_id"] = user[0]
            session["name"] = user[1]
            session["role"] = user[3]
            return redirect("/dashboard")

        return "Invalid login ❌"

    return render_template("login.html")


# ---------------- DASHBOARD ----------------
@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/")

    return render_template("dashboard.html", name=session["name"])


# ---------------- LOGOUT (optional but useful) ----------------
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(debug=True)