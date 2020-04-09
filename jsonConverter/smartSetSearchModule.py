from mojo.UI import *
from parseSyllable.configSyllable import *
import json
import os
from rbFontG.tools.tMatrix.PhaseTool import *
from rbFontG.tools.tMatrix.groupTestController import *
from rbFontG.tools.tTopology.topologyJudgement import *
from rbFontG.tools.tTopology.topologyAssignment import *

"""
2020/03/25
create By Kim heesup
"""

baseDir = "/Users/font/Desktop/GroupDict/"

def searchGroup(glyph,contourNumber,mode,mainWindow,message = False):
	"""
	check that contour group is created
	if exist return file number else return None
	Args:
		glyph :: Rglyph
		contourNumber :: int
			contour that is being searched
		mode :: int
			0 - > matrix , 1-> topology
		
		jsonFileName :: Stirng
			file name that include data about contour group name
		mainWindow :: tool Menu object
			to get font File
	Return :: List
		contain fileNumber and syllable and last data is checkdata(if 0 -> grouped , 1 -> not grouped)
		수정부분 : json 파일로 찾지 말고 set 이용하여 해결
	"""

	glyphConfigure = getConfigure(glyph)

	check = 0
	positionNumber = None
	searchSmartSet = None
	#해당 컨투어가 초성인지 중성인지 종성인지 확인을 해 보아햐함
	#!!
	for i in range(0,len(glyphConfigure[str(glyph.unicode)])):
		for j in range(0,len(glyphConfigure[str(glyph.unicode)][i])):
			if contourNumber == glyphConfigure[str(glyph.unicode)][i][j]:
				check = 1
				positionNumber = i
				break

		if check == 1:
			break

	if mode == 0:
		setStat = getSmartSetStatMatrix()
		print("현재 스마트 셋의 상태 : ", setStat)
		searchMode = "Matrix"
	elif mode == 1:
		setStat = getSmartSetStatTopology()
		print("현재 스마트 셋의 상태 : ", setStat)
		searchMode = "Topology"

	if positionNumber == 0:
		positionName = "first"
	elif positionNumber == 1:
		positionName = "middle"
	else:
		positionName = "final"



	sSets = getSmartSets()
	glyphNames = list()
	check = 0

	for sSet in sSets:
		checkSetName = str(sSet.name)
		checkSetNameList = checkSetName.split('_')
		if checkSetNameList[1] != positionName or checkSetNameList[2] != searchMode:
			continue
		#검사를 진행을 해야함(기준 컨투어는 알고 있고 비교 글리프에 있는 컨투어는 순회를 하면서 조사하는 방식)
		#matrix 체크에서는 같은 그룹이 아니면 None이고 topology 에서는 같은 그룹이 아니면 flase반환
		print("checkSetNameList : ",checkSetNameList)
		standardNameList = checkSetNameList[3].split('-')
		standardGlyphUnicode = int(standardNameList[0][1:])
		standardIdx = int(standardNameList[1][0:len(standardNameList)-1]) 
		for item in sSet.glyphNames:
			#if item != glyph.name:
				#continue
			if mode == 0:
				standardGlyph = mainWindow.file["uni" + str(hex(standardGlyphUnicode)[2:]).upper()]
				#width값은 정해져 있다고 생각을 하고 진행
				standardMatrix=Matrix(standardGlyph.contours[standardIdx],10)
				compareController = groupTestController(standardMatrix,0)
				result = compareController.conCheckGroup(glyph[contourNumber])
				if result is not None: 
					searchSmartSet = sSet
					check = 1
					break
			elif mode == 1:
				standardGlyph = mainWindow.file["uni" + str(hex(standardGlyphUnicode)[2:]).upper()]
				result = topologyJudgementController(standardGlyph.contours[standardIdx],glyph[contourNumber],500).topologyJudgement()
				if result is not False: 
					searchSmartSet = sSet
					check = 1
					break
					
		if check == 1:
			break

	print("searchSmartSet",searchSmartSet)

	#glyphUniName =  "uni" + hex(glyph.unicode)[2:].upper()

	#fileNumber = json_data[glyphUniName][str(contourNumber)]

	if searchSmartSet is not None:
		#팝업창으로 띄워주면 좋을 부분
		if message == True:
			print(Message("이미 그룹 연산이 진행이 되어 있으므로 그룹화 작업을 생략합니다."))
		return [checkSetNameList[0],positionNumber,0]
	else:
		if positionNumber == 0:
			appendNumber = setStat["first"] + 1
		elif positionNumber == 1:
			appendNumber = setStat["middle"] + 1
		elif positionNumber == 2:
			appendNumber = setStat["final"] + 1

		#json_data[glyphUniName][positionNumber] = appendNumber

		return [appendNumber,positionNumber,1]

