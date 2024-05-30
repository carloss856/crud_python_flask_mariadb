from flask import Flask, render_template, request, redirect, url_for
import os
from database import get_db

database = get_db()

template_dir = os.path.dirname(os.path.abspath(os.path.dirname(__file__)))
template_dir = os.path.join(template_dir, 'src', 'templates')

app = Flask(__name__, template_folder=template_dir)


#Rutas de aplicacion
@app.route('/')
def home():

    cur = database.cursor()
    cur.execute("SELECT * FROM users")
    myresult = cur.fetchall()
    #Convertir datos a diccionario
    insertObject = [] #Crear objeto vacio
    if len(myresult) != 0:
        columnNames = [column[0] for column in cur.description] #creamos un array para obtener la descripcion o la posicion
        for record in myresult:
            insertObject.append(dict(zip(columnNames, record))) #insertamos los datos en el arreglo convirtiendolo en un diccionario y comprimiendo el arreglo bidimencional con zip
    database.commit()
    return render_template('index.html', data=insertObject)

#Ruta para Crear usuarios en la base de datos
@app.route('/user', methods=['POST'])
def createUser():
    
    username = request.form['username']
    name = request.form['name']
    password = request.form['password']
    if username and name and password:
        cur = database.cursor()
        sql = "INSERT INTO users (username, name, password) VALUES (%s, %s, %s)"
        data = (username, name, password)
        cur.execute(sql, data)
        database.commit()
    return redirect(url_for('home'))

@app.route('/delete/<string:id>')
def delete(id):
    
    cur = database.cursor()
    sql = "DELETE FROM users WHERE id=%s"
    data = (id,)
    cur.execute(sql, data)
    database.commit()
    return redirect(url_for('home'))

@app.route('/edit/<string:id>', methods=['POST'])
def editUser(id):
    username = request.form['username']
    name = request.form['name']
    password = request.form['password']
    if username and name and password:
        cur = database.cursor()
        sql = "UPDATE users SET username=%s, name=%s, password=%s WHERE id=%s"
        data = (username, name, password, id)
        cur.execute(sql, data)
        database.commit()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True, port=4000)