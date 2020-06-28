from jsonConverter.makeJsonFile import *
from groupingTool.clockWise.clockWiseGroup import *
import rbWindow.editWindow as ew
from parseSyllable.configSyllable import *
from mojo.UI import *
import os
import math
from mojo.extensions import getExtensionDefault, setExtensionDefault
from rbWindow.ExtensionSetting.extensionValue import *

class FileExist(Exception):
    def __init__(self,msg):
        self.msg = msg
        
    def __str__(self):
        return self.msg

def checkLanguage(CurrentFont):
    """
        현재 띄워져 있는 폰트의 첫번째 glyphOrder를 참고하여 한글 폰트인지 한자 폰트인지 판별한다.
        한자, 한글이 섞여있거나 첫번째 glyphOrder에 해당하는 글자에 이상이 있으면 정확한 판별이 되지 않는다.
        수행 도중 알 수 없는 이유로 에러가 나면 None으로 세팅
    """
    font = CurrentFont

    idx = 0
        
    #만약 ufo파일에 글자 수가 10개 미만인 경우 고려 + 첫번째 글리프 오더가 이상한 경우 고려
    for idx in range(min(len(font.glyphOrder),10)):
        try:
            int(font.glyphOrder[idx][3:],16)
            break
        except ValueError:
            continue    

    try:
        print(font.glyphOrder[idx][3:])
        if not 0xAC00 <= int(font.glyphOrder[idx][3:], 16) <= 0xD7A3:
            return False
        else:
            return True
    except Exception as e:
        print("언어(한글, 한자) 판별 중 예외가 발생했습니다.")
        print(e)


def StartProgram(testPath,testFile,CurrentFont):
    """
    프로그램 시작시 해당 폰트 파일이 처음일 경우 1차 필터링 세팅과 한글의 경우 음절분리 과정을 수행하여 .json파일로 저장하여 관리 
    """
    KoreanCheck = getExtensionDefault(DefaultKey+".korean")
    #한글일 떄만 해당 사항 적용
    #if KoreanCheck == True:
    #    MakeJsonController(testPath,testFile)


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

    #1차필터링
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
    #한글의 음절 분리 경우에만!
    if KoreanCheck is True:
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