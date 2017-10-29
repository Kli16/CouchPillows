from flask import Flask, render_template, request, session, redirect, url_for, flash
import storiesDB
import hashlib
import sqlite3

stories = Flask(__name__)
stories.secret_key = 'random'

#USER = "user1"
#PASS = "pass1"

AUTHENTICATED = 1
BADUSER = -1
BADPASSWORD = -2
def authenticate(user, password):
#    return storiesDB.findUser(user, password)
    correct = storiesDB.findUser(user, password)
    if user == correct[0]:
        if hashlib.md5(password).hexdigest() == correct[1]:
            print("YES")
            return AUTHENTICATED
        else:
            return BADPASSWORD
    else:
        return BADUSER
 

@stories.route('/')
def root():
    if 'user' in session:
        return redirect(url_for('home'))
    else:
        return render_template('login.html')

@stories.route('/login', methods=['POST', 'GET'])
def login():
    username = request.form['usr']
    password = request.form['pwd']
    authres = authenticate(username, password)

    if authres == AUTHENTICATED:
        session['user'] = username
        return redirect( url_for('home') )
    if authres == BADPASSWORD:
        flash('You may have entered the wrong password. Try again!')
        pass
    elif authres == BADUSER:
        flash('You may have entered the wrong username. Try again!')
        pass
    return redirect(url_for('root'))

@stories.route('/signup', methods=['POST'])
def signup():
    if 'user' not in session:
        username = request.form['usr']
        password = request.form['pwd']
        passwordconf = request.form['cpwd']

#CODE NOT WORKING YET
#        if username #is in DATABASE:
#            flash("Username taken!")
#            return render_template(url_for('signup'))
#
#        if password == passwordconf:
#            #DATABASE STUFF, ADD IT IN THE DATABASE
#            return redirect(url_for('root'))
#    else:
#        flash ("You are already signed in!")
#CODE NOT WORKING YET

@stories.route('/profile', methods=['POST', 'GET'])
def profile():
    if 'user' in session:
        return render_template('profile.html', usr = session['user'])
    else:
        return redirect(url_for('root'))

@stories.route('/home', methods = ['POST', 'GET'])
def home():
    if 'user' in session:
        return render_template('home.html')
    else:
        return redirect(url_for('root'))

@stories.route('/contribute')
def contribute_to_stories():
    if 'user' in session:
        #updateStory(sid, uid, text, time)
        pass
    else:
        return render_template(url_for('root'))

@stories.route('/createstory')
def create_stories():
    if 'user' in session:
        #newStory(sid, uid, title, text, time)
        pass
    else:
        return render_template(url_for('root'))

@stories.route('/logout', methods = ['POST'])
def logout():
    if 'user' in session:
        session.pop('user')
        #print "testingg"
    return redirect(url_for('root'))

if __name__ == '__main__':
    stories.debug = True
    stories.run()
