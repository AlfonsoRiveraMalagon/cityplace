from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

# initializacion de la app
app = Flask(__name__)

# Mysql Connection

app.config['MYSQL_HOST'] = 'us-cdbr-east-05.cleardb.net' 
app.config['MYSQL_PORT'] = 3306
app.config['MYSQL_USER'] = 'b00171aeb62698'
app.config['MYSQL_PASSWORD'] = '123456'
app.config['MYSQL_DB'] = 'heroku_0431911d94d8b92'

#app.config['MYSQL_HOST'] = 'localhost' 
#app.config['MYSQL_PORT'] = 3306
#app.config['MYSQL_USER'] = 'root'
#app.config['MYSQL_PASSWORD'] = 'segura9108'
#app.config['MYSQL_DB'] = 'city_place'

mysql = MySQL(app)

# settings
app.secret_key = "mysecretkey"

# routes
@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM empresas')
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', contacts = data)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        razon_social = request.form['razon_social']
        email = request.form['email']
        sector_comercial = request.form['sector_comercial']
        nombre_contacto = request.form['nombre_contacto']
        telefono = request.form['telefono']
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO empresas (razon_social, email, sector_comercial, nombre_contacto, telefono) VALUES (%s,%s,%s,%s,%s)", (razon_social, email, sector_comercial, nombre_contacto, telefono))
        mysql.connection.commit()
        flash('Se agregó satisfactoriamente')
        return redirect(url_for('Index'))

@app.route('/edit/<id>', methods = ['POST', 'GET'])
def get_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM empresas WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit-contact.html', contact = data[0])

@app.route('/update/<id>', methods=['POST'])
def update_contact(id):
    if request.method == 'POST':
        razon_social = request.form['razon_social']
        email = request.form['email']
        sector_comercial = request.form['sector_comercial']
        nombre_contacto = request.form['nombre_contacto']
        telefono = request.form['telefono']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE empresas
            SET razon_social = %s,
                email = %s,
                sector_comercial = %s,
                nombre_contacto = %s,
                telefono = %s
            WHERE id = %s
        """, (razon_social, email, sector_comercial, nombre_contacto, telefono, id))
        flash('Contacto actualizado satisfactoriamente')
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_contact(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM empresas WHERE id = {0}'.format(id))
    mysql.connection.commit()
    flash('Contacto eliminado satisfactoriamente')
    return redirect(url_for('Index'))

@app.route('/about')
def about():
    return render_template('about.html')


# starting the app
if __name__ == "__main__":
    app.run(port=3000, debug=True)
