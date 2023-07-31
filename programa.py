from flask import Flask, render_template,request, redirect
from flaskext.mysql import MySQL

programa = Flask(__name__)

mysql = MySQL()
programa.config['MYSQL_DATABASE_HOST']='localhost'
programa.config['MYSQL_DATABASE_PORT']=3306
programa.config['MYSQL_DATABASE_USER']='root'
programa.config['MYSQL_DATABASE_PASSWORD']=''
programa.config['MYSQL_DATABASE_DB']='concurso'
mysql.init_app(programa)

@programa.route('/')
def index():
    mensaje = 'Esta es una primera prueba'
    return render_template('categorias.html')

@programa.route("/categorias")
def medicos():
        sql = "SELECT * FROM categorias"
        cone = mysql.connect()
        cursor = cone.cursor()
        cursor.execute(sql)
        resultado = cursor.fetchall()
        cone.commit()
        return render_template('/categorias.html', res = resultado )

@programa.route('/agregacategorias')
def agregamedico():
        return render_template('agregacategorias.html')

@programa.route('/guardacategorias', methods=['post'])
def guardamedico():
        nombre = request.form['nombre']
        sql = f"SELECT * FROM 'categorias' WHERE id_categorias"
        con = mysql.connect()
        cursor = con.cursor()
        cursor.execute(sql)
        resultado = cursor.fetchone()
        con.commit()

@programa.route('/borracag/<id>')
def borramed(id):
        sql=f"UPDATE categorias WHERE id_categorias='{id}'"
        con = mysql.connect()
        cur = con.cursor()
        cur.execute(sql)
        con.commit()
        return redirect('/categorias')

@programa.route('/editamed/<id>')
def editamed(id):
        sql = f"SELECT * FROM medicos WHERE id_categorias = '{id}'"
        con = mysql.connect()
        cur = con.cursor()
        cur.execute(sql)
        resultado = cur.fetchall()
        con.commit()
        return render_template('editamedico.html', med = resultado[0])


if __name__ == '__main__':
    programa.run(host='0.0.0.0',debug=True, port='8080')