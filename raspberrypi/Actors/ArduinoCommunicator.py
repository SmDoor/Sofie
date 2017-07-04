import pykka
import serial
from Camerist import Camerist

class ArduinoCommunicator(pykka.ThreadingActor):
    def __init__(self):
        super(ArduinoCommunicator, self).__init__()
        try:
            self.connection = serial.Serial('/dev/ttyACM1')
        except:
            self.connection = serial.Serial('/dev/ttyACM1')
        self.actors = {}    
       
    def setReceivers(self, actors):
        print(actors)
        self.actors = actors

    def on_receive(self, message):
        #print(message)
        if message['msg']=='SYN':
            self.actors = message['receivers']
            self.connection.reset_input_buffer()
            self.actors['ard'].tell({'msg':'ME'})
            print(self.actors)
        elif message['msg']=='ME':
            if self.connection.in_waiting > 0 and self.actors.get('cm'):
                d = self.connection.readline().decode().strip()
                if(d=='STOPPED' and 'cm' in self.actors.keys()):
                    self.connection.write('WAIT'.encode())
                    self.actors['cm'].ask({'msg':'Action'})
                    self.connection.write("GO".encode())
            #print(self.connection.readline().decode().strip() + " GOOD!")
            self.actors['ard'].tell({'msg':'ME'})
        else:
            print('I am ArduinoCommunicator! I dont care what you want!')

 
#arduino_ref = ArduinoCommunicator.start()
#arduino_ref._actor.setReceivers({'cm':'123'})
     
#arduino_ref = ArduinoCommunicator.start()
#arduino_ref.setReceivers({'cm':camerist_ref})

#arduino_ref.test2()
#print('test')
#camerist_ref = Camerist.start()
#arduino_ref.tell({'msg':'SYN', 'receivers':{'cm':camerist_ref, 'ard':arduino_ref}})
#arduino_ref.setReceivers({'cm':camerist_ref})
