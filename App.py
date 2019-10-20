from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)

# MYSQL CONEXIÓN
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'juan123'
app.config['MYSQL_DB'] = 'flaskcontacts'
mysql = MySQL(app)

# CONFIGURACIONES
app.secret_key = 'mysecretkey'

# RUTAS
@app.route('/')
def Index():
    cur = mysql.connection.cursor(())
    cur.execute(('SELECT * FROM contacts'))
    data = cur.fetchall()  ## ENCAPSULANDO LOS DATOS DE LA CONSULTA A UNA VARIABLE
    return render_template('index.html', contacts = data)

@app.route('/agregar', methods=['POST'])
def agregarContacto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        correo = request.form['correo']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contacts (fullname, phone, email) VALUES (%s, %s, %s)',
                    (nombre, telefono, correo))
        mysql.connection.commit()
        flash('Contacto guardado con exito!')
        return redirect(url_for('Index'))

@app.route('/editar/<id>')
def editarContacto(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts WHERE id = %s', (id,))
    data = cur.fetchall()
    return render_template('editarContacto.html', contact = data[0])

@app.route('/actualizar/<id>', methods=['POST'])
def actualizarContacto(id):
    if request.method == 'POST':
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        correo = request.form['correo']
        cur = mysql.connection.cursor()
        cur.execute('UPDATE contacts SET fullname = %s, phone = %s, email = %s WHERE id = %s', (nombre, telefono, correo, id))
        mysql.connection.commit()
        flash('Contacto Actualizado con exito')
    return redirect(url_for('Index'))

@app.route('/eliminar/<string:id>')
def eliminarContacto(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contacto eliminado con exito')
    return redirect(url_for('Index'))

if __name__ == '__main__':
    app.run(port = 3000, debug = True)