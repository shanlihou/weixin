class logWeixin(object):
    def __init__(self):
        pass
    @staticmethod
    def log(fileName, data):
        fileWrite = open(fileName + '.txt', 'w')
        fileWrite.write(data)