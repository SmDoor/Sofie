import sys
from skimage import io
import face_recognition
import encodings

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
		img_enc = face_recognition.face_encodings(image)
		if len(img_enc) == 0:
                        raise exceptions.NoFaceError
		if len(img_enc) > 1:
                        raise exceptions.ManyFacesError
		if person_id not in self.people:
                        self.people[person_id] = []
		self.people[person_id].append(img_enc[0])
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

	def add_person(self, person_id, encodings):
		if person_id not in self.people:
			self.people[person_id] = encodings
	
	@staticmethod
	def compare_encs(enc1, enc2):
		res = face_recognition.compare_faces(enc1, enc2)
		print(res)
		if True in res:
			return True
		return False
		
