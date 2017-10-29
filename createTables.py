import sqlite3   #enable control of an sqlite database
import hashlib   #allows for passwords to be encrypted

f="danceballoon.db"

db = sqlite3.connect(f) #open if f exists, otherwise create
c = db.cursor() #facilitate db ops

# -- hardcoded stories and users for site testing purposes --

#c.execute ("DROP TABLE stories")
#c.execute ("DROP TABLE contributions")
#c.execute ("DROP TABLE users")

# creation and population of stories table
c.execute('''CREATE TABLE stories (
		story_ID INTEGER PRIMARY KEY AUTOINCREMENT,
		title TEXT NOT NULL,
		archive TEXT,
		last_update TEXT NOT NULL,
		time_stamp)''')

command = "INSERT INTO stories VALUES(%d, '%s', '%s', '%s', '%s')" % (3231, 'Generic Fairytale', '', 'Once upon a time', '1999-12-31 11:59 PM')
c.execute(command)

command = "INSERT INTO stories VALUES(%d, '%s', '%s', '%s', '%s')" % (4353, "The Story that Never Ends", "This is the story that never ends", "Yes it goes on and on my friend", "2017-10-22 10:03 AM")
c.execute(command)

command = "INSERT INTO stories VALUES(%d, '%s', '%s', '%s', '%s')" % (8972, "The Adventure of the Dead Monkey", "Wow. The monkey died oh no", "He slipped on a banana peel", "2017-10-20 5:30 PM")
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


'''
print "SELECT stories.story_ID FROM stories, contributions WHERE contributions.story_ID != stories.story_ID AND contributions.user_ID = 0"
c.execute("SELECT stories.story_ID FROM stories, contributions WHERE contributions.story_ID != stories.story_ID AND contributions.user_ID = 0")
Lset = []
for tuple in c.fetchall():
    Lset.append(tuple[0])
print "before setting"
print Lset
Lset = list(set(Lset))
print "after setting"
print Lset
db.commit()
db.close()
'''
'''
SELECT story_ID FROM contributions WHERE user_ID = 0

SELECT stories.story_ID FROM stories, contributions WHERE contributions.story_ID != stories.story_ID AND contributions.user_ID = 0
before setting
[3231, 4353, 4353, 8972]
after setting
[4353, 8972, 3231]
'''
