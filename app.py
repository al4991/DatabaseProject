from flask import Flask, render_template, session, redirect
from flask import url_for, escape, request, flash 
import pymysql.cursors

app = Flask(__name__)
app.secret_key = "Doesn'tMatterRn"

# Setting up MySQL
db = pymysql.connect(host='localhost',
	                 user='root',
	                 password='root',
	                 db='meetup',
	                 charset='utf8mb4',
	                 cursorclass=pymysql.cursors.DictCursor)


@app.route("/")
def index():
    if 'useremail' in session:
    	return 'Logged in as %s' % escape(session['useremail'])

    return "You ain't logged in"


@app.route('/login', methods=['GET', 'POST'])
def login(): 
	# Get the info we have in the form
    user_email = request.form['email']
    password = request.form['password']
    # Set up cursor to prepare for executing queries
    cursor = db.cursor()
    # Templating the query to check email and password
    # FOR THE FUTURE: we need to account for the fact that we will 
    # be hashing passwords :) 
    query = 'SELECT * FROM PERSON WHERE email = %s and password = %s'
    cursor.execute(query, (user_email, password))
    # Grab the row with email and password (if it exists)
    data = cursor.fetchone()
    # We're done with the cursor now so we can close it
    cursor.close()

    # Checking to see if the login info actually exists or not 
    if (data):
    	# creates a session for the user
    	session['useremail'] = user_email
    	# redirecting user to our main page
    	return redirect(url_for('/'))
    else: 
    	# Means we didn't find the login info, so failed login
    	# We create an error to pass to our html
    	flash("Something is wrong. Login failed")
    	error = "Invalid email or password"
    	return render_template('login.html', error=error)


@app.route('/signup', methods=['GET', 'POST'])
def signup(): 
	return render_template('signup.html')


@app.route('/logout')
def logout(): 
	session.pop('useremail', None)
	return redirect(url_for('/'))


if __name__ == "__main__":
	app.run('127.0.0.1', 5000, debug = True)

