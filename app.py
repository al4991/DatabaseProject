from flask import Flask, render_template, session, redirect
from flask import url_for, escape, request, flash 
import MySQLdb

app = Flask(__name__)
app.secret_key = "Doesn'tMatterRn"


db = MySQL.db.connect(host="localhost", user="root", 
	                  passwd = "", db="Pricosha")
place = db.cursor()


@app.route("/")
def index():
    if 'useremail' in session:
    	return 'Logged in as %s' % escape(session['useremail'])

    return "You ain't logged in"


@app.route('/login', methods=['GET','POST'])
def login():
	if 'useremail' in session: 
		return redirect(url_for('index'))

	if request.method == 'POST':
		user_email = request.form['email']
	    password = request.form['password']
	    place.execute("SELECT count(*) FROM Person WHERE email = %s;",[user_email])
	    if place.fetchone()[0]:
	    	place.execute("SELECT password FROM Person WHERE email = %s;", [user_email])
	    	row = place.fetchone(): 
	    		if password == row[0]:
	    			session['useremail'] = request.form['useremail']
	    			return redirect(url_for('index'))
	    		else:
	    			flash('Something is wrong')


	    else:
	    	flash("Something is wrong pops")
	   	return render_template('login.html')



@app.route('/signup', methods=['GET', 'POST'])
def signup(): 
	return ''

@app.route('/logout')
def logout(): 
	session.pop('useremail', None)
	return redirect(url_for('index'))


if __name__ == "__main__":
	app.run()

