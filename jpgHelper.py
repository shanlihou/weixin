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
    def parseFFC0(self):
        print 'parseFFC0---------------------------------------'
        tmp = self.fileRead.read(2)
        size = ord(tmp[0]) * 256 + ord(tmp[1])
        print 'size:', size
        tmp = self.fileRead.read(size - 2)
        print ord(tmp[0])
        print 'high:', ord(tmp[1]) * 256 + ord(tmp[2])
        print 'width:', ord(tmp[3]) * 256 + ord(tmp[4])
        print ord(tmp[5])
        count = 0
        for i in tmp[6:]:
            count += 1
            print self.get2(ord(i))
            if count == 3:
                count = 0
                print '\n'
    def parseFFC4(self):#dht    
        print 'parseFFC4---------------------------------------'
        tmp = self.fileRead.read(2)
        size = ord(tmp[0]) * 256 + ord(tmp[1])
        print 'size:', size
        tmp = self.fileRead.read(size - 2)
        print self.get2(ord(tmp[0]))
        count = 0
        for i in range(16):
            print i,':', ord(tmp[1 + i])
            count += ord(tmp[1 + i])
        print count
    def parseFFDB(self):
        print 'parseFFDB---------------------------------------'
        tmp = self.fileRead.read(2)
        size = ord(tmp[0]) * 256 + ord(tmp[1])
        print 'size:', size
        tmp = self.fileRead.read(size - 2)
        print ord(tmp[0])
        print self.get2(ord(tmp[0]))
    def parseFFDA(self):
        print 'parseFFDA---------------------------------------'
        tmp = self.fileRead.read(2)
        size = ord(tmp[0]) * 256 + ord(tmp[1])
        print 'size:', size
        tmp = self.fileRead.read(size - 2)
        flag = 0
        while 1:
            tmp = ord(self.fileRead.read(1))
            if flag == 0:
                if tmp == 0xff:
                    flag = 1
            else:
                if tmp == 0xff:
                    continue
                elif tmp == 0xd9:
                    break
                elif tmp >= 0xd0 and tmp <= 0xd7:
                    print tmp
                    flag = 0
                else:
                    flag = 0
    def parseFlag(self):
        while 1:
            flag = self.fileRead.read(1)
            if not flag:
                break
            flag = ord(flag)
            print '%x' % flag
            if flag == 0xff:
                flag = ord(self.fileRead.read(1))
                print '%x' % flag
                if flag == 0xdb:
                    self.parseFFDB()
                elif flag == 0xc0:
                    self.parseFFC0()
                elif flag == 0xc4:
                    self.parseFFC4()
                elif flag == 0xda:
                    self.parseFFDA()
                else:
                    break
            else:
                break
    def parser(self):
        tmp = self.fileRead.read(4)
        for i in tmp:
            print '%x' % ord(i)
        tmp = self.fileRead.read(2)
        size = ord(tmp[0]) * 256 + ord(tmp[1])
        print 'size:', size
        tmp = self.fileRead.read(size - 2)
        print tmp[:5]
        print 'ver:', str(ord(tmp[5])) + '.' + str(ord(tmp[6]))
        print ord(tmp[7])
        print 'x:', ord(tmp[8]) * 256 + ord(tmp[9])
        print 'y:', ord(tmp[10]) * 256 + ord(tmp[11])
        for i in tmp[12:]:
            print '%x' % ord(i)
        self.parseFlag()