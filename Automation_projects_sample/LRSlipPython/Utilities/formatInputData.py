
def generateMap(filePath):
    file = open(filePath,mode='r')
    data = file.read()
    file.close()
    data = data.split("\n")
    key = data[0].split("|")
    value = data[1].split("|")
    return dict(zip(key,value))

