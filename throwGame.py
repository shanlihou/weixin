class throwGame(object):
    def __init__(self):
        self.mMap = [([0] * 256) for i in range(256)]
    def func(self, x):
        return x * x / (-64) + 4 * x
    def getFrame(self, times):
        y = self.func(times)
        #print times, y
        if y == 256:
            y = 255
        self.mMap[times][y] = 1
        strRet = ''
        strPrint = ''
        for i in range(256):
            for j in range(256):
                strRet += chr(self.mMap[j][255 - i])
            strPrint += '\n' 
        #print strPrint    
        return strRet
    def throw(self):
        imgList = []
        for i in range(256):
            imgList.append(self.getFrame(i))
        return imgList