def setGroup(glyph,contourNumber,mode,jsonFileName,appendNumber):
	"""
	store group information about glyph's contour to json File
	(Not Using)
	Args:
		glyph :: Rglyph
		contourNumber :: int
			glyph's contour number
		mode :: int
			0 - > matrix , 1-> topology
		
		jsonFileName :: Stirng
			file name that include data about contour group name
		appendNumber :: int
			setNumber
	"""

	if mode == 0:
		searchFileName = "Matrix"
	elif mode == 1:
		searchFileName = "Topology"


	glyphUniName =  "uni" + hex(glyph.unicode)[2:].upper()

	with open(baseDir + searchFileName, 'r') as f:
		json_data = json.load(f)


	json_data[glyphUniName][str(contourNumber)] = appendNumber

	with open(baseDir + searchFileName,'w',encoding = 'utf-8') as make_file:
		json.dump(json_data,make_file,indent = '\t')



	
def getSmartSetStatMatrix():
	"""
	check minimum file number according to syllable
	set name format example
		:##(number)_##(syllable)_####(mode)
	"""

	matrixSetStat = {"first" : 0, "middle" : 0 , "final" : 0}

	firstl = list()
	middlel = list()
	finall = list()

	setList = getSmartSets()

	for sl in setList:
		setName = sl.name
		setNameList = setName.split('_')
		modeName = setNameList[2]
		setNumber = int(setNameList[0])
		setSyllable = setNameList[1]

		if modeName ==  "Matrix":
			#matrixSetStat[setSyllable] += 1
			if setSyllable == "first":
				firstl.append(setNumber)
			elif setSyllable == "middle":
				middlel.append(setNumber)
			elif setSyllable == "final":
				finall.append(setNumber)

	firstl.sort()
	middlel.sort()
	finall.sort()

	check = 0 
	for i in range(0,len(firstl)):
		if (i +1) != firstl[i]:
			matrixSetStat["first"] = i
			check = 1
	if check == 0:
		matrixSetStat["first"] = len(firstl)

	check = 0 
	for i in range(0,len(middlel)):
		if (i +1) != middlel[i]:
			matrixSetStat["middle"] = i
			check = 1
	if check == 0:
		matrixSetStat["middle"] = len(middlel)

	check = 0 
	for i in range(0,len(finall)):
		if (i +1) != finall[i]:
			matrixSetStat["final"] = i
			check = 1
	if check == 0:
		matrixSetStat["final"] = len(finall)

	return matrixSetStat



def getSmartSetStatTopology():
	"""
	check how many set about topology
	not count other
	set name format example
		:##(number)_##(syllable)_####(mode)
	"""

	topologySetStat  = {"first" : 0 , "middle" : 0 , "final" : 0}

	firstl = list()
	middlel = list()
	finall = list()

	setList = getSmartSets()

	for sl in setList:
		setName = sl.name
		setNameList = setName.split('_')
		modeName = setNameList[2]
		setNumber = int(setNameList[0])
		setSyllable = setNameList[1]

		if modeName == "Topology":
			#topologySetStat[setSyllable] += 1
			if setSyllable == "first":
				firstl.append(setNumber)
			elif setSyllable == "middle":
				middlel.append(setNumber)
			elif setSyllable == "final":
				finall.append(setNumber)


	firstl.sort()
	middlel.sort()
	finall.sort()

	check = 0 
	for i in range(0,len(firstl)):
		if (i +1) != firstl[i]:
			topologySetStat["first"] = i
			check = 1
	if check == 0:
		topologySetStat["first"] = len(firstl)

	check = 0 
	for i in range(0,len(middlel)):
		if (i +1) != middlel[i]:
			topologySetStat["middle"] = i
			check = 1
	if check == 0:
		topologySetStat["middle"] = len(middlel)

	check = 0 
	for i in range(0,len(finall)):
		if (i +1) != finall[i]:
			topologySetStat["final"] = i
			check = 1
	if check == 0:
		topologySetStat["final"] = len(finall)

	return topologySetStat