import os
import jsonConverter.searchModule as search
import groupingTool.tMatrix.PhaseTool
import groupingTool.tMatrix.groupTestController
from groupingTool.tTopology import topologyJudgement as tj
from groupingTool.tTopology import topologyAssignment as ta
from groupingTool.tools import parseUnicodeControll as puc
import jsonConverter.converter as convert
from jsonConverter.smartSetSearchModule import *
from jsonConverter.clockWiseGroup import *
from parseSyllable.configSyllable import *
from mojo.UI import *
from rbWindow.ExtensionSetting.extensionValue import *
from rbWindow.Controller import smartSetFocus as sSF
from mojo.extensions import *

matrixMode = 0
topologyMode = 1

margin = 20
width = 100
k = 500

matrix_margin = 20
matrix_size = 3
topology_margin = 500

"""
2020/03/35 
modify by Kim Heesup Kim
"""

def getMatchGroupByMatrix(standardGlyph, contourIndex, margin, width, height, file,checkSetData,jsonFileName1,jsonFileName2):
	"""
	UI와 그룹 방법을 연결시켜주는 함수 (Matrix 방법)
	Args :
		standardGlyph :: RGlyph 
			기준 컨투어
		contourIndex ::  int
			컨투어의 번호
		margin :: int
			matrix로 반별시 오차 범위 허용 값(0 ~ 100)
			숫자가 높을수록 허용 범위가 넓어짐
			(20정도가 적당)
		width :: int
			매트릭스의 가로 구획 수
		height :: int
			매트릭스의 세로 구획 수
		file  :: RFont
			조사를 진행하고 있는 폰트 파일
		checkSetData :: List
			스마트셋 이름을 관리하기 위하여 필요한 checkSetData
			smartSetSearchModule 파일을 이용하여 구함
			[setNumber, syllableNumber]
		jsonFileName1 :: String
			시계방향, 반시계방향 정보를 담고 있는 json파일 이름(1차 필터링 결과)
		jsonFileName2 :: String
			음절 분리가 되어 있는 json파일 이름을 반환

	2020/03/23
	스마트셋 이름 규칙을 정리함
	set name format example
		: ##(number)_##(syllable)_####(mode)
	"""
	contour = standardGlyph.contours[contourIndex]

	standardMatrix = Matrix(contour,matrix_size)
	#k에 대한 마진값 적용하는 부분 넣어 주워야 함
	compareController = groupTestController(standardMatrix,matrix_margin)
	smartSetGlyphs = []
	smartSet = SmartSet()

	#추가부분
	with open(jsonFileName1, 'r') as jsonFile1:
	    resultDict = json.load(jsonFile1)

	with open(jsonFileName2, 'r') as jsonFile2:
		configDict = json.load(jsonFile2)

	standard = resultDict[standardGlyph.name][contourIndex]
	bar = ProgressBar('Matrix Process',len(resultDict),'Grouping...')
	barProcess = 0

	if checkSetData[1] == 0:
		smartSet.name = str(checkSetData[0]) + "_first_Matrix_" + "(" + str(standardGlyph.unicode) + "-" + str(contourIndex) + ")"
	elif checkSetData[1] == 1:
		smartSet.name = str(checkSetData[0])  + "_middle_Matrix_" +"(" + str(standardGlyph.unicode) + "-" + str(contourIndex) + ")"
	elif checkSetData[1] == 2:
		smartSet.name = str(checkSetData[0]) + "_final_Matrix_"+"(" + str(standardGlyph.unicode) + "-" + str(contourIndex) + ")"

	smartGroupDict = {}
	smartContourList = [] 
			

	for key, value in resultDict.items():
		barProcess += 1
		smartCheck = 0
		for i,compare in enumerate(value):
			if i not in configDict[key][checkSetData[1]]:#초, 중, 종 분리 로직
				continue
			if (standard['reverse'] == compare['reverse']) and (standard['forword'] == compare['forword']):
				compareContour = file[key].contours[i]
				result = compareController.conCheckGroup(compareContour)
				if result is not None:
					smartContourList.append(i)
					smartCheck = 1

		if smartCheck == 1:
			glyphUniName = file[key].name
			smartGroupDict[glyphUniName] = smartContourList
			smartSetGlyphs.append(glyphUniName)
			smartContourList = []
		if barProcess % 10 == 0:
			bar.tick(barProcess)

	bar.close()


	smartSet.glyphNames = smartSetGlyphs
	print("그룹화를 진행한 글리프 셋", len(smartSetGlyphs))
	addSmartSet(smartSet)
	updateAllSmartSets()	



