from flask import Flask, request
from flask_restful import Resource, Api
#from sqlalchemy import create_engine
#from json import dumps
from flask_jsonpify import jsonify
import sqlite3
#from PIL import Image
#from io import BytesIO
import datetime
import base64


#db_connect = create_engine('sqlite:///../Robot.db')
app = Flask(__name__)
api = Api(app)

class Image(Resource):
    def	get(self, image_id):
        conn = sqlite3.connect('Robot.db').cursor()
        conn.execute("delete from image where id=?", (image_id,))


class Message(Resource):
    def get(self, message_id):
        conn = sqlite3.connect('Robot.db').cursor()
        conn.execute("delete from message where id=?", (image_id,))
        conn.commit()

    def post(self):
        message_id = request.form["message_id"]
        message = request.form["message"]
        conn = sqlite3.connect('Robot.db').cursor()
        conn.execute("update message set message=? where id=?", (message, message_id))
        conn.commit()


class User(Resource):
    def get(self, user_id, start=-1, end=-1):
        conn = sqlite3.connect('Robot.db').cursor()
        query = conn.execute("""select id, message from message
				where from_id=?""",(user_id, )).fetchall()
        if start == -1:
            count = len(query)
            return jsonify({'count':count})
        else:
            query = query[start:end]
            res = {id:mess for (id, mess) in query}
            return jsonify(res)

    def post(self):
        username = request.form["username"]
        password = request.form["password"]
        name = request.form["name"]
        new = request.form["new"]
        conn = sqlite3.connect('Robot.db').cursor()
        if new == "true":
            conn.execute("""insert into user(username, password, name)
                                   values(?,?,?)""", (username, password, name))
        query = conn.execute("""select id from user
                                where username=? and password=?""", (
                                username, password)).fetchall()
        if len(query) == 0:
            id = -1
        else:
            id = query[0]
        conn.commit()
        return jsonify({"user_id":query[0]})

		
class People(Resource):
    def get(self, person_name, start = -1, end = -1):
        conn=sqlite3.connect('Robot.db').cursor()
        if start == -1:
            count = conn.execute("select count(*) from person where name = ?",(person_name, )).fetchone()[0]
            print(count)
            return jsonify({'count':count})
        else:
            p_query = conn.execute("select id from person where name = ?",(person_name,)).fetchall()
            ids=[row[0] for row in p_query]
            ids = ids[int(start):int(end)]
            print(int(start))
            data={}
            for id in ids:
                 i_query = conn.execute("select file_name from image where person_id = ?",(id,)).fetchall()
                 if len(i_query) > 0:
                     with open(file_name, 'rb') as im:
                         encoded = base64.b64encode(im.read())
                         data[id] = encoded
        #result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
            return jsonify(data)

    def post(self):
        name = request.form['name']
        image = request.files.get("image")
        person_id = request.form['person_id']
        conn = sqlite3.connect('Robot.db').cursor()
        date_time = str(datetime.datetime.now())
        encodings = "1ghjk"
        if person_id == "":
            conn.execute("""insert into person(name) values(?)""", (name, ))
            person_id = conn.execute("""select id from person where name=?""", (name, )).fetchall()[-1]
        count = conn.execute("""select count(*) from image where person_id=?""", (
			person_id, )).fetchone()[0]
        file_name = str(person_id) + "_" + str(count) + ".jpg"
        image.save(file_name)
        conn.execute("""insert into image(file_name, person_id, date, encodings)
                         values(?, ?, ?, ?);""", (
                         file_name, to_id, date_time, encodings))
        conn.commit()
        return jsonify({'person_id':person_id})


class Messanger(Resource):
    def post(self):
        from_id = request.form['from_id']
        message = request.form['message']
        conn = sqlite3.connect('Robot.db').cursor()
        date_time = str(datetime.datetime.now())
        conn.execute("""insert into message(from_id, to_id, message, status, date) 
                    values(?, ?, ?, ?, ?);""", (
                    from_name, to_id, message, 'waiting', date_time))
        conn.commit()


api.add_resource(Image, '/image/<image_id>')
api.add_resource(Message, '/message', '/message/<message_id>') # Route_1
api.add_resource(User, '/user', '/user/<user_id>', '/user/<user_id>/<start>/<end>') # Route_2
api.add_resource(People, '/person','/person/<person_name>','/person/<person_name>/<start>/<end>') # Route_3
api.add_resource(Messanger,'/messanger')

if __name__ == '__main__':
     app.run(host='0.0.0.0', port='5002')
