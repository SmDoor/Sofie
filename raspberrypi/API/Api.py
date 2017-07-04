import sys
sys.path.append("..")
sys.path.append("../Faces")
import pykka
from flask import Flask, request
from flask_restful import Resource, Api
#from sqlalchemy import create_engine
#from json import dumps
from flask.ext.jsonpify import jsonify
import sqlite3
#from PIL import Image
#from io import BytesIO
import datetime
import base64
import random
import encoding
#from encoding import NP2Json
#import face_recognizer
from remote_recognizer import RemoteRecognizer
#frrom Faces import exceptions

#db_connect = create_engine('sqlite:///../Robot.db')
app = Flask(__name__)
api = Api(app)
remote_url = 'http://127.0.0.1:5003'

class DB:
	def __init__(self):
		self.conn = sqlite3.connect('/home/gss9/robot/Robot.db')
		#self.conn.isolation_level = None		
		
	def query(self, sql):
		self.conn = sqlite3.connect('../Robot.db')
		print('test')
		res=self.conn.execute(sql).fetchall()
		print('test2')
		self.conn.commit()
		self.conn.close()
		return res


class Image(Resource):
    def	get(self, image_id):
        #conn = sqlite3.connect('Robot.db').cursor()
        #conn.execute("delete from image where id=?", (image_id,))
        db = DB()
        sql = '''delete from rb_images where id={}"'''
        sql = sql.format(image_id)
        db.query(sql)


class Message(Resource):
    def get(self, message_id):
        #conn = sqlite3.connect('Robot.db').cursor()
        #conn.execute("delete from message where id=?", (message_id,))
        #conn.commit()
        db = DB()
        sql = '''delete from rb_messages where id="{}"'''
        sql = sql.format(message_id)
        db.query(sql)


    def post(self):
        message_id = request.form["message_id"]
        message = request.form["message"]
        #conn = sqlite3.connect('Robot.db').cursor()
        #conn.execute("update message set message=? where id=?", (message, message_id))
        #conn.commit()
        db = DB()
        sql = '''update rb_messages set message="{}" where id="{}"'''
        sql = sql.format(message, message_id)
        db.query(sql)


class User(Resource):
    def get(self, user_id, start=-1, end=-1):
        #conn = sqlite3.connect('Robot.db').cursor()
        #query = conn.execute("""select id, message from message
			#where from_id=?""",(user_id, )).fetchall()

        db = DB()
        sql = '''select id, message from rb_messages where from_id="{}"'''
        sql = sql.format(user_id)
        query = db.query(sql)
		
        if start == -1:
            count = len(query)
            return jsonify({'count':count})
        else:
            query = query[int(start):int(end)]
            res = {id:mess for (id, mess) in query}
            return jsonify(res)

    def post(self):
        username = request.form["username"]
        password = request.form["password"]
        #name = request.form["name"]
        new = request.form["new"]
        #conn = sqlite3.connect('Robot.db').cursor()
        db = DB()
        

        if new == "true":
            name = request.form["name"]
            #conn.execute("""insert into user(username, password, name)
            #                     values(?,?,?)""", (username, password, name))
            sql = '''insert into rb_users(username, password, name)
				values("{}","{}","{}")'''
            sql = sql.format(username, password, name)
            db.query(sql)

        #query = conn.execute("""select id from user
        #                        where username=? and password=?""", (
        #                        username, password)).fetchall()
        sql = '''select id from rb_users where username="{}" and password="{}"'''
        sql = sql.format(username, password)
        query = db.query(sql)

        if len(query) == 0:
            id = -1
        else:
            id = query[0][0]
        #conn.commit()
        token = random.randrange(10000)
        return jsonify({"user_id":id,"token":token})

		
