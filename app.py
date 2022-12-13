from flask import Flask, render_template, url_for,redirect, request,flash
import sqlite3
from os.path import exists as file_exists
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from model.User import User
from datetime import date

login_manager = LoginManager()

app = Flask(__name__)
login_manager_app = LoginManager(app)


## BASE DATOS
@login_manager_app.user_loader
def load_user(user_id):
    return User(user_id)

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

@app.route("/login", methods=('POST','GET'))
def login():
    
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for('cliente'))
        else:
            return render_template("login.html")

    if request.method == 'POST':
        correo = request.form['iduser']
        contrasenia = request.form['contrasenia']
        con = CreateConnection()
        cur = con.cursor()

        cur.execute(f"SELECT * FROM persona WHERE correo = '{correo}' AND contrasenia = '{contrasenia}'")
        contenido = cur.fetchall()
        print(contenido)
        if len(contenido) >0:
            # Existe una coincidencia
            id = contenido[0][0]
            print(id)
            user = User(id)
            login_user(user)
            print("alo")
            print(current_user.id)
            return redirect("/cliente")
        else:
            return redirect("/login")


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route("/loginworker",methods=['GET','POST'])  
def loginworker():
    
    if request.method == 'GET':
        return render_template("login.html")

    if request.method == 'POST':
        correo = request.form['iduser']
        contrasenia = request.form['contrasenia']
        con = CreateConnection()
        cur = con.cursor()



        print(cur.execute(f"""SELECT tipo FROM persona 
    INNER JOIN trabajador ON persona.persona_id = trabajador.trabajador_id WHERE correo ='{correo}' AND contrasenia  = '{contrasenia}' ;"""))
        contenido = cur.fetchall()
        print(contenido)
        if len(contenido) >0:
            # Existe una coincidencia
            id = contenido[0]
            print(id)
            user = User(id)
            login_user(user)
            return redirect("/pedidomesero")
        else:
            return redirect("/loginworker")
    return render_template("loginworker.html")


@app.route("/loginworkerform", methods=('POST','GET'))
def loginworkerform():
    print("testing login worker")
    print(request.args.get('iduser'))
    print(request.args.get('contrasenia'))
    correo = request.args.get('iduser')
    contrasenia = request.args.get('contrasenia')

    con = CreateConnection()
    cur = con.cursor()

    print(cur.execute(f"""SELECT tipo FROM persona 
    INNER JOIN trabajador ON persona.persona_id = trabajador.trabajador_id WHERE correo ='{correo}' AND contrasenia  = '{contrasenia}' ;"""))

    contenido = cur.fetchall()
    print(contenido)
    if (len(contenido)>0 ):
        if(contenido[0] == 'Mesero'):
            return redirect("/pedidomesero")
        elif(contenido[0]=='Cocinero'):
            return redirect("/cocinero  ")
    else:
        return redirect("/loginworker")


@app.route("/register",methods=('GET','POST'))
def register():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for('cliente'))
        else:
            return render_template("register.html")

    if request.method == 'POST':
        nombres = request.form['nombres']
        apellidos = request.form['apellidos']
        telefono = request.form['telefono']
        direccion = request.form['direccion']
        correo = request.form['correo']
        contraseña = request.form['contraseña']
        con =  sqlite3.connect('restaurante.db')
        cur = con.cursor()
        
        cur.execute("SELECT * FROM persona ORDER BY persona_id DESC;")
        newid = int(cur.fetchone()[0])
        newid = newid + 1
        con.close()
        
        con =  sqlite3.connect('restaurante.db')
        cur = con.cursor()
        
        print(newid)

        query = """
                INSERT INTO persona (persona_id,nombre,apellidos,correo,contrasenia,telefono,direccion) 
                VALUES ('{newid}','{nombres}','{apellidos}','{correo}','{contraseña}','{telefono}','{direccion}')
                """.format(newid = newid, nombres = nombres,apellidos=apellidos,correo=correo,contraseña= contraseña,telefono = telefono, direccion=direccion)
        cur.execute(query)
        query = f"""
            INSERT INTO 'cliente' ('cliente_id') VALUES
            ('{newid}');
        """
        cur.execute(query)
        con.commit()
        con.close()
        return redirect("/login")
    return render_template("register.html")


@app.route("/testdb")
def testdb():
    con = CreateConnection()
    cur = con.cursor()
    print(cur.execute("SELECT * FROM pedido").fetchall())
    print(cur.execute("SELECT * FROM pedido_platillo").fetchall())
    return render_template("nosotros.html")

@app.route("/cliente")
@login_required
def cliente():
    con = CreateConnection()
    cur = con.cursor()
    print(current_user.id)
    pedido_query =  """SELECT * FROM pedido
                        WHERE cliente_id = '{user_id}'
                        AND estado_id != 13
                        """.format(user_id = current_user.id)

    cur.execute(pedido_query)

    pedido = cur.fetchone()

    if pedido != None and pedido[1] != 0:
        numero = pedido[1]
        flash('Mesero Solicitado (Mesa '+str(numero)+')')
        return render_template('cliente.html')
    else:
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
    
@app.route("/carta")
def carta():
    return render_template("carta.html")

