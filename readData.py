class readData(object):
    def __init__(self):
        pass
    def read(self, fileName):
        fileRead = open(fileName, 'r')
        strRet = '['
        flag = False
        for i in fileRead:
            if flag:
                strRet += ', '
            strTmp = '['    
            tmp = i[:-1].split('\t')
            flag = False
            for j in tmp:
                if flag:
                    strTmp += ', '
                flag = True
                strTmp += j
            strTmp += ']'
            strRet += strTmp
        strRet += ']'
        print strRet