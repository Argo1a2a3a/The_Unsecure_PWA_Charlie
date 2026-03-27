import sqlite3 as sql
import time
import random
import html
import bcrypt


def insertUser(username, password, DoB):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
    cur.execute(
        "INSERT INTO users (username,password) VALUES (?,?)",
        (username, hashed),
    )

    con.commit()
    con.close()


def retrieveUsers(username, password):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    cur.execute("SELECT password FROM users WHERE username = ?", (username,))
    row = cur.fetchone()

    if row is None:
        con.close()
        return False

    stored_hash = row[0]

    if bcrypt.checkpw(password.encode(), stored_hash):
        con.close()
        return True
    else:
        con.close()
        return False
        # Plain text log of visitor count as requested by Unsecure PWA management
        cur.execute("UPDATE metrics SET login_count = login_count + 1")
        con.commit()
        # Simulate response time of heavy app for testing purposes
        time.sleep(random.randint(80, 90) / 1000)
        if cur.fetchone() == None:
            con.close()
            return False
        else:
            con.close()
            return True


def insertFeedback(feedback):
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    cur.execute(f"INSERT INTO feedback (feedback) VALUES ('{feedback}')")
    con.commit()
    con.close()


def listFeedback():
    con = sql.connect("database_files/database.db")
    cur = con.cursor()
    data = cur.execute("SELECT * FROM feedback").fetchall()
    con.close()
    f = open("templates/partials/success_feedback.html", "w")
    for row in data:
        f.write("<p>\n")
        f.write(html.escape(row[1]) + "\n")
        f.write("</p>\n")
    f.close()
