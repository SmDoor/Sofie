import sqlite3

conn=sqlite3.connect('Robot.db')

conn.execute('''CREATE TABLE USER
	(ID    INTEGER PRIMARY KEY AUTOINCREMENT,
	NAME     TEXT  NOT NULL,
	USERNAME TEXT NOT NULL,
	PASSWORD TEXT NOT NULL);''')


conn.execute('''CREATE TABLE PERSON
	(ID    INTEGER PRIMARY KEY AUTOINCREMENT,
	NAME   TEXT  NOT NULL);''')


conn.execute('''CREATE TABLE IMAGE
	(ID  INTEGER PRIMARY KEY AUTOINCREMENT,
	FILE_NAME            TEXT      NOT NULL,
	DATE             DATETIME      NOT NULL,
	ENCODINGS            TEXT      NOT NULL,
	PERSON_ID         INTEGER      NOT NULL,
	FOREIGN KEY(PERSON_ID) REFERENCES PERSON(ID));''')

conn.execute('''CREATE TABLE MESSAGE
	(ID  INTEGER PRIMARY KEY AUTOINCREMENT,
	MESSAGE           TEXT  NOT NULL,
	DATE          DATETIME  NOT NULL,
	FROM_ID	       INTEGER  NOT NULL,
	TO_ID          INTEGER  NOT NULL,
	STATUS   CHARACTER(16)  NOT NULL,
	FOREIGN KEY(TO_ID) REFERENCES PERSON(ID),
	FOREIGN KEY(FROM_ID) REFERENCES USER(ID));''')
	
conn.close()
