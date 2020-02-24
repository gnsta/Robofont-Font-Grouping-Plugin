def getMaxXValue(con):
    """
    create by Kim heesup

    Get maximum x value about contours
    
    Args:
        con : Rcontour
    Return:
        maximum x value
    """
    max = -100000
    for p in con.points:
        if(p.type != "offcurve"):
            if(max < p.x):
                max = p.x    
    return max

def getMinXValue(con):
    """
    create by Kim heesup

    Get minimum x value about contours
    
    Args:
        con : Rcontour
    Return:
        minimum x value
    """
    min = 100000
    for p in con.points:
        if(p.type != "offcurve"):
            if(min > p.x):
                min = p.x
    return min

def getMaxYValue(con):
    """
    create by Kim heesup

    Get maximum y value about contours
    
    Args:
        con : Rcontour
    Return:
        maximum y value
    """
    max = -100000
    for p in con.points:
        if(p.type != "offcurve"):
            if(max < p.y):
                max = p.y
    return max

def getMinYValue(con):
    """
    create by Kim heesup
    
    Get minimum y value about contours
    
    Args:
        con : Rcontour
    Return:
        minimum y value
    """
    min = 100000
    for p in con.points:
        if(p.type != "offcurve"):
            if(min >  p.y):
                min = p.y
    return min


class Matrix:
    """
    create by Kim heesup
    """
    
    def __init__(self,con,kx,ky):
        """
        Divide Matrix by x & y. Calculate how many number of points are in the specific area of matrix.
        """
        
        self.matrix= []
        
        
        for i in range(0,kx):
            self.matrix.append([])
            
        for i in range(0,len((self.matrix))):
            for j in range(0,ky):
                self.matrix[i].append(0)    
            
        
        #self.matrix = [[0]*ky for i in range(kx)]

        pl= []

        self.con = con
        self.kx = kx
        self.ky = ky
        

        for p in self.con.points:
            if(p.type != "offcurve"):
                pl.append(self.getPointPart(p))

        for li in pl:
            self.matrix[li[0]][li[1]] = self.matrix[li[0]][li[1]] + 1
            
                 
    def getKx(self):
        return self.kx 
    def getKy(self):
        return self.ky
    def getCon(self):
        return self.con            

    def getPointPart(self,p):
        """Get point's position if point's x is divided by kx and point's y is divided by ky.
    
        Args:
            p : Rpoint
        
            kx : dividing value of x
        
            ky : dividing value of y
        
        Return:
            point position
        """
    
        maxx = getMaxXValue(self.con) + 10
        minx = getMinXValue(self.con) - 10
        maxy = getMaxYValue(self.con) + 10
        miny = getMinYValue(self.con) - 10
    
        dis_x = maxx - minx
        dis_y = maxy - miny
    
        term_x = float(dis_x / self.kx)
        term_y = float(dis_y / self.ky)      
        
    
        compart_x = []
        compart_y = []
    
        compart_x.append(minx)
        compart_y.append(miny)
    
        num = 0
    
        while compart_x[num] + term_x < maxx:
            compart_x.append(compart_x[num] + term_x)
            num = num+1
        compart_x.append(maxx)

        num = 0
    
        while compart_y[num] + term_y < maxy:
            compart_y.append(compart_y[num] + term_y)
            num = num +1    
        compart_y.append(maxy)

    
        position_x = -1
        position_y = -1
    
        for i in range(0,len(compart_x)-1):
            if((compart_x[i] <= p.x)):
                position_x = i
            else:
                break
        
        for i in range(0,len(compart_y)-1):
            if((compart_y[i] <= p.y)):
                position_y = i
            else:
                break    
        
        rl = [position_x, position_y]
    
        return rl     
    
    
    def getPointCnt(self):
        res = 0
        for m in self.matrix:
            for j in m:
                res += j
        
        return res
        
    
    def getDivideStatus(self):
        """Get the number of point each case that points are arranged vertical or horizonal
    
        Args:       
            kx : dividing value of x
        
            ky : dividing value of y
        
        Return :
            list : [vertical arrange, horizonal arrange]     
        """
    
        point_stat = []
    
        rl = [[],[]]
    
        for i in range(0,self.kx):
            rl[0].append(0)
        
        for i in range(0,self.ky):
            rl[1].append(0)    
    
        for p in self.con.points:
            if(p.type != "offcurve"):
                point_stat.append(self.getPointPart(p))
    
        for st in point_stat:
            cx = st[0]
            cy = st[1]
        
            rl[0][cx] = rl[0][cx] + 1
            rl[1][cy] = rl[1][cy] + 1
        
        return rl