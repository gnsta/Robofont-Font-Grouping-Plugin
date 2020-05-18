from jsonConverter.makeJsonFile import *
from jsonConverter.clockWiseGroup import *
import rbWindow.editWindow as ew
from parseSyllable.configSyllable import *
from mojo.UI import *
import os
import math

class FileExist(Exception):
    def __init__(self,msg):
        self.msg = msg
        
    def __str__(self):
        return self.msg

def StartProgram(testPath,testFile):
    MakeJsonController(testPath,testFile)
    insert = dict()
    barProcess = 0

    jsonFileName1 = None
    jsonFileName2 = None

    
    tempFileName = testPath.split('/')[-1]
    if tempFileName.split('.')[1] == 'ufo':
        bar = ProgressBar('start',len(testFile) * 2,'initial setting...')
        barProcess = 0
    else:
        bar = ProgressBar('start',len(testFile),'initial setting...')
        barProcess = 0

    try:
        jsonFileName1 = os.path.dirname(os.path.abspath(__file__)) + '/jsonResource/' + tempFileName.split('.')[0] + '.json'
        if os.path.exists(jsonFileName1):
            raise FileExist('해당 파일은 이미 존재합니다')
        for tg in testFile:
            barProcess += 1
            tempList = list()
            for tc in tg.contours:
                compare = getClockWiseList(tc)
                tempList.append(compare)
            insert[tg.name] = tempList
            if barProcess % 10 == 0:
                bar.tick(barProcess)     
        with open(jsonFileName1,'w',encoding = 'utf-8') as make_file:
            json.dump(insert,make_file,indent = '\t')
    except FileExist as e:
        print(e)


    insert = dict()
    if tempFileName.split('.')[1] == 'ufo':
       try:
            tempFileName = testPath.split('/')[-1]
            jsonFileName2 = os.path.dirname(os.path.abspath(__file__)) + '/jsonResource/' + tempFileName.split('.')[0] + '_config.json'
            if os.path.exists(jsonFileName2):
                raise FileExist('해당 파일은 이미 존재합니다')
            for tg in testFile:
                barProcess += 1
                tempDict = getConfigure(tg)
                insert[tg.name] = tempDict[str(tg.unicode)]
                if barProcess % 10 == 0:
                    bar.tick(barProcess)     
            with open(jsonFileName2,'w',encoding = 'utf-8') as make_file:
                json.dump(insert,make_file,indent = '\t')
       except FileExist as e:
            print(e) 
    
    bar.close()

    return [jsonFileName1,jsonFileName2]