@app.route("/pedido",methods=['GET','POST'])
@login_required
def pedido():
    if request.method == 'GET':    
        con = CreateConnection()
        cur = con.cursor()
        opciones = cur.execute("SELECT * FROM platillo")
        print(opciones)
        return render_template("pedido.html",opciones = opciones)

    if request.method == 'POST':
        print("pedido post")
        print(request.form)
        lista = request.form['lista']
        lista = lista.split("\n")
        for i in range(len(lista)):
            lista[i] = lista[i].split(" ",1)
            

        print(lista)



        con = CreateConnection()
        cur = con.cursor()
        print(current_user.id)
        query = """
        SELECT * FROM pedido
        WHERE cliente_id = '{current_client}'
        AND estado_id != 13
        """.format(current_client = current_user.id)
        
        cur.execute(query)

        pedido = cur.fetchone()
        pedido_id = 0
        if pedido == None:

            cur.execute("SELECT * FROM pedido ORDER BY pedido_id DESC;")
            newid = int(cur.fetchone()[0])
            newid = newid + 1

            insert_query = """
            INSERT INTO pedido (pedido_id, numero_mesa, fecha, estado_id, cliente_id)
            VALUES ('{pedido_id}',0,'{fecha}',12,'{user_id}')
            """.format(pedido_id = newid, fecha = date.today() , user_id = current_user.id)

            cur.execute(insert_query)

            con.commit()
            pedido_id = newid
        else:
            pedido_id = pedido[0]
        
        clean = """
        DELETE FROM pedido_platillo
        WHERE pedido_id_pedido = '{pedido_id}'
        """.format(pedido_id = pedido_id)
        cur.execute(clean)
        con.commit()
        
        sql = """
            INSERT INTO pedido_platillo (pedido_id_pedido,platillo_id_platillo,cantidad) VALUES
            """
        for i in range(len(lista)-1):
            sql = sql + f"('{pedido_id}','{lista[i][0]}','1')"
            if(i!=len(lista)-2):
                sql = sql + ','

        print(sql)
        cur.execute(sql)
        con.commit()
        con.close()
        return redirect(url_for("pedido"))



        
        
### MESERO


@app.route("/pedidomesero")
def pedidomesero():
    con = CreateConnection()
    cur = con.cursor()
    opciones = cur.execute("SELECT * FROM platillo")
    print(opciones)
    return render_template("pedidomesero.html",opciones = opciones)
    
@app.route("/comprobante",methods=['GET','POST'])
def comprobante():
    idpedido = 1
    if request.method == 'GET':    
        pass

    if request.method == 'POST':
        idpedido = request.form['idpedido']

    ##Testing

    con = CreateConnection()
    cur = con.cursor()
    pedido = cur.execute(f"""
    SELECT cantidad,platillo.nombre,costo_venta FROM pedido_platillo
     INNER JOIN platillo ON pedido_platillo.platillo_id_platillo=platillo.platillo_id WHERE pedido_platillo.pedido_id_pedido='{idpedido}'""")
    print(pedido)
    pedido = pedido.fetchall()
    total = 0
    for i in pedido:
        total += i[2]
    datos = [0 ,total]


    opciones = cur.execute(f"""
    SELECT pedido_id FROM pedido""")
    
    opciones = opciones.fetchall()
    print(opciones)
    return render_template("comprobante.html",pedido = pedido,datos = datos,opciones = opciones)



### COCINEROO
@app.route("/cocinero")
def cocinero():
    return render_template("cocinero.html")
@app.route("/visualizarpedidos",methods=['GET','POST'])
def visualizarpedidos():
    
    if request.method == 'GET':
        con = CreateConnection()
        cur = con.cursor()
        pedido = cur.execute("""
        SELECT numero_mesa, estado.nombre FROM pedido
        INNER JOIN estado ON estado.estado_id = pedido.estado_id""")
        print(pedido)
        estados = pedido.fetchall()

        
        return render_template("visualizarpedidos.html",estados = estados)


@app.route("/mesa",methods=['GET','POST'])
@login_required
def mesa():
    if request.method == 'GET':

        return render_template("mesa.html")
    else:
        print("numero",request.form['numero'])
        numero = request.form['numero']
        con = CreateConnection()
        cur = con.cursor()

        query = """
                SELECT * FROM pedido
                WHERE estado_id != 13
                AND numero_mesa = '{mesa_numero}'
                """.format(mesa_numero = numero)
        
        cur.execute(query)

        res = cur.fetchone()
        if res != None:
            con.close()   
            return redirect(url_for('mesa'))
        else:

            pedido_query =  """
                            SELECT * FROM pedido
                            WHERE cliente_id = '{user_id}'
                            AND estado_id != 13
                            """.format(user_id = current_user.id)
            
            cur.execute(pedido_query)

            pedido = cur.fetchone()

            if pedido == None:
                return redirect(url_for('cliente'))
            
            pedido_id = pedido[0]

            update_query =  """
                            UPDATE pedido
                            SET numero_mesa = '{numero}'
                            WHERE pedido_id = '{pedido_id}' 
                            """.format(numero = str(numero) , pedido_id = pedido_id)

            cur.execute(update_query)

            con.commit()

            con.close()
            flash('Mesero Solicitado (Mesa '+str(numero)+')')
            return redirect(url_for('cliente'))

if __name__ == "__main__":
    app.secret_key = 'super secret key'
    app.run(debug=True,port=5000,host="0.0.0.0")