class People(Resource):
    def get(self, person_name, start = -1, end = -1):
        #conn=sqlite3.connect('Robot.db').cursor()
        db = DB()
        if start == -1:
            #count = conn.execute("select count(*) from person where name = ?",(person_name, )).fetchone()[0]
            sql = '''select count(*) from rb_people where name="{}"'''
            sql = sql.format(person_name)
            count = db.query(sql)[0][0]
            #print(count)
            return jsonify({'count':count})
        else:
            #p_query = conn.execute("select id from person where name = ?",(person_name,)).fetchall()
            sql = '''select id from rb_people where name="{}"'''
            sql = sql.format(person_name)
            p_query = db.query(sql)
            print(p_query)
            ids=[row[0] for row in p_query]
            print(ids)
            ids = ids[int(start):int(end)]
            print(ids)
            data={}
            for id in ids:
                 print(id)
                 sql = '''select file_name from rb_images where person_id="{}"'''
                 sql = sql.format(id)
                 i_query = db.query(sql)
                 print(i_query)
                 #i_query = conn.execute("select file_name from image where person_id = ?",(id,)).fetchall()
                 if len(i_query) > 0:
                     file_name = i_query[0][0]
                     with open(file_name, 'rb') as im:
                         encoded = base64.b64encode(im.read())
                         data[id] = encoded.decode('utf-8')
        #result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
            return jsonify(data)

    def post(self):
        print("gfhjk")
        db = DB()
        name = request.form['name']
        image = request.files.get("image")
        person_id = request.form['person_id']
        #conn = sqlite3.connect('Robot.db').cursor()
        date_time = str(datetime.datetime.now())
        encodings = "1ghjk"
        print("gfhjk")
        if person_id == "":
            sql = '''insert into rb_people(name) values("{}")'''
            sql = sql.format(name)
            db.query(sql)
            sql = '''select id from rb_people where name="{}"'''
            sql = sql.format(name)
            person_id = db.query(sql)[-1][0]
            #conn.execute("""insert into person(name) values(?)""", (name, ))
            #person_id = conn.execute("""select id from person where name=?""", (name, )).fetchall()[-1]
        #count = conn.execute("""select count(*) from image where person_id=?""", (
	#		person_id, )).fetchone()[0]
        sql = '''select count(*) from rb_images where person_id="{}"'''
        sql = sql.format(person_id)
        count = db.query(sql)[0]
        print(person_id)
        print(count)
        file_name = str(person_id) + "_" + str(count[0]) + ".jpg"
        image.save(file_name)
        try:
            recognizer = RemoteRecognizer(remote_url)
            encodings = recognizer.remote_get_encodings("/home/gss9/robot/API/"+file_name)
        except:
            print('err3')
            return jsonify({'error':3})
        if len(encodings)==0:
            print('err1')
            return jsonify({'error':1})
        if len(encodings)>1:
            print('err2')
            return jsonify({'error':2})
        encodings = encoding.NP2Json.encode(encodings)
        #conn.execute("""insert into image(file_name, person_id, date, encodings)
        #                 values(?, ?, ?, ?);""", (
        #                 file_name, to_id, date_time, encodings))
        #conn.commit()
        sql = '''insert into rb_images(file_name, person_id, date,encodings) values("{}", "{}", "{}", '{}')'''
        sql = sql.format(file_name, person_id, date_time, encodings)
        #print(sql)
        db.query(sql)
        return jsonify({'person_id':person_id})

    
      

class Messanger(Resource):
    def post(self):
        db = DB()
        to_id = request.form['to_id']
        from_id = request.form['from_id']
        message = request.form['message']
        #conn = sqlite3.connect('Robot.db').cursor()
        date_time = str(datetime.datetime.now())
        print("test")
        sql = '''insert into rb_messages(from_id, to_id, message,status,date) 
                        values("{}","{}","{}","{}","{}")'''
        sql = sql.format(from_id, to_id, message, 'waiting', date_time)
        p = db.query(sql)
        print(p)
        #conn.execute("""insert into message(from_id, to_id, message, status, date) 
        #            values(?, ?, ?, ?, ?);""", (
        #            from_id, to_id, message, 'waiting', date_time))
        #conn.commit()



api.add_resource(Image, '/image/<image_id>')
api.add_resource(Message, '/message', '/message/<message_id>')
api.add_resource(User, '/user', '/user/<user_id>', '/user/<user_id>/<start>/<end>')
api.add_resource(People, '/people','/people/<person_name>','/people/<person_name>/<start>/<end>')
api.add_resource(Messanger,'/messanger')

if __name__ == '__main__':
     app.run(host='0.0.0.0', port='5002')



