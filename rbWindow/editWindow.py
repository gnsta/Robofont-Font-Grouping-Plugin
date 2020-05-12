from defconAppKit.windows.baseWindow import BaseWindowController
from vanilla import EditText, FloatingWindow, CheckBox, Button, HelpButton, RadioGroup, HorizontalLine
from mojo.UI import MultiLineView, SelectGlyph, Message, setScriptingMenuNamingShortKeyForPath, createModifier, HelpWindow
import pathManager.pathSetting as extPath
from mojo.events import addObserver,removeObserver
from mojo.drawingTools import fill, oval, rect
from mojo.extensions import getExtensionDefault, setExtensionDefault
from rbWindow.contourPen import BroadNibPen
from rbWindow.sliderGroup import SliderGroup
#from rbWindow.addGroupWindow import AddGroupWindow
from rbWindow.toolMenu import toolsWindow
from rbWindow.attributeWindow import attributeWindow
from rbWindow.previewWindow import previewWindow
from rbWindow.settingWindow import settingWindow
from mojo.UI import CurrentFontWindow
from AppKit import *
from rbWindow.ExtensionSetting.extensionValue import *



def getMatchGroupDic(inputText, groupDict):
	"""
		2020/03/12
		created by H.W. Cho
		
		Param:
			- inputText(str)
			- groupDict(dict)
		Return:
			groupDict if inputText is in groupDict else None
			Can be used as check whether groupDict contians inputText or not.
	"""
	for key in groupDict.keys():
		if str(ord(inputText)) == str(key.unicode):
			return groupDict

	return None


def getContourListByDic(groupDic):
	"""
		2020/03/12
		created by H.W. Cho
		
		Param:
			- groupDict(dict)
		Return:
			- contourList(list) which glyphs' contourList of groupDict.

	"""
	contourList = []

	for glyph in groupDic.keys():
		for idx in groupDic[glyph]:
			contourList.append(glyph.contours[idx])

	return contourList


def getGlyphListByDic(groupDic):
	"""
		2020/03/12
		created by H.W. Cho

		Param:
			- groupDict(dict)
		Return:
			- glyphList(list)
	"""
	glyphList = []

	for glyph in groupDic.keys():
		glpyhList.add[glyph]

	return glyphList


def getMatchGroupDicByGlyph(inputGlyph, groupDict):
	"""
		2020/03/12
		created by H.W. Cho
		
		Param:
			- inputGlyph(RGlyph)
			- groupDict(dict)
		Return:
			if exists, groupDict(dict)
			else, None
	"""
	if inputGlyph in groupDict.keys():
		return groupDict
	
	return None

