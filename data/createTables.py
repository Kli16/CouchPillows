import sqlite3   #enable control of an sqlite database
import hashlib   #allows for passwords to be encrypted

def createTables():
    f="data/danceballoon.db"

    db = sqlite3.connect(f) #open if f exists, otherwise create
    c = db.cursor() #facilitate db ops

    # -- hardcoded stories and users for site testing purposes --

    # creation and population of stories table
    c.execute('''CREATE TABLE stories (
            story_ID INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT UNIQUE,
            archive TEXT,
            last_update TEXT NOT NULL,
            time_stamp)''')

    command = "INSERT INTO stories VALUES(%d, '%s', '%s', '%s', '%s')" % (3231, 'Generic Fairytale', '', 'Once upon a time', '1999-12-31 11:59 PM')
    c.execute(command)

    command = "INSERT INTO stories VALUES(%d, '%s', '%s', '%s', '%s')" % (4353, "The Story that Never Ends", "This is the story that never ends.", "Yes it goes on and on my friend.", "2017-10-22 10:03 AM")
    c.execute(command)

    command = "INSERT INTO stories VALUES(%d, '%s', '%s', '%s', '%s')" % (8972, "The Adventure of the Dead Monkey", "Wow. The monkey died. oh no!", "He slipped on a banana peel.", "2017-10-20 5:30 PM")
    c.execute(command)
    
    # creation and population of users table
    command = '''CREATE TABLE users (
            user_ID INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT NOT NULL)'''
    c.execute(command)

    password = hashlib.md5('admin').hexdigest() # hexdigest returns the encrypted string instead of location in memory
    command = "INSERT INTO users VALUES(%d, '%s', '%s')" % (0, 'DW', password)
    c.execute(command)

    password = hashlib.md5('trampolines').hexdigest()
    command = "INSERT INTO users VALUES(%d, '%s', '%s')" % (1, 'Kevin', password)
    c.execute(command)

    password = hashlib.md5('12345').hexdigest()
    command = "INSERT INTO users VALUES(%d, '%s', '%s')" % (2, 'luckycharms123', password)
    c.execute(command)

    password = hashlib.md5('chickens').hexdigest()
    command = "INSERT INTO users VALUES(%d, '%s', '%s')" % (3, 'j.doe', password)
    c.execute(command)

    # creation and population of contributions table
    command = '''CREATE TABLE contributions (
            user_ID INTEGER,
            story_ID INTEGER
            )'''
    c.execute(command)

    c.execute("INSERT INTO contributions VALUES(0, 3231)")
    c.execute("INSERT INTO contributions VALUES(0, 8972)")
    c.execute("INSERT INTO contributions VALUES(1, 4353)")
    c.execute("INSERT INTO contributions VALUES(2, 4353)")
    c.execute("INSERT INTO contributions VALUES(2, 8972)")

    db.commit()
    db.close()