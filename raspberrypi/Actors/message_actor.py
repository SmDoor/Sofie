import sys
sys.path.append("..")
sys.path.append("../Speaker")
import pykka
from Speaker import Speaker
from face_rec_actor import DB

class MessageActor(pykka.ThreadingActor):
	def __init__(self, recievers=[]):
		super(MessageActor, self).__init__()
		self.recievers = recievers
		self.db = DB()
		self.speaker = Speaker()
		print('DFGHJKL')

	def setRecievers(self, recievers):
		self.recievers = recievers

	def deliverMessages(self, person):
		print('DFGHJ')
		sql = '''select message, from_id from rb_messages 
			where to_id="{}" and (status="pending" or status="waiting")'''
		sql = sql.format(person)
		q = self.db.query(sql)
		messages = []
		for (m, p) in q:
			sql = '''select name from rb_users where id="{}"'''
			sql = sql.format(p)
			name = self.db.query(sql)[0][0]
			messages.append((name, m))
		sql = '''select name from rb_people where id = "{}"'''
		sql = sql.format(person)
		person_name = self.db.query(sql)[0][0]
		mess = '''Здравей, "{}"! Аз съм Софи и имам съобщения за теб'''
		mess = mess.format(person_name)
		self.speaker.speak(mess)
		for (name, message) in messages:
			mess = '''Съобщение от "{}".'''
			mess.format(name)
			self.speaker.speak(mess)
			self.speaker.speak(message)
		sql = '''update rb_messages set status="delivered" where person_id="{}"'''
		sql.format(person_id)
		self.db.query(person_id) 
		
	def on_receive(self, message):
		if message['msg'] == 'DeliverMessage':
			if message.get('people_ids'):
				people = message['people_ids']
				for person in people:
					self.deliverMessages(int(person))
				return 'delivered'
		return 'not delivered'



#a = MessageActor.start()
#print(type(a))
#a.tell({'msg':'DeliverMessage','people_ids':['1']})
