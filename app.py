from flask import Flask, render_template, session, redirect
from flask import url_for, request
from perm import conn


app = Flask(__name__)
app.static_folder = 'static'
app.secret_key = "Doesn'tMatterRn"


@app.route("/")
def index():
    cursor = conn.cursor()
    if 'userEmail' in session:
        query = "SELECT * FROM ContentItem WHERE (is_pub = 1 AND post_time + INTERVAL 24 hour >= CURRENT_TIMESTAMP)" \
            " OR email_post = (%s)"
        cursor.execute(query, session['userEmail'])

    else:
        query = "SELECT * FROM ContentItem WHERE is_pub = 1 AND post_time + INTERVAL 24 hour >= CURRENT_TIMESTAMP"
        cursor.execute(query)
    data = cursor.fetchall()
    cursor.rownumber = 0
    if 'userEmail' in session: 
        friendQuery = "SELECT fg_name FROM FriendGroup WHERE owner_email = (%s)"
        # print("friendQuery results are" + friendQuery)
        cursor.execute(friendQuery, session['userEmail'])
    friendData = cursor.fetchall()
    cursor.rownumber = 0
    if 'userEmail' in session:
        memberQuery = "SELECT fg_name FROM Belong WHERE email = (%s) AND owner_email != (%s)"
        useremail = session['userEmail']
        cursor.execute(memberQuery, (useremail, useremail))
    memberData = cursor.fetchall()
    cursor.close()
    if 'userEmail' in session:
        return render_template('index.html', ownedGroups=friendData, memberGroups=memberData, posts=data,
                               email=session['userEmail'])
    else:
        return render_template('index.html', posts=data)


@app.route('/login')
def login(): 
    return render_template('login.html')


@app.route('/loginAuth', methods=['GET', 'POST'])
def loginAuth():
    user_email = request.form['userEmail']
    password = request.form['password']
    # Set up cursor to prepare for executing queries
    cursor = conn.cursor()
    # Templating the query to check email and password
    # FOR THE FUTURE: we need to account for the fact that we will 
    # be hashing passwords
    query = 'SELECT fname, lname FROM PERSON WHERE email = %s and password = SHA2(%s, 256)'
    cursor.execute(query, (user_email, password))
    # Grab the row with email and password (if it exists)
    data = cursor.fetchone()
    # We're done with the cursor now so we can close it
    cursor.close()

    # Checking to see if the login info actually exists or not 
    if data:
        # creates a session for the user
        session['userEmail'] = user_email
        # redirecting user to our main page
        # return redirect(url_for('/'))
        return redirect(url_for('index'))
    else: 
        # Means we didn't find the login info, so failed login
        # We create an error to pass to our html
        # error = "Invalid email or password"
        # return render_template('login.html', error=error)
        error = "Invalid email or password"
        return render_template('login.html', error=error)


@app.route('/register')
def register():
    return render_template('signup.html')


@app.route('/registerAuth', methods=['GET', 'POST'])
def registerAuth():
    # grabs information from the forms
    fname = request.form['fname']
    lname = request.form['lname']
    user_email = request.form['userEmail']
    password = request.form['password']

    # cursor used to send queries
    cursor = conn.cursor()
    # executes query
    query = 'SELECT * FROM PERSON WHERE email = %s'
    cursor.execute(query, user_email)

    data = cursor.fetchone()
    if data:
        error = "This user already exists"
        cursor.close()
        return render_template('signup.html', error=error)
    else:
        ins = 'INSERT INTO PERSON VALUES(%s, SHA2(%s, 256), %s, %s)'
        cursor.execute(ins, (user_email, password, fname, lname))

        conn.commit()
        cursor.close()
        return render_template('index.html')


@app.route('/post', methods=['GET', 'POST'])
def post():
    user_email = session['userEmail']
    cursor = conn.cursor()
    blog = request.form['blog']
    query = 'INSERT INTO ContentItem (email_post, item_name) VALUES(%s, %s)'
    cursor.execute(query, (user_email, blog))
    conn.commit()
    cursor.close()
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.pop('userEmail')
    return redirect('/')


