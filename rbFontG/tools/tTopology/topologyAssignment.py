class topologicalRpoint:
    """
    create by Kim heesup
    """
    def __init__(self,point):
        """
        contain point, x phase ,and y phase
        """
        self.point = point
        self.x = -1
        self.y = -1
        
    def setX(self,num):
        self.x = num
    def setY(self,num):
        self.y = num
    def getX(self):
        return self.x
    def getY(self):
        return self.y        
            


class checkCon:
    """
    create by Kim heesup 
    """
    def __init__(self,con,k):
        """
        con : Rcontour
        
        pointList : Rcontour's Rpoint's list
        
        slist : Rpoint's list sorted by startPoint and clockwise(not include offcurve)
        
        tpPointList : topologicalRpoint's list sorted by startPoint and clockwise 
        """
        self.con = con
        self.k = k
        self.pointList = list(con.points)
        
        self.consistClockWise()
        self.slist = self.sortByStartingPoint()
        self.tpPointList = self.assignmentTopological(self.k) 
    
    def consistClockWise(self):
        """
        To be consisit contours clockwise if contour's clockwise False reverse the clockwise
        """
        
        if(self.con.clockwise == False):
            self.pointList.reverse()
            rp = self.pointList[-1]
            self.pointList.insert(0,rp)
            del(self.pointList[-1])
            
    def sortByStartingPoint(self):
        """
        sort by list's index 0 point has minimum y value. If  value same choose minimum x value

        Return: List
            sorted List
        """
        minY = 10000000000
        minX = 10000000000
        
        candidatePoints = []
        startPoint = None
        slist = []
        
        for i in range(0,len(self.pointList)):
            if(self.pointList[i].type != "offcurve"):
                if(minX > self.pointList[i].x):
                    minX = self.pointList[i].x
                
        for i in range(0,len(self.pointList)):
            if(self.pointList[i].type != "offcurve"):
                if(minX == self.pointList[i].x):
                    candidatePoints.append(self.pointList[i])
                
        for i in range(0,len(candidatePoints)):
            if(candidatePoints[i].type != "offcurve"):
                if(minY > candidatePoints[i].y):
                    minY = candidatePoints[i].y
                
        for i in range(0,len(candidatePoints)):
            if(candidatePoints[i].type != "offcurve"):
                if(minY == candidatePoints[i].y):
                    startPoint = candidatePoints[i]
                
                        
        num = -1
        for i in range(0,len(self.pointList)):
            if((startPoint.x == self.pointList[i].x) and (startPoint.y == self.pointList[i].y)):
                num = i;
                break;
                
        ll = self.pointList[i:len(self.pointList)]
        rl = self.pointList[0:i]
        
        offSlist = ll + rl
        #remove offCurvce
        for i in range(0,len(offSlist)):
            if(offSlist[i].type != "offcurve"):
                slist.append(offSlist[i])
        return slist
        
             
    def assignmentTopological(self,num):
        """
        Assign x phase ,and y phase and create topologicalRpoint object and make List

        Return: List
            topologicalRpoint object's List
        """
        sortByX = sorted(self.pointList,key = lambda RPoint: RPoint.x)
        sortByY = sorted(self.pointList,key = lambda RPoint: RPoint.y)
        
        sortByXNone = []
        sortByYNone = []
        tpRpl =[]
        
        idx = 1

        sortByXNone.append(sortByX[0])
        
        
        while(idx < len(sortByX)):
            if(sortByX[idx].x - sortByX[idx-1].x < num):
                sortByXNone.append(sortByX[idx])
                idx += 1
            else:
                sortByXNone.append(None)
                sortByXNone.append(sortByX[idx])
                idx += 1

        
        idx = 1

        sortByYNone.append(sortByY[0])
        
        
        while(idx < len(sortByY)):
            if(sortByY[idx].y - sortByY[idx-1].y < num):
                sortByYNone.append(sortByY[idx])
                idx += 1
            else:
                sortByYNone.append(None)
                sortByYNone.append(sortByY[idx])
                idx += 1
                           
                
        #assign topological
        for i in range(0,len(self.slist)):
            intpPoint = topologicalRpoint(self.slist[i])
            #assign x topological
            for j in range(0,len(sortByXNone)):
                if(sortByXNone[j] == None):
                    continue
                if((intpPoint.point.x == sortByXNone[j].x) and (intpPoint.point.y == sortByXNone[j].y)):
                    intpPoint.setX(j)
            #assign y topological
            for j in range(0,len(sortByYNone)):
                if(sortByYNone[j] == None):
                    continue
                if((intpPoint.point.x == sortByYNone[j].x) and (intpPoint.point.y == sortByYNone[j].y)):
                    intpPoint.setY(j)
            tpRpl.append(intpPoint)
            
        return tpRpl