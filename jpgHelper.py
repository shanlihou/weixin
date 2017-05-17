class jpgHelper(object):
    def __init__(self, fileName):
        self.fileRead = open(fileName, 'rb')
    def get2(self, num):
        bit = 128
        strRet = ''
        while bit:
            tmp = num % bit
            strRet += str(num / bit)
            num = tmp
            bit /= 2
        return strRet
    def parser(self):
        tmp = self.fileRead.read(4)
        for i in tmp:
            print '%x' % ord(i)
        tmp = self.fileRead.read(2)
        size = ord(tmp[0]) * 256 + ord(tmp[1])
        print 'size:', size
        tmp = self.fileRead.read(size)
        print tmp[:5]
        for i in tmp[5:7]:
            print ord(i)
        
        