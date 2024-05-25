from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = "supersecretkey"

# Configuration for MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask'

mysql = MySQL(app)

@app.route('/', methods=['GET'])
def Index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM employees")
    data = cur.fetchall()
    cur.close()
    return render_template('index.html', employees=data)

@app.route('/insert', methods=['POST'])
def insert():
    if request.method == "POST":
        flash("Data Inserted Successfully!!!")
        name = request.form['name']
        address = request.form['address']
        email = request.form['email']
        phone = request.form['phone']
        role = request.form['role']
        
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO employees (name, address, email, phone, role) VALUES (%s, %s, %s, %s, %s)", (name, address, email, phone, role))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('Index'))

@app.route('/update', methods=['POST'])
def update():
    if request.method == 'POST':
        id_data = request.form['id']
        name = request.form['name']
        address = request.form['address']
        email = request.form['email']
        phone = request.form['phone']
        role = request.form['role']
        
        cur = mysql.connection.cursor()
        cur.execute("""
        UPDATE employees 
        SET name=%s, address=%s, email=%s, phone=%s, role=%s 
        WHERE id=%s
        """, (name, address, email, phone, role, id_data))
        flash("Data Updated Successfully!!!")
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('Index'))
    
@app.route('/delete/<string:id_data>', methods=['GET', 'POST'])
def delete(id_data):  
        cur = mysql.connection.cursor()
        cur.execute("DELETE FROM employees WHERE id=%s", (id_data,))
        mysql.connection.commit()
        cur.close()
        flash("Data Deleted Successfully!!!")
        return redirect(url_for('Index'))
        

if __name__ == "__main__":
    app.run(debug=True)
