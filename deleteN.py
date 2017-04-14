import sys
def deleteEnd(fileName):
    fileRead = open(fileName, 'r')
    fileWrite = open(fileName + 'w', 'w')
    for line in fileRead:
        fileWrite.writelines(line.replace('\n', '').replace('\r', '').replace(' ', ''))
def tab2Space(fileName):
    fileRead = open(fileName, 'r')
    fileWrite = open(fileName + 'w', 'w')
    for line in fileRead:
        fileWrite.writelines(line.replace('\t', '    '))
tab2Space(sys.argv[1])
        