class EditGroupMenu(object):

	def __init__(self, font, file,jsonFileName1, jsonFileName2):
		
		self.font = font
		# self.groupDict = groupDict
		
		self.defaultKey = "com.robofontTool.rbFontGroup"

		self.selectedGlyphs = []                # Apply List Label을 통해 색칠된 글리프들을 다시 무채색으로 변환하기 위한 변수
		self.markColor = 0.3, 0.4, 0.7, 0.7
		self.state = False
		self.layerName = self.font.layerOrder[0]
		self.currentPen = None
		self.file = file
		self.window = None		# 현재 띄워져 있는 ufo 윈도우

		self.jsonFileName1 = jsonFileName1
		self.jsonFileName2 = jsonFileName2
		
		self.mode = None  		# 연산 방법(matrix, topology)
		self.w3 = None
		self.jsonFileName = jsonFileName

		self.createUI()
		self.color = None
		self.step = None
		self.width = None
		self.height = None
		self.shape = None
		self.angle = None
		self.keyDict = None


	"""
		UI 컴포넌트 부착
	"""
	def createUI(self):
		self.window = CurrentFontWindow()
		if self.window is None:
			return

		toolbarItems = self.window.getToolbarItems()
		print("dir(toolbarItems) = ", dir(toolbarItems))
		self.newToolbarItems = list()
		newItem1 = dict(itemIdentifier="Search", label="Search", imageNamed=NSImageNameRevealFreestandingTemplate, callback=self.popSearchWindow); self.newToolbarItems.append(newItem1);
		newItem2 = dict(itemIdentifier="Rewind", label="Rewind", imageNamed=NSImageNameRefreshFreestandingTemplate, callback=None); self.newToolbarItems.append(newItem2);
		newItem3 = dict(itemIdentifier="Save", label="Save", imageNamed=NSImageNameComputer, callback=None); self.newToolbarItems.append(newItem3);
		newItem4 = dict(itemIdentifier="Exit", label="Exit", imageNamed=NSImageNameStopProgressFreestandingTemplate, callback=self.windowCloseCallback); self.newToolbarItems.append(newItem4);
		newItem5 = dict(itemIdentifier="Settings", label="Settings", imageNamed=NSImageNameAdvanced, callback=self.popSettingWindow); self.newToolbarItems.append(newItem5);
		newItem6 = dict(itemIdentifier="Attribute", label="Attribute", imageNamed=NSImageNameFontPanel, callback=self.popAttributeWindow); self.newToolbarItems.append(newItem6);
		newItem7 = dict(itemIdentifier="Help", label="Help", imageNamed=NSImageNameInfo, callback=self.popManualWindow); self.newToolbarItems.append(newItem7);

		# add the new item to the existing toolbar
		for i in range(len(self.newToolbarItems)):
			toolbarItems.append(self.newToolbarItems[i])


		#toolbarItems.append(newItem7)
		# get the vanilla window object
		vanillaWindow = self.window.window()
		# set the new toolbaritems in the window
		self.window.toolbar = vanillaWindow.addToolbar(toolbarIdentifier="myCustomToolbar", toolbarItems=toolbarItems, addStandardItems=False)

		x = 10; y = 10; w = 280; h = 22; space = 5; size = (800, 600)

		addObserver(self, "drawBroadNibBackground", "drawBackground")

	def popManualWindow(self,sender):
		manual = extPath.resourcePath + "manual.html"
		print(manual)
		HelpWindow(htmlPath=manual)

	def popSettingWindow(self, sender):
		self.w6 = settingWindow(self)

	def popPreviewWindow(self, sender):

		self.w5 = previewWindow(self)
		self.w5.createUI(sender)
		
	def popAttributeWindow(self, sender):

		# Window for Assign & Remove Attribute
		mode = getExtensionDefault(DefaultKey + ".mode")
		contourNumber = getExtensionDefault(DefaultKey + ".contourNumber")
		if mode is None or contourNumber is None:
			print(Message("먼저 속성을 부여할 그룹을 찾아야 합니다."))
			return
		self.w4 = attributeWindow(self)


	def popSearchWindow(self, sender):

		# Window for Matrix & Topology Process
		self.w3 = toolsWindow(self)
		self.w3.createUI()

	def windowCloseCallback(self, sender):
	    
	    try:
	        for glyph in self.w3.selectedGlyphs:
	            glyph.markColor = None
	    except AttributeError:
	    	pass

	    try:
	    	removeObserver(self, "drawBackground")
	    	super(BroadNibBackground, self).windowCloseCallback(sender)
	    except NameError:
	    	pass

	    currentToolbarItems = self.window.getToolbarItems()

	    for i in range(7):
	    	currentToolbarItems.pop()

	    self.window.setToolbar()

	    del self
	

	def drawBroadNibBackground(self, info):

		# paint current group's contour
		targetGlyph = info["glyph"].getLayer(self.layerName)
		# picks current contours which should be painted from current group
		contourList = []

		try :
			file = getExtensionDefault(DefaultKey + ".file")
			targetIdxList = getExtensionDefault(DefaultKey+".groupDict")[targetGlyph]
			setExtensionDefault(DefaultKey + ".contourNumber", targetIdxList[0])

			# 칠할 필요가 없다면 해당 컨투어 번호만 세팅하고 종료
			if self.state is not 1:
				return

			r,g,b,a = self.color
			fill(r,g,b,a)

			if info["glyph"].layerName == self.layerName or not self.currentPen:
				self.currentPen = BroadNibPen(None, self.step, self.width, self.height, 0, oval)

			for idx in targetIdxList:
				targetGlyph.contours[idx].draw(self.currentPen)


		except Exception as e:
			setExtensionDefault(DefaultKey + ".contourNumber", None)
			return