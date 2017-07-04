import sys
sys.path.append("..")
import face_recognizer
import exceptions
import encoding
import requests

class RemoteRecognizer(face_recognizer.FaceRecognizer):
	def __init__(self, url, people={}):
		super(RemoteRecognizer, self).__init__(people)
		self.url = url

	def remote_get_encodings(self, img_name):
		try:
			print('remote')
			url1 = self.url + '/encodings'
			files = {'image':open(img_name,'rb'),'ContentType':'image/jpeg'}
			r = requests.post(url1, files = files)
			enc = r.json()
			enc = encoding.NP2Json.decode(enc)
			print('remote')
		except:
			print('not remote')
			enc = self.get_encodings_str(img_name)
		#if count==0:
			#raise exceptions.NoFaceError
		#if count >1:
			#raise exceptions.ManyFacesError
		return enc

	def remote_recognize(self, img_name):
		try:
			print('BBBBBBBBBBBBB')
			encs = self.remote_get_encodings(img_name)
			url2 = self.url + '/recognize'
			res = []
			print(encs)
			for enc1 in encs:
				for person in self.people.keys():
					for enc2 in self.people[person]:
						r = requests.post(url2, data={'enc1':enc2, 'enc2':[enc1]})
						r = r.json()
						if r['res'] == 'True':
							res = res.append(person)
							break
			return res
		except:
			print('AAAA')
			return self.recognize_str(img_name)	

