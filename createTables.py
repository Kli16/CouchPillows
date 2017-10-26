import sqlite3   #enable control of an sqlite database
import hashlib   #allows for passwords to be encrypted

f="danceballoon.db"

db = sqlite3.connect(f) #open if f exists, otherwise create
c = db.cursor() #facilitate db ops

# -- hardcoded stories and users for site testing purposes --

# creation and population of stories table
c.execute('''CREATE TABLE stories (
		story_ID INTEGER PRIMARY KEY,
		contributors,
		title TEXT NOT NULL,
		archive TEXT,
		last_update TEXT NOT NULL,
		time_stamp)''')

command = "INSERT INTO stories VALUES(%d, '%s', '%s', '%s', '%s', '%s')" % (3231, 'j-doe', 'Generic Fairytale', '', 'Once upon a time', '1999-12-31 11:59 PM')
c.execute(command)

command = "INSERT INTO stories VALUES(%d, '%s', '%s', '%s', '%s', '%s')" % (4353, '[Kevin, luckycharms123]', "The Story that Never Ends", "This is the story that never ends", "Yes it goes on and on my friend", "2017-10-22 10:03 AM")
c.execute(command)

command = "INSERT INTO stories VALUES(%d, '%s', '%s', '%s', '%s', '%s')" % (8972, '[Kevin]', "The Adventure of the Dead Monkey", "Wow. The monkey died oh no", "He slipped on a banana peel", "2017-10-20 5:30 PM")
c.execute(command)

# creation and population of users table
command = '''CREATE TABLE users (
		user_ID INTEGER PRIMARY KEY,
		username TEXT UNIQUE,
		password TEXT NOT NULL,
		stories)'''
c.execute(command)


password = hashlib.md5('admin').hexdigest() # hexdigest returns the encrypted string instead of location in memory
command = "INSERT INTO users VALUES(%d, '%s', '%s', '%s')" % (0, 'DW', password, [])
c.execute(command)

password = hashlib.md5('trampolines').hexdigest()
command = "INSERT INTO users VALUES(%d, '%s', '%s', '%s')" % (1, 'Kevin', password, [4353, 8972])
c.execute(command)

password = hashlib.md5('12345').hexdigest()
command = "INSERT INTO users VALUES(%d, '%s', '%s', '%s')" % (2, 'luckycharms123', password, [4353])
c.execute(command)

password = hashlib.md5('chickens').hexdigest()
command = "INSERT INTO users VALUES(%d, '%s', '%s', '%s')" % (3, 'j.doe', password, [4353])
c.execute(command)

db.commit()
db.close()
