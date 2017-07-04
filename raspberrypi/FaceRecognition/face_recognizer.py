import sys
from skimage import io
import face_recognition
import os
import pykka
import sqlite3
import json
import numpy as np
import collections

class FaceRecognizer:
	def __init__(self, people={}):
#people e dict s zapisi person_id:[encodings]
		self.people = people
		#for (name, image) in images.items():
		#	encoding = face_recognition.face_encodings(image)[0]
		#	self.people[name] = encoding

	@staticmethod
	def get_encodings(image):
		return face_recognition.face_encodings(image)

	@staticmethod
	def get_encodings_str(image_name):
		image = io.imread(image_name)
		return face_recognition.face_encodings(image)

	def add_image(self, person_id, image):
		if person_id not in self.people:
			self.people[person_id] = []
		img_enc = face_recognition.face_encodings(image)[0]
		self.people[person_id].append(img_enc)
		print(img_enc)
		return img_enc

	def add_image_str(self, person_id, image_name):
		image = io.imread(image_name)
		return self.add_image(person_id, image)

	def remove_image(self, person_id, image):
		if person_id in self.people:
			img_enc = face_recognition.face_encodings(image)[0]
			self.people[person_id].remove(img_enc)
			return True
		return False

	def remove_image_str(self, person_id, image_name):
		image=io.imread(image_name)
		return self.remove_image(person_id, image)

	def remove_person(self, person_id):
		if person_id in self.people:
			del self.people[person_id]
			return True
		return False

	def get_person_encodings(self, person_id):
		if person_id in self.people:
			return self.people[person_id]
		else:
			return None

	def recognize(self, image):
		encodings = face_recognition.face_encodings(image)
		return self.recognize_encs(encodings)

	def recognize_str(self, image_name):
		image = io.imread(image_name)
		return self.recognize(image)

	def recognize_encs(self, encodings):
                result = []
                for face_enc in encodings:
                        for (person, encs) in self.people.items():
                                res = face_recognition.compare_faces(
                                        encs, face_enc)
                                if True in res:
                                        result.append(person)
                return result

class DB:
	def __init__(self):
		self.conn = sqlite3.connect('Robot.db')
		#self.conn.isolation_level = None		
		
	def query(self, sql):
		self.conn = sqlite3.connect('Robot.db')
		print('test')
		res=self.conn.execute(sql).fetchall()
		print('test2')
		self.conn.commit()
		self.conn.close()
		return res

class FaceRecognizerActor(pykka.ThreadingActor):
         def __init__(self, img_dir='', actors=[]):
                 super(FaceRecognizerActor, self).__init__()
                 self.db = DB()
                 self.img_dir = img_dir
                 self.actors = actors
                 self.recognizer = FaceRecognizer()
                 #load all images from the db

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
        
         def add_image_str(self, img_name, person_id):
                enc=self.recognizer.add_image_str(person_id, img_name)
                print(enc)
                enc_json = self.arr2json(enc)
                print(enc_json)        
  
                sql='''INSERT INTO rb_images (file_name, date, encodings, person_id) VALUES ("{}", datetime(), "{}", "{}")'''
                sql=sql.format(img_name, enc_json, person_id) 
                print(sql)
                self.db.query(sql)		   
                   

         def on_receive(self, message):
                if message['msg']=='NewImage':
                       if message.get('img_name') and message.get('person_id'):
                               print('good')
                               self.add_image_str(message['img_name'], message['person_id'])
                        #TODO: Trqbva li drugiq actor da znae za vyzniknal problem?                                

actor_ref = FaceRecognizerActor.start()
actor_ref.tell({'msg':'NewImage', 'img_name':'images7/img3.jpg', 'person_id':'5'})

#f = FaceRecognizer()
#f.add_image_str(5, 'images7/img3.jpg')
#db=DB()
#enc=db.query('select encodings from rb_images where id=8')
#print(enc)
#enc=enc[0]
#res=f.recognize_encs(enc)
#print(res)

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        else:
            return super(MyEncoder, self).default(obj)

#arr = np.arange(10)
#print(arr)
#print(json.dumps(arr.toList()))
#d=dict(enumerate(arr.flatten(), 1))
#print(d)
#json_enc = json.dumps(d, cls=MyEncoder)
#print(json_enc)
#json_decode = json.loads(json_enc)
#map(int, json_decode.keys()) 
#js={int(k): v for k, v in json_decode.items()}
#jsnd2 = collections.OrderedDict(sorted(js.items()))
#print(jsnd2)
#list= [ v for v in d.values() ]
#list= [ v for v in jsnd2.values() ]
#print(np.array(list))
#print(json.loads(json_enc))
