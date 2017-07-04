import pykka
from face_rec_actor import FaceRecognizerActor
from ArduinoCommunicator import ArduinoCommunicator
from Camerist import Camerist
from message_actor import MessageActor

class MasterActor(pykka.ThreadingActor):
	def __init__(self):
		self.classes = {'fr':'FaceRecognizerActor', 'ac':'ArduinoCommunicator','cm':'Camerist','ma':'MessageActor'}
		self.communication = {'fr':[], 'ac':['cm'], 'cm':['ac', 'fr'], 'ma':[]}
		self.actors = {}
		for (name, cls) in self.classes.items():
			class_n = globals()[cls]
			self.actors[name] = class_n.start()
		for name in self.actors.keys():
			com = {a:self.actors[a] for a in communication[name]}
			self.actors[name].tell({'msg':'Syn','recievers':com})
		for name in self.actors.keys():
			try:
				actors[name].tell({'msg':'alive?'})
			except pykka.ActorDeadError:
				class_n = globals()[classes[name]]
				com = {a:self.actors[a] for a in communication[name]}
				self.actors[name] = class_n.start() 
				self.actors[name].tell({'msg':'Syn','recievers':com})
				for name2 in self.actors.keys():
					if name in communication[name2]:
						com = {a:self.actors[a] for a in communication[name2]}
						self.actors[name2].tell({'msg':'Syn','recievers':com})


m = MasterActor()
