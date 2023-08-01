from flask import Flask, render_template,request, redirect
from flaskext.mysql import MySQL

programa = Flask(__name__)

mysql = MySQL()
programa.config['MYSQL_DATABASE_HOST']='localhost'
programa.config['MYSQL_DATABASE_PORT']=3306
programa.config['MYSQL_DATABASE_USER']='root'
programa.config['MYSQL_DATABASE_PASSWORD']=''
programa.config['MYSQL_DATABASE_DB']='concurso2,0'
mysql.init_app(programa)


@programa.route('/')
def principal():
        return render_template("sitios.html")

@programa.route("/sitios")
def medicos():
        sql = "SELECT * FROM sitios_turisticos WHERE activo = 1"
        cone = mysql.connect()
        cursor = cone.cursor()
        cursor.execute(sql)
        resultado = cursor.fetchall()
        cone.commit()
        return render_template('/sitios.html', res = resultado )

@programa.route('/agregasitios')
def agregamedico():
        return render_template('agregasitios.html')

@programa.route('/guardasitios', methods=['post'])
def guardamedico():
        id = request.form['id_turisticos']
        nombre = request.form['nombre']
        id_categorias = request.form['id_categorias']
        sector = request.form['sector']
        localizacion = request.form['localizacion']
        calificacion = request.form['calificacion']
        sql = f"SELECT * FROM sitios_turisticos WHERE id_turisticos='{id}'"
        con = mysql.connect()
        cursor = con.cursor()
        cursor.execute(sql)
        resultado = cursor.fetchone()
        con.commit()
        
        if not resultado:
                sql = f"INSERT INTO sitios_turisticos (id_turisticos,nombre,id_categorias,sector,localizacion,calificacion,activo) VALUES ('{id}','{nombre}','{id_categorias}','{sector}','{localizacion}','{calificacion}',1)"
                cursor.execute(sql)
                con.commit()
                return redirect('/sitios')
        
@programa.route('/borrasit/<id>')
def borramed(id):

        sql=f"UPDATE sitios_turisticos SET activo=0 WHERE id_turisticos='{id}'"
        con = mysql.connect()
        cur = con.cursor()
        cur.execute(sql)
        con.commit()
        return redirect('/sitios')

@programa.route('/editasit/<id>')
def editamed(id):
        sql = f"SELECT * FROM sitios_turisticos WHERE id_turisticos = '{id}'"
        con = mysql.connect()
        cur = con.cursor()
        cur.execute(sql)
        resultado = cur.fetchall()
        con.commit()
        return render_template('editasitio.html', med = resultado[0])

@programa.route('/actualizasitio', methods=['POST'])
def actualizamedico():
        id = request.form['id_turisticos']
        nombre = request.form['nombre']
        id_categorias = request.form['id_categorias']
        sector = request.form['sector']
        localizacion = request.form['localizacion']
        calificacion = request.form['calificacion']
        sql = f"UPDATE sitios_turisticos SET nombre = '{nombre}', id_categorias = '{id_categorias}', sector = '{sector}', localizacion = '{localizacion}', calificacion = '{calificacion}' WHERE id_turisticos = '{id}'"
        con = mysql.connect()
        cur = con.cursor()
        cur.execute(sql)
        con.commit()
        return redirect("/sitios")

if __name__ == '__main__':
        programa.run(host='0.0.0.0',debug=True, port='8080')