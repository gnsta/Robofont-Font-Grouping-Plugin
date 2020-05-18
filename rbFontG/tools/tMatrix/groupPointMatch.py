import copy
import math
from rbFontG.tools.tMatrix.PhaseTool import *
from fwig.tools import attributetools as at

def calcDirection(con,point):
	"""
	make compare point data's direction
	[up,down,left,right]
	"""

	dr = [10,-10,0,0]
	dc = [0,0,-10,10]

	#standard direction
	checkCdirection = [0,0,0,0]
	r = point.y
	c = point.x
	for i in range(0,4):
		nr = r + dr[i]
		nc = c + dc[i]
		if con.pointInside((nc,nr)):
			checkCdirection[i] = 1

	return checkCdirection


class matrixRelocatePoint:
	"""
	2020/02/24
	create by kim heesup
	"""
	def __init__(self,point,rx,ry,direction):
		"""
		contain RPoint, relocated x position, relocate y position
		"""
		self.point = point
		self.rx = rx
		self.ry = ry
		self.direction = direction

class groupPointMatchController:
	def __init__(self,matrix,point,con):
		"""
		controll match modify contour point and group contours point

		Args:
			matrix : standard contour

			point :  selected point

			con : contour that is included group 
		"""
		self.matrix = matrix
		self.point = point
		self.con = con

		self.standardCon = matrix.getCon()

	def matchPoint(self):
		"""
		match modify contour point and group contours point

		return:
			matched point

		example(if divided 3 by 3)
		-------------------------------------------------
		|		|		|2	3	|
		|		|	       4|1		|
		-------------------------------------------------
		|		|		|		|
		|		|		|		|
		-------------------------------------------------
		|		|		|		|
		|		|		|		|
		-------------------------------------------------

		if selected point is point 1

		point 2, point 3 and point 4 is group contour's points

		result is that point 1 and point 2 are match
		
		Because they are included same part and has shortest distance in the part
		"""	 
		pointPart = self.matrix.getPointPart(self.point)
		getStandardMaxMin = GetMaxMinPointValue(self.matrix.con)

		#find all point that contour's point that is located pointPart
		originpl = [] #original points

		relocatepl = []

		checkMatrix = Matrix(self.con,self.matrix.getdivk())
		getCompareMaxMin = GetMaxMinPointValue(checkMatrix.con)


		#additional mechanism
		dr = [10,-10,0,0]
		dc = [0,0,-10,10]

		#standard direction
		checkSdirection = [0,0,0,0]
		r = self.point.y
		c = self.point.x
		print("r : ",r)
		print("c : ", c)
		for i in range(0,4):
			nr = r + dr[i]
			nc = c + dc[i]
			print("i : ", i)
			print("nr : ", nr)
			print("nc : ",nc)
			if self.matrix.con.pointInside((nc,nr)):
				checkSdirection[i] = 1




		for p in self.con.points:
			if(p.type != 'offcurve'):
				checkPart = checkMatrix.getPointPart(p)
				if((pointPart[0] == checkPart[0]) and (pointPart[1] == checkPart[1])):
					originpl.append(p)



		#locate contour exactly matrix's contour
		#standardMinx = getStandardMaxMin.getMinXValue()
		standardMinx = self.matrix.con.bounds[0]
		#standardMiny = getStandardMaxMin.getMaxYValue()
		standardMiny = self.matrix.con.bounds[1]

		#checkMinx = getCompareMaxMin.getMinXValue()
		checkMinx = self.con.bounds[0]
		#checkMiny = getCompareMaxMin.getMaxYValue()
		checkMiny = self.con.bounds[1]


		termX = checkMinx - standardMinx
		termY = checkMiny - standardMiny

		#apply pl
		for p in originpl:
			rx = p.x - termX
			ry = p.y - termY
			checkCdirection = calcDirection(self.con,p)
			relocatepl.append(matrixRelocatePoint(p,rx,ry,checkCdirection))



		#get point that get minimum distance
		minDist = 10000000000
		indx = -1


		for	i,o in enumerate(relocatepl):
			if (o.direction[0] != checkSdirection[0]) or (o.direction[1] != checkSdirection[1]) or (o.direction[2] != checkSdirection[2]) or (o.direction[3] != checkSdirection[3]):
				continue

			print("비교 컨투어" , self.con)
			print("비교 점", o.point)
			print("기준 direction", checkSdirection)
			print("비교 direction", o.direction)
			dist = math.sqrt(math.pow(self.point.x - o.rx,2) + math.pow(self.point.y - o.ry,2))
			if(minDist > dist):
				indx = i
				minDist = dist

		if indx != -1:
			return relocatepl[indx].point
		else:
			return None

	def mgiveSelected(self):
		insertPoint = self.matchPoint()
		if insertPoint is not None:
			insertPoint.selected = True

	def mgiveAttrPenPair(self):
		insertPoint = self.matchPoint()
		if insertPoint is not None:
			temp = at.get_attr(self.point,'penPair')
			at.add_attr(insertPoint,'penPair',temp)

	def mgiveDependX(self):
		insertPoint = self.matchPoint()
		if insertPoint is not None:
			temp = at.get_attr(self.point,'dependX')
			at.add_attr(insertPoint,'dependX',temp)

	def mgiveDependY(self):
		insertPoint = self.matchPoint()
		if insertPoint is not None:
			temp = at.get_attr(self.point,'dependY')
			at.add_attr(insertPoint,'dependY',temp)

	def mgiveInnerFill(self):
		insertPoint = self.matchPoint()
		if insertPoint is not None:
			temp = at.get_attr(self.point,'innerFill')
			at.add_attr(insertPoint,'innerFill',temp)

	def mdeleteAttr(self,attribute):
		insertPoint = self.matchPoint()
		if insertPoint is not None:
			at.del_attr(insertPoint,attribute)		













