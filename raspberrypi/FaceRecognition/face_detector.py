import sys
import dlib
from skimage import io
from skimage import draw

class FaceDetector:
	def __init__(self):
		self.detector = dlib.get_frontal_face_detector()

	def get_faces(self, image):
                detected_faces = self.detector(image,1)
                return detected_faces

	def find_face(self, image):
		detected_faces = self.get_faces(image)
		return (len(detected_faces) > 0)

	def get_faces_str(self, image_name):
		image = io.imread(image_name)
		return self.get_faces(image)

	def find_face_str(self, image_name):
		detected_faces = self.get_faces_str(image_name)
		return (len(detected_faces) > 0)

	def mark_faces(self, image, color=(255, 0, 0)):
                detected_faces = self.get_faces(image)
                output_image = image.copy()
                for face in detected_faces:
                        rr,cc = draw.polygon_perimeter(
                                [face.top(), face.top(),
                                face.bottom(), face.bottom()],
                                [face.right(), face.left(),
                                face.left(), face.right()])
                        output_image[rr, cc] = color
                return output_image

	def mark_faces_str(self, image_name, output_name, color=(255, 0, 0)):
                image = io.imread(image_name)
                output_image = self.mark_faces(image, color)
                io.imsave(output_name, output_image)