@app.route('/newGroup')
def newGroup():
    displayNewGroup = "true"
    return render_template('newGroup.html', displayNewGroup=displayNewGroup)


@app.route('/createNewGroup', methods=['GET', 'POST'])
def createNewGroup():
    user_email = session['userEmail']
    groupName = request.form['groupName']
    groupDesc = request.form['groupDesc']

    # Check if group already exists!!!!
    cursor = conn.cursor()
    checkQuery = 'SELECT fg_name FROM FriendGroup WHERE owner_email = (%s) AND fg_name = (%s)'
    cursor.execute(checkQuery, (user_email, groupName))
    groupData = cursor.fetchone()
    if groupData:
        cursor.rownumber = 0
        error = "You have already created a group with this name"
        displayNewGroup = "true"
        return render_template('newGroup.html', displayNewGroup=displayNewGroup, error=error)
    else:
        newGroupQuery = 'INSERT INTO FriendGroup(owner_email,fg_name,description) VALUES (%s,%s,%s)'
        cursor.execute(newGroupQuery, (user_email, groupName, groupDesc))
        cursor.rownumber = 0
        if request.form.get('AddMember') == 'AddMember':
            displayAddMember = "true"
            return render_template('newGroup.html', displayAddMember=displayAddMember, dispGroupName=groupName)

    # YOU NEED TO FIX THIS TO ACTUALLY CREATE A GROUP
    return render_template('newGroup.html', displayNewGroup='true')  # fix so it goes back to home.
   
    # newMemberQuery = 'INSERT INTO Belong (email,owner_email,fg_name) VALUES (%s,%s,%s)'
    # cursor.execute(newMemberQuery,(newMember,user_email,groupName))
    # conn.commit();
    # cursor.close();

    # if request.form['submit_button'] == addNewMember:


@app.route('/addNewMember', methods=['GET', 'POST'])
def addNewMember():
    user_email = session['userEmail']
    groupName = request.form['groupName']
    newMember = request.form['newMember']
    # check that the member you're adding exists
    cursor = conn.cursor()
    checkExist = 'SELECT * FROM Person WHERE email =(%s)'
    cursor.execute(checkExist, newMember)
    memExist = cursor.fetchone()
    if memExist:
        # if the member exists - check if they're already in your group
        checkMemQuery = 'SELECT email FROM Belong WHERE owner_email =(%s) AND fg_name = (%s)'
        cursor.execute(checkMemQuery, (user_email, groupName))
        memExistData = cursor.fetchone()
        # if they're already in your group send an error message
        if memExistData:
            cursor.rownumber = 0
            displayAddMember = "true"
            error = "This person is already in your group"
            return render_template('newGroup.html', displayAddMember=displayAddMember, dispGroupName=groupName,
                                   error=error)
        else:
            # member exists and is not in group so add the to your group
            cursor.rownumber = 0
            addMemberQuery = 'INSERT INTO Belong (email, owner_email, fg_name) VALUES (%s,%s,%s)'
            cursor.execute(addMemberQuery, (newMember, user_email, groupName))
            displayAddMember = "true"
            message = "You successfully added a member"
            return render_template('newGroup.html', displayAddMember=displayAddMember, dispGroupName=groupName,
                                   message=message)
    # member doesn't exist
    else:
        cursor.rownumber = 0
        displayAddMember = "true"
        error = "This person does not exist, try another email"
        return render_template('newGroup.html', displayAddMember=displayAddMember, dispGroupName=groupName,
                               error=error)

    checkMemQuery = 'SELECT email FROM Belong WHERE owner_email =(%s) AND fg_name = (%s)'
    cursor.execute(checkMemQuery, (user_email, groupName))
    memExistData = cursor.fetchone()
    if memExistData:
        cursor.rownumber = 0
        error = "This person is already in your group"


if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug=True)
