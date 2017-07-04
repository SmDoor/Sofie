import sys
sys.path.append("..")
sys.path.append("../Faces")
from skimage import io
#import face_recognition
import os
import pykka
import sqlite3
import json
import numpy as np
import collections
import encodings
import requests
#import exceptions
from remote_recognizer import RemoteRecognizer

class DB:
	def __init__(self):
		self.conn = sqlite3.connect('../Robot.db')
		#self.conn.isolation_level = None		
		
	def query(self, sql):
		self.conn = sqlite3.connect('../Robot.db')
		print('test')
		res=self.conn.execute(sql).fetchall()
		print('test2')
		self.conn.commit()
		self.conn.close()
		return res

class FaceRecognizerActor(pykka.ThreadingActor):
         def __init__(self, url='', recievers={}):
                 super(FaceRecognizerActor, self).__init__()
                 self.db = DB()
                 self.recievers = recievers
                 self.url = url
                 sql = '''select to_id from rb_messages where status="waiting" or status="pending"'''
                 people = self.db.query(sql)
                 people = {id for (id,) in people}
                 data = {}
                 print(people)
                 for person in people:
                     sql = '''select encodings from rb_images where person_id="{}"'''
                     sql.format(person)
                     q = self.db.query(sql)
                     enc = [e[0] for (e,) in q]
                     enc = map(encodings.NP2Json.decode,enc)
                     data[person] = enc
                 self.recognizer = RemoteRecognizer(url, data)
                 print("FR: Init")

         def arr2json(arr): 
                 d=dict(enumerate(arr.flatten(), 1))
                 print(d)
                 json_enc = json.dumps(d, cls=MyEncoder)
                 print(json_enc)

                 return json_enc

         def json2arr(jsn):
                 json_decode = json.loads(jsn) 
                 js={int(k): v for k, v in json_decode.items()}
                 jsnd2 = collections.OrderedDict(sorted(js.items()))
                 list= [ v for v in jsnd2.values() ]

                 return np.array(list) 	
        
         def update(self):
                print('sddddddddddddd')
                sql = '''select to_id from rb_messages where status="waiting"'''
                q = self.db.query(sql)
                print(q)
                q = [p for (p,) in q]
                print(q)
                for person_id in q:
                    sql = '''select encodings from rb_images where person_id="{}"'''
                    sql = sql.format(person_id)
                    enc = self.db.query(sql)
                    enc = [e for (e,) in enc]
                    enc = map(encodings.NP2Json.decode,enc)
                    self.recognizer.add_person(person_id, enc)
                sql = '''update rb_messages set status="pending"
				where status="waiting"'''
                self.db.query(sql)

         def on_receive(self, message):
                print('recieve')
                if message['msg'] == 'Syn':
                       if message.get('recievers'):
                                self.recievers = message['recievers']
                elif message['msg'] == 'alive?':
                       print('update')
                       self.update()
                       print('updated')
#                elif message['msg']=='NewImage':
#                       if message.get('img_name') and message.get('person_id'):
#                                print('good')
#                                self.add_image_str(message['img_name'], message['person_id'])
#                elif message['msg']=='NewMessagee':
#                       print('Mess')
#                       if message.get('person_id'):
#                               self.add_person(message['person_id'])
                elif message['msg']=='Recognize':
                       print('rec')
                       if message.get('img_name'):
                                print('CCCCCCCCC')
                                res = self.recognizer.remote_recognize(message['img_name'])
                                return res




