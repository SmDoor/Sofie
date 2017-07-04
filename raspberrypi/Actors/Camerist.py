import sys
sys.path.append("..")
from config import Config
import pykka
import picamera
import time

class Camerist(pykka.ThreadingActor):
    def __init__(self):
        super(Camerist, self).__init__()
        self.actors = []
        self.img_dir = Config.getImgDir()
        self.camera = picamera.PiCamera()

    def setReceivers(_actors):
        self.actors = _actors    

    def on_receive(self, message):
        if message['msg']=='Action':
            print('Wait! I am taking a photo!'+'\n')
            #camera = picamera.PiCamera()
            img_name = self.img_dir + '/' + str(int(time.time())) + '.jpg'
            #img_name = 'test35.jpg'
            print(img_name)
            self.camera.capture(img_name)
            print(img_name+'\n')
            if self.actors.get('fr'):
                res = self.actors['fr'].ask({'msg':'Recognize', 'img_name':img_name})
                if len(res)>0:
                    self.actors['ma'].ask({'msg':'DeliverMessage', 'people_ids':res})
            return 'Done'
        else:
            print('I am Camerist! I dont care what you want!')

#camerist_ref = Camerist.start()
#camerist_ref.tell({'msg':'Action'})