def getMatchGroupByTopology(standardGlyph, contourIndex, k, file,checkSetData,jsonFileName1,jsonFileName2):
	"""
	2020/03/25
	modify by Kim heesup
	To get group contours Based on standard Glyph's contour by topology
	Args :
		standardGlyph :: RGlyph 
			기준 컨투어
		contourIndex ::  int
			컨투어의 번호
		k : int
			topology의 margin값 설정
		file  :: RFont
			조사를 진행하고 있는 폰트 파일
		checkSetData :: List
			스마트셋 이름을 관리하기 위하여 필요한 checkSetData
			smartSetSearchModule 파일을 이용하여 구함
			[setNumber, syllableNumber]
		jsonFileName1 :: String
			시계방향, 반시계방향 정보를 담고 있는 json파일 이름(1차 필터링 결과)
		jsonFileName2 :: String
			음절 분리가 되어 있는 json파일 이름을 반환

	2020/03/23
	스마트셋 이름 규칙을 정리함
	set name format example
		: ##(number)_##(syllable)_####(mode)				
	"""

	#추가부분
	with open(jsonFileName1, 'r') as jsonFile1:
		resultDict = json.load(jsonFile1)

	with open(jsonFileName2, 'r') as jsonFile2:
		configDict = json.load(jsonFile2)

	standard = resultDict[standardGlyph.name][contourIndex]

	bar = ProgressBar('Topology Process',len(resultDict),'Grouping...')
	barProcess = 0

	smartSetGlyphs = []
	smartSet = SmartSet()
	if checkSetData[1] == 0:
		smartSet.name = str(checkSetData[0]) + "_first_Topology_" +"(" + str(standardGlyph.unicode) + "-" + str(contourIndex) + ")"
	elif checkSetData[1] == 1:
		smartSet.name = str(checkSetData[0])  + "_middle_Topology_"+"(" + str(standardGlyph.unicode) + "-" + str(contourIndex) + ")"
	elif checkSetData[1] == 2:
		smartSet.name = str(checkSetData[0]) + "_final_Topology_"+"(" + str(standardGlyph.unicode) + "-" + str(contourIndex) + ")"
	smartGroupDict = {}
	smartContourList = [] 


	for key, value in resultDict.items():
		smartCheck = 0
		barProcess += 1
		for i,compare in enumerate(value):
			if i not in configDict[key][checkSetData[1]]:#초, 중, 종 분리 로직
				continue
			if (standard['reverse'] == compare['reverse']) and (standard['forword'] == compare['forword']):
				compareContour = file[key].contours[i]
				result = topologyJudgementController(standardGlyph.contours[contourIndex],compareContour,topology_margin).topologyJudgement()
				if result == True:
					smartContourList.append(i)
					smartCheck = 1

		if smartCheck == 1:
			glyphUniName = file[key].name
			smartGroupDict[glyphUniName] = smartContourList
			smartSetGlyphs.append(glyphUniName)
			smartContourList = []
		if barProcess % 10 == 0:
			bar.tick(barProcess)
			
	bar.close()

	smartSet.glyphNames = smartSetGlyphs
	addSmartSet(smartSet)
	updateAllSmartSets()


