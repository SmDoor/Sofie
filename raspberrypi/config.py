class Config():    
    img_dir = '/home/gss9/robot/Actors/images'

    @staticmethod
    def getImgDir():
        return Config.img_dir

print(Config.getImgDir())
