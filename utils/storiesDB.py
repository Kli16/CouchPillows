import sqlite3
import hashlib
import time
import datetime

f = "data/danceballoon.db"

#======================================================
# HELPER FXNS

def openDB():
    db = sqlite3.connect(f)
    c = db.cursor()
    return db, c

def closeDB(db):
    db.commit()
    db.close()

def time_stamp():
    ts = time.time()
    st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    return st

def getUID(u, c):
    uid = -1
    command = "SELECT user_ID FROM users WHERE username = '%s'" %u
    for i in c.execute(command):
        uid = i[0]
    return uid

def getSID(title, c):
    sid = -1
    command = "SELECT story_ID FROM stories WHERE title = '%s'" % (title)
    for i in c.execute(command):
        sid = i[0]
    return sid


#======================================================
# USERS DB FUNCTIONS


#adds a new user to the users table
#--------------------------------
def newUser(u, p):
    db, c = openDB()
    command = "INSERT INTO users (username, password) VALUES ('%s', '%s')" % (u,hashlib.md5(p).hexdigest())
    c.execute(command)
    closeDB(db)


#finds user in users table; returns username and password if existing; null else
#---------------------------------
def findUser(u):
    db, c = openDB()
    command = "SELECT username, password FROM users WHERE username = '%s'" % (u)
    answer = [0, 0]
    for i in c.execute(command):
        answer[0] = i[0]
        answer[1] = i[1]
    closeDB(db)
    return answer


#updates user username & password
#---------------------------------
def updateUser(oldU, newU, p):
    db, c = openDB()
    command = "UPDATE users SET username = '%s', password = '%s' WHERE username = '%s';" % (newU, hashlib.md5(p).hexdigest(), oldU)
    c.execute(command)
    closeDB(db)



#======================================================
# STORIES DB FUNCTIONS


#finds story and returns title; null if nonexisting
#---------------------------------
def findStory(stitle):
    db, c = openDB()
    command = "SELECT title FROM stories WHERE title = '%s'" % (stitle)
    answer = ""
    for i in c.execute(command):
        answer = i[0]
    closeDB(db)
    return answer

#adds a story to the contributions table
#---------------------------------
def addStory(uid, sid):
    db, c = openDB()
    command = "INSERT INTO contributions VALUES (%d, %d)" % (uid,sid)
    c.execute(command)
    closeDB(db)


#adds a new story to the stories table
#---------------------------------
def newStory(u, title, text):
    db, c = openDB()
    uid = getUID(u, c)
    time = time_stamp()
    command = "INSERT INTO stories (title,archive,last_update,time_stamp) VALUES ('%s', '%s', '%s', '%s');" % (
        title, "", text, time)
    c.execute(command)
    db.commit()
    sid = getSID(title, c)
    closeDB(db)
    addStory(uid, sid)


#updates story's archive, last_update
#---------------------------------
def updateStory(title, u, text):
    db, c = openDB()
    time = time_stamp()

    #syntax for concatenating strings : ||
    #adds old last_update to archive
    command = "UPDATE stories SET archive = archive || ' ' || last_update WHERE title = '%s';" % (title)
    c.execute(command)

    #updates last_update to the new text
    command = "UPDATE stories SET last_update = '%s' WHERE title = '%s';" % (text, title)
    c.execute(command)

    #updates time stamp
    command = "UPDATE stories SET time_stamp = '%s' WHERE title = '%s';" % (time, title)

    #adds to the contribution table
    c.execute(command)
    db.commit()
    uid = getUID(u, c)
    print(uid)
    sid = getSID(title, c)
    print(sid)
    closeDB(db)
    addStory(uid, sid)


#returns last_updated
#---------------------------------
def getLast(stitle):
    db, c = openDB()
    command = "SELECT last_update FROM stories WHERE title = '%s';" % (stitle)
    retstr = ''
    for i in c.execute(command):
        retstr = ( i[0] + ' ')
    closeDB(db)
    return retstr


#returns entire story (archive + last_updated)
#---------------------------------
def getStory(stitle):
    db, c = openDB()
    command = "SELECT archive,last_update FROM stories WHERE title = '%s';" % (stitle)
    retstr = ''
    for i in c.execute(command):
        retstr = ( i[0] + ' ' + i[1])
    closeDB(db)
    return retstr


#======================================================
# CONTRIBUTIONS DB FUNCTIONS


#gets contributors for a story
#---------------------------------
def getConts(stitle):
    db, c = openDB()
    command = "SELECT username FROM users, contributions, stories WHERE users.user_ID = contributions.user_ID AND contributions.story_ID = stories.story_ID AND title = '%s';" % (stitle)
    retstr = []
    for i in c.execute(command):
        retstr.append( i[0] )
    closeDB(db)
    return retstr


# gets stories user has contributed to
#---------------------------------
def getCStories(u):
    db, c = openDB()
    stories = []
    uid = getUID(u, c)
    command = "SELECT title FROM stories, contributions WHERE stories.story_ID = contributions.story_ID AND contributions.user_ID = %d;" % (uid)
    for i in c.execute(command):
        stories.append(i[0])
    closeDB(db)
    return stories


## gets stories user has NOT contributed to
#---------------------------------
def getAStories(u):

    uStories = getCStories(u)

    db, c = openDB()
    stories = []
    uid = getUID(u, c)

    # gets contributed stories from others
    command = "SELECT title FROM stories, contributions WHERE user_ID != %d AND contributions.story_ID = stories.story_ID" % uid
    oStories = []
    final = []
    for story in c.execute(command):
        oStories.append(story[0])
        final.append(story[0])

    #removes user's contributed stories from list of other's contributed stories
    for x in oStories:
        if x in uStories:
            final.remove(x)

    #removes duplicates by turning into a set and back into a list
    stories = list(set(final))
    closeDB(db)
    return stories