def handleSearchGlyphList(standardGlyph, contourIndex, file, mode, jsonFileName1, jsonFileName2, font, groupDict):
	"""
		2020/03/23
		created by H.W. Cho

		Get matching file and update currentWindow's group. If there is no matching file,
		search process will find a new group. Update view is followed at the end of process.

		Args::
			standardGlyph(RGlyph), contourIndex(int) : target object which want to search.
			file(RFont) : search area
			currentWindow(toolMenu object)

		2020/03/25
		modifyed by Kim heesup
		add smart set information

	"""
	checkSetData = searchGroup(standardGlyph,contourIndex,mode,file,True)

	print("checkSetData", checkSetData)
	if checkSetData[2] == 0:
		groupDict = findContoursGroup(checkSetData,file,mode)
		setExtensionDefault(DefaultKey + ".groupDict", groupDict)
		print("이미 그룹화가 진행된 컨투어입니다.")

	else:
		if mode is matrixMode:
			getMatchGroupByMatrix(standardGlyph, contourIndex, margin, width, width, file, checkSetData, jsonFileName1,jsonFileName2)
			groupDict = findContoursGroup(checkSetData, file,mode)
			setExtensionDefault(DefaultKey + ".groupDict", groupDict)

		elif mode is topologyMode:
			getMatchGroupByTopology(standardGlyph, contourIndex, k, font,checkSetData,jsonFileName1,jsonFileName2)
			groupDict = findContoursGroup(checkSetData, file, mode)
			setExtensionDefault(DefaultKey + ".groupDict", groupDict)

	#현재 스마트셋 포커싱
	smartSetIndex = sSF.getMatchingSmartSet(checkSetData, standardGlyph, contourIndex)
	
	sSF.updateSmartSetIndex(smartSetIndex)
	
def findContoursGroup(checkSetData, file, mode):
	"""
	json파일과 스마트 셋을 참고하여 이미 그룹화가 진행된 컨투어를 찾아냄
	Args :
		checkSetData :: List
			스마트셋 이름을 관리하기 위하여 필요한 checkSetData
			smartSetSearchModule 파일을 이용하여 구함
			[setNumber, syllableNumber]
		mainWindow :: object
			editWindow object
		mode :: int
		0 -> matrix , 1- > topology
	Returns :: Dictionary
		각각의 키는 같은 그룸의 컨투어를 포함하는 글리프, 값은 해당 컨투어의 번호를 저장 :: Dictionary
			key :: RGlyph
			value :: list
	"""


	ssets = getSmartSets()
	glyphList = list()
	res = dict()
	positionName  = None
	groupSet = None

	if mode == 0:
		modeName = "Matrix"
	else:
		modeName = "Topology"

	if checkSetData[1] == 0:
		positionName = "first"
	elif checkSetData[1] == 1:
		positionName = "middle"
	else:
		positionName = "final"


	for sset in ssets:
		nameList = str(sset.name).split('_')
		standardNameList = nameList[3].split('-')
		standardGlyphUnicode = int(standardNameList[0][1:])
		standardIdx = int(standardNameList[1][0:len(standardNameList[1])-1])
		if (nameList[0] == str(checkSetData[0])) and (nameList[1] == positionName) and (nameList[2] == modeName):
			groupSet = sset
			break


	for item in groupSet.glyphNames:
		glyphList.append(file[str(item)])


	for g in glyphList:
		searchContours = []
		for i,comc in enumerate(g.contours):
			if mode == 0:
				standardGlyph = file["uni" + str(hex(standardGlyphUnicode)[2:]).upper()]
				standardMatrix=Matrix(standardGlyph.contours[standardIdx],matrix_size)
				compareController = groupTestController(standardMatrix,matrix_margin)
				result = compareController.conCheckGroup(comc)
				if result is not None:
					searchContours.append(i)
			elif mode == 1:
				standardGlyph = file["uni" + str(hex(standardGlyphUnicode)[2:]).upper()]
				result = topologyJudgementController(standardGlyph.contours[standardIdx],comc,topology_margin).topologyJudgement()
				if result is not False:
					searchContours.append(i)
		res[g] = searchContours

	return res