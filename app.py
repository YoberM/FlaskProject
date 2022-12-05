from flask import Flask, render_template, url_for
import sqlite3
from os.path import exists as file_exists

app = Flask(__name__)


if(file_exists('restaurante.db') == False):
    print("Creando Database")
    con = sqlite3.connect("restaurante.db")
    cur = con.cursor()

    cur.execute("PRAGMA foreign_keys=1;")

    f = open('db/create.sql','r')
    cur.executescript(f.read())
    con.commit()
    # Insert
    f2 = open('db/insert.sql','r')
    cur.executescript(f2.read())
    con.commit()

def CreateConnection(db = "restaurante.db"):
    con = sqlite3.connect(db)
    return con
    
    
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/loginworker")
def loginworker():
    return render_template("loginworker.html")

@app.route("/testdb")
def testdb():
    return render_template("selector.html")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/client")
def client():
    return render_template('cliente.html')

@app.route("/nosotros")
def nosotros():
    return render_template("nosotros.html")

@app.route("/contactar")
def contactar():
    return render_template("contactar.html")

@app.route("/ubicacion")
def ubicacion():
    return render_template("ubicacion.html")

@app.route("/pedido")
def pedido():
    con = CreateConnection()
    cur = con.cursor()
    opciones = cur.execute("SELECT * FROM platillo")
    print(opciones)
    return render_template("pedido.html",opciones = opciones)

@app.route("/mesa")
def mesa():
    return render_template("mesa.html")

if __name__ == "__main__":
    app.run(debug=True,port=5000,host="0.0.0.0")

