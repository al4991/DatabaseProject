import os
import re
from flask import Flask, render_template, session, redirect
from flask import url_for, request
from perm import conn

RATE_RE = "(rate[0-9]+)"
rate_match = re.compile(RATE_RE)

TAG_RE = "(tagged[0-9]+)"
tag_match = re.compile(TAG_RE)

app = Flask(__name__)
app.static_folder = 'static'
app.secret_key = "Doesn'tMatterRn"

# APP_ROOT = os.path.dirname(os.path.abspath(__file__))

UPLOAD_FOLDER = os.path.basename('/static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/", methods=['GET', 'POST'])
def index(tagError=None):
    sessionBool = False
    contentType = None
    friendData = None
    memberData = None
    rate_data = None
    rate_stats = None

    if 'userEmail' in session:
        sessionBool = True
    try: 
        contentType = request.form['contentType']
    except:
        contentType = "all"
    data = content(sessionBool, contentType)
    cursor = conn.cursor()
    # adding name of group that you own
    if 'userEmail' in session: 
        friendQuery = "SELECT fg_name FROM FriendGroup WHERE owner_email = %s"
        cursor.execute(friendQuery, session['userEmail'])
        friendData = cursor.fetchall()
        cursor.rownumber = 0
    # adding name of group that you are a part of
        memberQuery = "SELECT fg_name FROM Belong WHERE email = %s AND owner_email != %s"
        useremail = session['userEmail']
        cursor.execute(memberQuery, (useremail, useremail))
        memberData = cursor.fetchall()
        cursor.rownumber = 0

        query = "SELECT item_id, emoji FROM Rate WHERE email = %s"
        cursor.execute(query, (session['userEmail']))
        rate_data = cursor.fetchall()
        cursor.rownumber = 0

    query = "SELECT item_id, emoji, count(*) AS emoji_count FROM Rate GROUP BY item_id, emoji"
    cursor.execute(query)
    rate_stats = cursor.fetchall()

    cursor.close()
    if 'userEmail' in session:
        if tagError:
            flash(tagError)
        return render_template('index.html', ownedGroups=friendData, memberGroups=memberData, posts=data,
                               rates=rate_data, rate_stats=rate_stats, email=session['userEmail'], tagError=tagError, contentType=contentType)
    else:
        return render_template('index.html', posts=data, rate_stats=rate_stats,contentType=contentType)


def content(inSession, contentType):
    cursor = conn.cursor()
    if (inSession):
        if contentType == "text":
            query = "SELECT * FROM ContentItem WHERE (is_pub = 1 AND contentType = (%s) AND post_time + INTERVAL 24 hour >= CURRENT_TIMESTAMP)" \
            " OR email_post = %s"
            cursor.execute(query, ("text",session['userEmail']))
        elif (contentType == "image"):
            query = "SELECT * FROM ContentItem WHERE (is_pub = 1 AND contentType = (%s) AND post_time + INTERVAL 24 hour >= CURRENT_TIMESTAMP)" \
            " OR email_post = %s"
            cursor.execute(query, ("image",session['userEmail']))
        else:
            query = "SELECT * FROM ContentItem WHERE (is_pub = 1 AND post_time + INTERVAL 24 hour >= CURRENT_TIMESTAMP)" \
            " OR email_post = %s"
            cursor.execute(query, session['userEmail'])
    #user not logged in and can only see public data
    else:
        if contentType == "text":
            query = "SELECT * FROM ContentItem WHERE is_pub = 1 AND contentType =(%s) AND post_time + INTERVAL 24 hour >= CURRENT_TIMESTAMP"
            cursor.execute(query,"text")
        elif contentType == "image":
            query = "SELECT * FROM ContentItem WHERE is_pub = 1 AND contentType =(%s) AND post_time + INTERVAL 24 hour >= CURRENT_TIMESTAMP"
            cursor.execute(query,"text")
        else:
            query = "SELECT * FROM ContentItem WHERE is_pub = 1 AND post_time + INTERVAL 24 hour >= CURRENT_TIMESTAMP"
            cursor.execute(query)
    data = cursor.fetchall()
    cursor.close()
    return data


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
        return redirect(url_for('index'))
    else: 
        # Means we didn't find the login info, so failed login
        # We create an error to pass to our html
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
    blog = request.form['content']
    pub = request.form.get('pub')
    file = request.files.getlist('image')
    destination = 'NULL'
    if file:
        contentType = "image"
        target = app.config['UPLOAD_FOLDER']+'/images'
        if not os.path.isdir(target):
            os.makedirs(target)

        for file in request.files.getlist('image'):
            filename = file.filename
            destination = "/".join([target, filename])
    else:
        contentType = "text"

    pub = True if pub else False

    query = 'INSERT INTO ContentItem(email_post, file_path, content_type, item_name, is_pub) VALUES(%s, %s, %s, %s, %s)'
    cursor.execute(query, (user_email, destination, contentType, blog, pub))

    if file:
        file.save(destination)

    conn.commit()
    cursor.close()
    return redirect(url_for('index'))


@app.route('/logout')
def logout():
    session.pop('userEmail')
    return redirect('/')


@app.route('/newGroup')
def newGroup():
    if 'userEmail' in session:
        return render_template('newGroup.html', displayNewGroup="true")
    else:
        return redirect('/')


@app.route('/share/<postid>')
def share(postid):
    if 'userEmail' in session:
        query = 'SELECT owner_email, fg_name FROM belong  WHERE email = %s AND (owner_email, fg_name) ' \
                'NOT IN (SELECT owner_email, fg_name FROM share WHERE item_id = %s)'
        cursor = conn.cursor()
        cursor.execute(query, (session['userEmail'], postid))
        data = cursor.fetchall()
        cursor.close()
        if data:
            return render_template('share.html', postid=postid, data=data)

    return redirect('/')


@app.route('/shareAction/<owner_email>/<fg_name>/<postid>', methods=['GET', 'POST'])
def shareAction(owner_email, fg_name, postid):
    query = "INSERT INTO share VALUES (%s, %s, %s)"
    cursor = conn.cursor()
    cursor.execute(query, (owner_email, fg_name, postid))
    conn.commit()
    cursor.close()
    return redirect('/')


@app.route('/addMember/<nameGroup>')
def addMember(nameGroup):
    if 'userEmail' in session:
        return render_template('newGroup.html', displayAddMember="true", dispGroupName=nameGroup)
    else:
        return redirect('/')


@app.route('/removeMember/<nameGroup>', methods=['GET', 'POST'])
def removeMember(nameGroup):
    if 'userEmail' in session:
        useremail = session['userEmail']
        cursor = conn.cursor()
        showMemQuery = 'SELECT * FROM Belong WHERE fg_name = %s AND email != %s AND owner_email=%s'
        cursor.execute(showMemQuery, (nameGroup, useremail, useremail))
        memNames = cursor.fetchall()
        if memNames:
            nameData = []
            for x in range(len(memNames)):
                searchEmail = memNames[x]['email']
                nameQuery = 'SELECT * FROM Person WHERE email = (%s)'
                cursor.execute(nameQuery, searchEmail)
                nameData.extend(cursor.fetchall())
            cursor.close()
            return render_template('removeMember.html', memNames=memNames, nameGroup=nameGroup, nameData=nameData)
        else:
            # if there are no members the group will be deleted
            cursor = conn.cursor() 
            # delete everyone from belong
            deleteQuery4 = 'DELETE FROM Belong WHERE owner_email = %s AND fg_name = %s'
            cursor.execute(deleteQuery4, (useremail, nameGroup))
            conn.commit()
            conn.rownumber = 0

            # delete the shared content
            deleteQuery5 = 'DELETE FROM Share WHERE owner_email = %s AND fg_name = %s'
            cursor.execute(deleteQuery5, (useremail, nameGroup))
            conn.commit()
            conn.rownumber = 0

            # delete the group
            deleteQuery6 = 'DELETE FROM FriendGroup WHERE owner_email = %s AND fg_name = %s'
            cursor.execute(deleteQuery6, (useremail, nameGroup))
            conn.commit()
            cursor.close()
            # error = "There is no one in this group. Return home to add people"
            return redirect('/')
    else:
        return redirect('/')


@app.route('/deleteMember', methods=['GET', 'POST'])
def deleteMember():
    if 'userEmail' in session:
        useremail = session['userEmail']
        deletePerson = request.form['memberEmail']
        fromGroup = request.form['deleteGroup']
        if request.form.get('Remove') == 'Remove':
            cursor = conn.cursor()
            # delete a person from your group
            deleteQuery1 = 'DELETE FROM Belong WHERE email = %s AND fg_name = %s AND owner_email = %s'
            cursor.execute(deleteQuery1, (deletePerson, fromGroup, useremail))
            conn.commit()
            cursor.close()
            return removeMember(fromGroup)
        # if you want to completely sever your relationship with the person
        elif request.form.get('Sever') == 'Sever':
            cursor = conn.cursor()
            # removes the person from all their groups
            deleteQuery2 = 'DELETE FROM Belong WHERE email = %s AND owner_email = %s'
            cursor.execute(deleteQuery2, (deletePerson, useremail))
            conn.commit()
            conn.rownumber = 0

            # deletes the user from all of deleted persons group to sever friendship
            deleteQuery3 = 'DELETE FROM Belong WHERE email = %s AND owner_email = %s'
            cursor.execute(deleteQuery3, (useremail, deletePerson))
            conn.commit()
            cursor.close()
            return removeMember(fromGroup)
        elif request.form.get('Delete') == 'Delete':
            cursor = conn.cursor() 
            # delete everyone from belong
            deleteQuery4 = 'DELETE FROM Belong WHERE owner_email = %s AND fg_name = %s'
            cursor.execute(deleteQuery4, (useremail, fromGroup))
            conn.commit()
            conn.rownumber = 0

            # delete the shared content
            deleteQuery5 = 'DELETE FROM Share WHERE owner_email = %s AND fg_name = %s'
            cursor.execute(deleteQuery5, (useremail, fromGroup))
            conn.commit()
            conn.rownumber = 0

            # delete the group
            deleteQuery6 = 'DELETE FROM FriendGroup WHERE owner_email = %s AND fg_name = %s'
            cursor.execute(deleteQuery6, (useremail, fromGroup))
            conn.commit()
            cursor.close()
            return redirect('/')
            
        else:
            return removeMember(fromGroup)
    else:
        return redirect('/')
    

@app.route('/createNewGroup', methods=['GET', 'POST'])
def createNewGroup():
    user_email = session['userEmail']
    groupName = request.form['groupName']
    groupDesc = request.form['groupDesc']

    # Check if group already exists!!!!
    cursor = conn.cursor()
    checkQuery = 'SELECT fg_name FROM FriendGroup WHERE owner_email = %s AND fg_name = %s'
    cursor.execute(checkQuery, (user_email, groupName))
    groupData = cursor.fetchone()
    if groupData:
        cursor.rownumber = 0
        error = "You have already created a group with this name"
        cursor.close()
        return render_template('newGroup.html', displayNewGroup="true", error=error)
    else:
        newGroupQuery = 'INSERT INTO FriendGroup(owner_email, fg_name, description) VALUES (%s,%s,%s)'
        cursor.execute(newGroupQuery, (user_email, groupName, groupDesc))
        cursor.rownumber = 0
        conn.commit()
        cursor.close()
        if request.form.get('AddMember') == 'AddMember':
            return render_template('newGroup.html', displayAddMember="true", dispGroupName=groupName)
    cursor.close()
    return redirect(url_for('index'))
   

@app.route('/addNewMember', methods=['GET', 'POST'])
def addNewMember():
    user_email = session['userEmail']
    groupName = request.form['groupName']
    newMemberF = request.form['newMemFname']
    newMemberL = request.form['newMemLname']
    duplicateTest = request.form['duplicateTest']
    # check that the member you're adding exists
    cursor = conn.cursor()
    checkExist = 'SELECT * FROM Person WHERE fname = %s AND lname = %s'
    cursor.execute(checkExist, (newMemberF, newMemberL))
    memExist = cursor.fetchall()
    if duplicateTest == "True":
        cursor.rownumber = 0
        newMemEmail = request.form['newMemEmail']
        # check if they're already in your group
        checkInQuery = 'SELECT * FROM Belong WHERE owner_email = %s AND fg_name = %s AND email = %s'
        cursor.execute(checkInQuery, (user_email, groupName, newMemEmail))
        memExistData2 = cursor.fetchall()
        # if the member already exists
        if memExistData2:
            cursor.close()
            error = "This person is already in your group"
            return render_template('newGroup.html', displayAddMember="true", dispGroupName=groupName, error=error)
        else:
            cursor.rownumber = 0
            addMemQuery2 = 'INSERT INTO Belong (email, owner_email, fg_name) VALUES (%s, %s, %s)'
            cursor.execute(addMemQuery2, (newMemEmail, user_email, groupName))
            message = "you successfully added a member"
            conn.commit()
            cursor.close()
            return render_template('newGroup.html', displayAddMember="true", dispGroupName=groupName, message=message)
    else:
        if len(memExist) == 1:
            cursor.rownumber = 0
            # if the member exists - check if they're already in your group
            newMember = memExist[0]['email']
            print(newMember)
            checkMemQuery = 'SELECT * FROM Belong WHERE owner_email = %s AND fg_name = %s AND email = %s'
            cursor.execute(checkMemQuery, (user_email, groupName, newMember))
            memExistData = cursor.fetchone()
            # if they're already in your group send an error message
            if memExistData:
                error = "This person is already in your group"
                cursor.close()
                return render_template('newGroup.html', displayAddMember="true", dispGroupName=groupName,
                                       error=error)
            else:
                # member exists and is not in group so add the to your group
                cursor.rownumber = 0
                addMemberQuery = 'INSERT INTO Belong (email, owner_email, fg_name) VALUES (%s, %s, %s)'
                cursor.execute(addMemberQuery, (newMember, user_email, groupName))
                message = "You successfully added a member"
                conn.commit()
                cursor.close()
                return render_template('newGroup.html', displayAddMember="true", dispGroupName=groupName,
                                       message=message)
        
        elif len(memExist) == 0:
            error = "This person does not exist, try another email"
            cursor.close()
            return render_template('newGroup.html', displayAddMember="true", dispGroupName=groupName,
                                   error=error)

        else:
            error = "There are multiple people with the same name. Enter the correct email and to move on"
            return render_template('newGroup.html', displayAddMember="true", dispGroupName=groupName, error=error,
                                   duplicate="true", memExist=memExist)


@app.route('/rate', methods=['GET', 'POST'])
def rate():
    user_email = session['userEmail']
    cursor = conn.cursor()
    print(request.form)
    for item in request.form:
        if re.match(rate_match, item):
            cursor.rownumber = 0
            rate_id = int(item.split('e')[-1])
            query = "SELECT * FROM Rate WHERE item_id = %s AND email = %s"
            cursor.execute(query, (rate_id, user_email))
            rate_exist = cursor.fetchone()
            cursor.rownumber = 0
            if rate_exist:
                query = "UPDATE Rate SET rate_time = CURRENT_TIMESTAMP, emoji = %s WHERE item_id = %s AND email = %s"
                cursor.execute(query, (request.form[item], rate_id, user_email))
            else:
                query = "INSERT INTO Rate (email, item_id, rate_time, emoji) VALUES (%s, %s, CURRENT_TIMESTAMP, %s)"
                cursor.execute(query, (user_email, rate_id, request.form[item]))
            conn.commit()
    cursor.close()
    return redirect(url_for('index'))


@app.route('/pendingTags')
def pending_tag():
    user_email = session['userEmail']
    cursor = conn.cursor()
    query = "SELECT * FROM Tag NATURAL JOIN ContentItem WHERE email_tagged = %s AND status = 'False'"
    cursor.execute(query, (user_email))
    pends = cursor.fetchall()
    cursor.close()
    return render_template('pendingTags.html', pendings = pends)


@app.route('/tagAuth', methods=['GET', 'POST'])
def tag_auth():
    user_email = session['userEmail']
    cursor = conn.cursor()
    for item in request.form:
        lst = item.split('@nyu.edu')
        tagger, item_id = lst[0], int(lst[1])
        status = request.form[item]
        query = ""
        if status == "True":
            query = "UPDATE Tag SET status = 'True' WHERE email_tagger = %s AND email_tagged = %s AND item_id = %s"
        else:
            query = "DELETE FROM Tag WHERE email_tagger = %s AND email_tagged = %s AND item_id = %s"
        cursor.execute(query, (tagger+'@nyu.edu', user_email, item_id))
        conn.commit()
    cursor.close()
    return redirect(url_for('pending_tag'))



@app.route('/tag', methods=['GET', 'POST'])
def tag():
    user_email = session['userEmail']
    cursor = conn.cursor()
    for item in request.form:
        if re.match(tag_match, item):
            taggee = request.form[item]
            cursor.rownumber = 0
            tag_id = int(item.split('d')[-1])
            query = "SELECT * FROM Tag WHERE item_id = %s AND email_tagger = %s AND email_tagged = %s"
            cursor.execute(query, (tag_id, user_email, taggee))
            tag_exist = cursor.fetchone()
            cursor.rownumber = 0
            if not tag_exist:
                query = "SELECT is_pub FROM ContentItem WHERE item_id = %s"
                cursor.execute(query, (tag_id))
                is_public = cursor.fetchone()
                cursor.rownumber = 0
                if is_public['is_pub']:
                    print("crop")
                    status = "False"
                    if user_email == taggee:
                        status = "True"
                    query = "INSERT INTO Tag(email_tagged, email_tagger, item_id, status) VALUES (%s, %s, %s, %s)"
                    cursor.execute(query, (taggee, user_email, tag_id, status))
                else:
                    query = "SELECT * FROM Belong NATURAL JOIN Share WHERE email = %s AND item_id = %s"
                    cursor.execute(query, (taggee, tag_id))
                    is_shared = cursor.fetchone()
                    if is_shared:
                        print("What")
                        query = "INSERT INTO Tag(email_tagged, email_tagger, item_id, status) VALUES (%s, %s, %s, %s)"
                        cursor.execute(query, (taggee, user_email, tag_id, "False"))
                    else:
                        error = "Tag request cannot be done."
                        print("plop")
                        return redirect(url_for('index', tagError=error))
            conn.commit()
            break
    cursor.close()
    return redirect(url_for('index'))

@app.route('/comments/<postid>', methods=['GET', 'POST'])
def comments(postid):
    if 'userEmail' in session:
        query = 'SELECT content, commentor_email FROM comments WHERE item_id = %s'
        cursor = conn.cursor()
        cursor.execute(query, postid)
        data = cursor.fetchall()

        cursor.rownumber = 0

        query2 = 'SELECT * FROM ContentItem WHERE item_id = %s'
        cursor.execute(query2, postid)
        post = cursor.fetchone()
        cursor.close()

        return render_template('comments.html', data=data, post=post)


@app.route('/commentsubmit/<postid>', methods=['GET', 'POST'])
def commentsubmit(postid):
    return ''


if __name__ == "__main__":
    app.run('127.0.0.1', 5000, debug=True)
