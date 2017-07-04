import os
import exceptions

class Speaker:
	def __init__(self, lang='bg'):
		self.lang = lang

	def speak(self, text):
		res =  os.system('espeak -v'+self.lang+' "{0}"  > errro_log'.format(text))
		if res == 512:
			raise exceptions.UnknownLanguageError
		if res > 0:
			raise exceptions.SpeakError
