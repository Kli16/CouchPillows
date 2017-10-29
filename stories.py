from flask import Flask, render_template, request, session, redirect, url_for, flash
import storiesDB
import hashlib
import sqlite3

stories = Flask(__name__)
stories.secret_key = 'random'


#============================================================
# LOG IN / LOG OUT ROUTES

# authentication helper fxn
#------------------------------------------------
AUTHENTICATED = 1
BADUSER = -1
BADPASSWORD = -2
def authenticate(user, password):
    correct = storiesDB.findUser(user)
    if user == correct[0]:
        if hashlib.md5(password).hexdigest() == correct[1]:
            return AUTHENTICATED
        else:
            return BADPASSWORD
    else:
        return BADUSER

    
#root: checks if user in session
# REDIRECTS: home
# RENDERS: login
#-------------------------------------------------
@stories.route('/')
def root():
    if 'user' in session:
        return redirect(url_for('home'))
    else:
        return render_template('login.html')

    
#login: takes in input from form in login.html; authenticates;
# REDIRECTS: home, root
# RENDERS: 
#-------------------------------------------------
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


#signup : checks if user is not in session
# REDIRECTS: home
# RENDERS: sign_up
#-------------------------------------------------
@stories.route('/signup', methods=['POST', 'GET'])
def signup():
    if 'user' not in session:
        return render_template("sign_up.html")
    else :
        return redirect(url_for('home'))

    
#signing: updates db's users
# REDIRECTS: root, sign_up
# RENDERS:
#-------------------------------------------------
@stories.route('/signing', methods = ['POST'])
def signing():
    if 'user' not in session:
        username = request.form['usr']
        password = request.form['pwd']
        passwordconf = request.form['cpwd']

        taken = storiesDB.findUser(username)
        if username == taken[0]:
            flash("Username taken!")
            return redirect(url_for('signup'))

        if password == passwordconf:
            #DATABASE STUFF, ADD IT IN THE DATABASE
            return redirect(url_for('root'))
    else:
        flash ("You are already signed in!")
    return redirect(url_for('root'))


#logout: pops user off session
# REDIRECTS: root
# RENDERS: 
#-------------------------------------------------
@stories.route('/logout', methods = ['POST'])
def logout():
    if 'user' in session:
        session.pop('user')
        #print "testingg"
    return redirect(url_for('root'))



#============================================================
# HOME 

#home: shows list of contributed stories
# REDIRECTS: root
# RENDERS: home
#-------------------------------------------------
@stories.route('/home', methods = ['POST', 'GET'])
def home():
    if 'user' in session:
        return render_template('home.html',
                               stories = storiesDB.getCStories(session['user']))
    else:
        return redirect(url_for('root'))


    
#============================================================
# ACCOUNT ROUTES

#profile: checks if user in session
# REDIRECTS: root
# RENDERS: profile
#-------------------------------------------------
@stories.route('/profile', methods=['POST', 'GET'])
def profile():
    if 'user' in session:
        return render_template('profile.html',
                               usr = session['user'])
    else:
        return redirect(url_for('root'))


#profiling: updates db with new user info
# REDIRECTS: root
# RENDERS: 
#-------------------------------------------------
@stories.route('/profiling', methods = ['POST'])
def profiling():
    return 0



#============================================================    
# VIEW CONTRIBUTED STORY ROUTE

#story: shows full story (retrieved from db) + contributers (including user)
# REDIRECTS: root
# RENDERS: story
#-------------------------------------------------
@stories.route('/story', methods = ['POST'])
def story():
    if 'user' in session:
        story = request.form['link']
        return render_template('story.html',
                               title = story,
                               conts = storiesDB.getConts(story),
                               archive = storiesDB.getStory(story))
    else:
        return redirect(url_for('root'))



#============================================================    
# CREATE ROUTES

#create_stories: gives user form to input new story info
# REDIRECTS: root
# RENDERS: create
#-------------------------------------------------
@stories.route('/createstory', methods = ['POST', 'GET'])
def create_stories():
    if 'user' in session:
        return render_template("create.html")
    else:
        return render_template(url_for('root'))


#creating: puts user input into database; updates stories and contributions
# REDIRECTS: home
# RENDERS: 
#-------------------------------------------------
@stories.route('/creating', methods = ['POST'])
def creating():
    return 0
    

#============================================================    
# CONTRIBUTE ROUTES
    
#all_stories: shows all stories the user can contribute to
# REDIRECTS: root
# RENDERS: story
#-------------------------------------------------
@stories.route('/all_stories', methods = ['POST', 'GET'])
def all_stories():
    if 'user' in session:
        return render_template("all_stories.html", stories = storiesDB.getAStories(session['user']))
    else:
        return render_template(url_for('root'))


#contribute: gives user last update and form for next update
# REDIRECTS: root
# RENDERS: contribute
#-------------------------------------------------
@stories.route('/contribute', methods = ['POST'])
def contribute():
    if 'user' in session:
        story = request.form['link']
        return render_template("contribute.html",
                               title = story,
                               last_update = storiesDB.getLast(story))
    else:
        return render_template(url_for('root'))

    
#contributing: updates db's contributions and stories with user input
# REDIRECTS: home
# RENDERS: 
#-------------------------------------------------
@stories.route('/contributing', methods = ['POST'])
def contributing():
    return 0
        




#============================================================
# RUNNING

if __name__ == '__main__':
    stories.debug = True
    stories.run()
