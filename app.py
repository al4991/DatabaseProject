from flask import Flask, render_template, session, redirect
from flask import url_for, escape, request 
import MySQLdb

app = Flask(__name__)
app.secret_key = "Doesn'tMatterRn"


db = MySQL.db.connect(host="localhost", user="root", 
	                  passwd = "", db="Pricosha")


@app.route("/")
def index():
    if 'username' in session:
    	return 'Logged in as %s' % escape(session['username'])
    return "You ain't logged in"

@app.route('/login', methods=['GET','POST'])
def login():
	if request.method == 'POST':
		session['username'] = request.form['username']
		return redirect(url_for('index'))
	return '''
	    <form method="post"> 
	        <p><input type=text name=username>
	        <p><input type=submit value=Login>
	    </form>
	       '''

@app.route('/logout')
def logout(): 
	session.pop('username', None)
	return redirect(url_for('index'))


if __name__ == "__main__":
	app.run()

