import sqlite3
import hashlib
import threading

f = "danceballoon.db"

#lock = threading.RLock()
#db = sqlite3.connect(f, check_same_thread = False)
#with lock: 
#    c = db.cursor()

'''
def openDB():
    db = sqlite3.connect(f)
    c = db.cursor()
    return db, c

def closeDB(db):
    db.commit()
    db.close()
'''

#adds a new user to the users table
def newUser(u, p): 
    command = "INSERT INTO users (username, password) VALUES (%s, %s)" % (u,p)
    c.execute(command)

#finds user in users table
def findUser(u, p):
    db = sqlite3.connect("danceballoon.db")
    c = db.cursor()
    command = "SELECT username, password FROM users WHERE username = '%s'" % (u)
    answer = [0, 0]
    for i in c.execute(command):
        answer[0] = i[0]
        answer[1] = i[1]
        '''
        if u == i[0]:
            if hashlib.md5(p).hexdigest() == i[1]:
                answer = 1 
            else:
                answer = -2
        else:
            answer = -1
        '''
    db.close()
    return answer
        
    
#adds a story to the contributions table
def addStory(uid, sid):
    command = "INSERT INTO contributions VALUES (%d, %d)" % (uid,sid)
    c.execute(command)

#adds a new story to the stories table
def newStory(sid, uid, title, text, time):
    addStory(uid,sid)
    command = "INSERT INTO stories VALUES (%d, '%s', '%s', '%s', '%s');" % (        sid, title, "", text, time)
    c.execute(command)


#updates story
def updateStory(sid, uid, text, time):
    #syntax for concatenating strings : ||
    #adds old last_update to archive
    command = "UPDATE stories SET archive = archive || ' ' || last_update WHERE story_ID = %s;" % (sid)
    c.execute(command)
    #updates last_update to the new text
    command = "UPDATE stories SET last_update = '%s' WHERE story_ID = %s;" % (text, sid)
    c.execute(command)
    #updates time stamp
    command = "UPDATE stories SET time_stamp = '%s' WHERE story_ID = %s;" % (time, sid)
    #adds to the contribution table
    c.execute(command)
    addStory(uid, sid)


#returns entire story
def getStory(sid):
    db = sqlite3.connect("danceballoon.db")
    c = db.cursor()
    command = "SELECT archive,last_update FROM stories WHERE story_ID = %d;" % (sid)
    for i in c.execute(command):
        print( i[0] + ' ' + i[1])
    db.close()
        
#print getStory(4353)

#given a list of contributed stories
def getCStories(u):
    db = sqlite3.connect("danceballoon.db")
    c = db.cursor()
    stories = []
    command = "SELECT user_ID FROM users WHERE username = '%s'" %u
    for i in c.execute(command):
        uid = i[0]
    command = "SELECT title FROM stories, contributions WHERE stories.story_ID = contributions.story_ID AND contributions.user_ID = %d;" % (uid)
    for i in c.execute(command):
        stories += [i[0]]
    db.close()
    return stories

print getCStories('DW')


#given a list of available stories
def getAStories(u):
    db = sqlite3.connect("danceballoon.db")
    c = db.cursor()
    cStories = getCStories(u)
    stories = []
    command = "SELECT user_ID FROM users WHERE username = '%s'" %u
    for i in c.execute(command):
        uid = i[0]
    command = "SELECT title FROM stories;" % (uid)
    for i in c.execute(command):
        stories += [i[0]]
    db.close()
    return stories

#print getAStories('DW')
       
#print getStories([4353,3231])

#db.commit()
#db.close()
