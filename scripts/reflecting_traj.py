import rhinoscriptsyntax as rs

import random



class machine():



    def __init__(self,PTA,CRVS,DIST):



        ####MAX DIST####

        self.maxDist = DIST

        ####CLOSEST POINT###

        minDist = 5000000000000000000 #large number

        for crv in CRVS:

            if crv is not None:

                t = rs.CurveClosestPoint(crv, PTA)

                clPt = rs.EvaluateCurve(crv,t)

                dist = rs.Distance(PTA, clPt) #distance to closest point on each curve

                if dist < minDist: #if distance is smaller than last one

                    minDist = dist #set minDist to this one

                    clPt = clPt #set closest pt to this one

        ####POINT B####

        vec = rs.VectorCreate(PTA,clPt)#vector to closest point

        vec = rs.VectorUnitize(vec)

        zVec = rs.VectorCreate([0,0,1],[0,0,0])#Unit Z Vector NOT NECESSARY FOR 3D

        trans = rs.VectorRotate(vec,90,zVec)

        PTB = rs.CopyObject(PTA,trans) #end point for line



        ####################

        self.ptsA = [rs.PointCoordinates(PTA)] #list of points a

        self.idsA = [PTA] #list of ids a



        self.ptsB = [rs.PointCoordinates(PTB)] #list of points b

        self.idsB = [PTB] #list of ids b



        self.vecs = [vec] #list of direction vectors



        self.trailPts = [PTA] #list of trail points

        self.trails = []



        self.boundsCount = [] #empty list for number of times is far from start point

        ####################



    def reflection(self,CRV,POS1,POS2,ID,SCALE):



        scaleR = SCALE*2

        scaleP = 2000000

        #create intersection for point a

        t = rs.CurveClosestPoint(CRV,POS1)

        inx = rs.EvaluateCurve(CRV, t)

        inxL = rs.AddLine(POS1, inx)#line to intersect

        mirrorIntersections = rs.CurveCurveIntersection(inxL, CRV)#list of intersection results

        rs.DeleteObject(inxL) #delete line

        for mirrorInt in mirrorIntersections:

            inxP = mirrorInt[3] #intersection point

            inxT = mirrorInt[7] #parameter in CRV



            delList = []



            tan = rs.CurveTangent(CRV,inxT)#tangent vector

            tan = rs.VectorAdd(tan, inxP)#tangent at curve

            tan = rs.AddPoint(tan)#TANGENT ADD

            delList.append(tan)#Delete List Add



            zVec = rs.VectorCreate([0,0,1],[0,0,0])#Unit Z Vector NOT NECESSARY FOR 3D



            nor = rs.RotateObject(tan,inxP,90,zVec,copy=True)#rotate 90 degrees to get normal

            pt = rs.MirrorObject(ID,inxP,nor,copy=True)#mirror self using normal as plane info

            delList.append(nor)#Delete List Add

            delList.append(pt)#Delete List Add



            refl = rs.AddLine(inxP, pt)#line to intersect

            refl = rs.ScaleObject(refl,inxP,[scaleR,scaleR,scaleR])#scale

            delList.append(refl)#Delete List Add



            plane = rs.AddLine(POS1, POS2) #plane at direction of movement

            midPt = rs.VectorAdd(POS1, POS2)#midPoint of plane //add and divide

            midPt = rs.VectorDivide(midPt, 2)

            plane = rs.ScaleObject(plane,midPt,[scaleP,scaleP,scaleP])#scale plane to ensure intersection

            delList.append(plane)#Delete List Add



            reflIntersections = rs.CurveCurveIntersection(refl,plane)#list of intersection results



            if type(reflIntersections) == type([]):

                reflInt = rs.AddPoint(reflIntersections[0][3])#resulting reflection

            else: reflInt = rs.CurveEndPoint(refl)



            rs.DeleteObjects(delList)

            return reflInt



    def test(self,CRVS,TRAILS,FCT,MAX,INDEX,TRAILINDEX,RECU,INT):



        ####PTS 0####

        ptA0 = self.ptsA[-1] #assign point a info (last item on list)

        idA0 = self.idsA[-1]



        ptB0 = self.ptsB[-1] #assign point b info (last item on list)

        idB0 = self.idsB[-1]



        ####SEPARATION####

        if RECU > 0:

            SEPM = self.separationMirror(CRVS,INDEX,RanOfVis)#find closest Point

            if SEPM is None: SEPM = [0,0,0]

            SEPS = self.separationSelf(CRVS,INDEX)#find closest Point

            if SEPS is None: SEPS = [0,0,0]



        ####COHESION####

        if RECU > 0:

            COH = self.cohesion(TRAILS,TRAILINDEX,RanOfVis)

            if COH is None: COH = [0,0,0]

            if INT < div:

                COH = rs.VectorReverse(COH)



        ####PTS 1####

        CRV = self.findClosestCurve(CRVS,INDEX,RECU)#find closest Curve

        mirrorVec = self.vecToRefl(idA0, CRV)#vector to point of reflection in mirror

        scale = rs.VectorLength(mirrorVec)



        ptA1 = self.reflection(CRV, ptA0, ptB0, idA0, scale)#reflection point of point a

        ptB1 = self.reflection(CRV, ptB0, ptA0, idB0, scale) #reflection point of point b



        adjust = 1.00 #adjust for scaling (in case of no intersection)



        if rs.IsPoint(ptA1): ptA1=ptA1

        else:

            ptA1=rs.AddPoint(ptA1)

            adjust = adjust-0.25



        if rs.IsPoint(ptB1): ptB1=ptB1

        else:

            ptB1=rs.AddPoint(ptB1)

            adjust = adjust-0.25



        ####DISTANCE TESTS####

        dInc = rs.Distance(ptA0,ptB0) #distance point a to point b

        dRefl = rs.Distance(ptA1,ptB1)*adjust #distance in reflected points

        Test1 = rs.Distance(ptB0,ptA1) #test to check for inversion

        Test2 = rs.Distance(ptA0,ptA1) #test to check for inversion

        dStart = rs.Distance(self.ptsA[0],ptA0) #distance from start point



        rs.DeleteObject(ptA1) #delete reflected points

        rs.DeleteObject(ptB1) #delete reflected points



        ratio = dRefl/dInc #ratio of distortion

        ratio = 0.00000001 + ratio*FCT #scaling

        if ratio > MAX*FCT: ratio = MAX*FCT



        ####TRANSLATION####

        trans = rs.VectorCreate(ptB0, ptA0)#translation vector

        if unitizeCurrent == True: ##

            trans = rs.VectorUnitize(trans)



        if scaleCurrent == True: ##

            trans = rs.VectorScale(trans,ratio)



        vec = self.vecs[-1] #direction vector from previous translation



        if unitizePrevious == True: ##

            vec = rs.VectorUnitize(vec)



        trans = rs.VectorAdd(vec,trans)



        if unitizeResult == True: ##

            trans = rs.VectorUnitize(trans)



        ####DISTORTION STATES####

        #if dInc == dRefl: print "true reflection"



        if dInc < dRefl:

            #print "augmented reflection"

            trans = rs.VectorSubtract(trans, rs.VectorScale(rs.VectorUnitize(mirrorVec), ratio))



        if dInc > dRefl:

            #print "reduced reflection"

            trans = rs.VectorAdd(trans, rs.VectorScale(rs.VectorUnitize(mirrorVec), ratio))



        if rs.VectorLength(trans) > maxMove:

            trans = rs.VectorUnitize(trans)

            trans = rs.VectorScale(trans, maxMove)



        if Test1>Test2:

            #print "inversion"

            trans = rs.VectorReverse(trans)



        if dStart >= self.maxDist:

            #trans = -1*trans

            self.boundsCount.append(1)



        ####SUM VECTORS####

        if RECU > 0:

            mag = rs.VectorLength(trans)



            if rs.VectorLength(SEPM) > mag:

                SEPM = rs.VectorUnitize(SEPM)

                SEPM = rs.VectorScale(SEPM,mag)

            if rs.VectorLength(SEPS) > mag:

                SEPS = rs.VectorUnitize(SEPS)

                SEPS = rs.VectorScale(SEPS,mag)

            if rs.VectorLength(COH) > mag:

                COH = rs.VectorUnitize(COH)

                COH = rs.VectorScale(COH,mag)



            trans = rs.VectorAdd(SEPM, trans)

            trans = rs.VectorAdd(SEPS, trans)

            trans = rs.VectorAdd(COH, trans)

            trans = rs.VectorUnitize(trans)

            trans = rs.VectorScale(trans, mag)



        ###################

        self.vecs.append(trans)

        newPtA = rs.VectorAdd(ptA0, trans)

        self.ptsA.append(newPtA)

        tp = rs.AddPoint(newPtA)

        self.idsA.append(tp)



        newPtB = rs.VectorAdd(ptB0, trans)

        self.ptsB.append(newPtB)

        self.idsB.append(rs.AddPoint(newPtB))



        self.trailPts.append(tp)

        ###################



    def makeTrails(self,INDEX,RECU):

        if len(self.trailPts)>2:

            myTrailID = rs.AddInterpCurve(self.trailPts) #Control Pts Curve Trajectory

            self.trails.append(myTrailID)

            return myTrailID



    def vecToRefl(self, PT1, CRV):

        t = rs.CurveClosestPoint(CRV, PT1)

        clPt = rs.EvaluateCurve(CRV,t)

        vec = rs.VectorCreate(clPt, PT1)

        return vec



    def findClosestCurve(self, CRVS, INDEX, RECU):

        mycoord = self.ptsA[-1] #position at last item of ptsA list

        minDist = 5000000000000000000 #large number

        for crv in CRVS:

            if crv is not None:

                if RECU > 0 and crv is not CRVS[INDEX]:

                    t = rs.CurveClosestPoint(crv, mycoord)

                    clPt = rs.EvaluateCurve(crv,t)

                    dist = rs.Distance(mycoord, clPt) #distance to closest point on each curve

                    if dist < minDist: #if distance is smaller than last one

                        minDist = dist #set minDist to this one

                        closestCurve = crv #set closest crv to this one

                t = rs.CurveClosestPoint(crv, mycoord)

                clPt = rs.EvaluateCurve(crv,t)

                dist = rs.Distance(mycoord, clPt) #distance to closest point on each curve

                if dist < minDist: #if distance is smaller than last one

                    minDist = dist #set minDist to this one

                    closestCurve = crv #set closest crv to this one

                return closestCurve



    def separationMirror(self,CRVS, INDEX, RANGE):

        closestPt = 0

        mycoord = self.idsA[-1] #position at last item of ptsA list

        minDist = RANGE

        for crv in CRVS:

            if crv is not None:

                if crv is not CRVS[INDEX]:

                    t = rs.CurveClosestPoint(crv, mycoord)

                    clPt = rs.EvaluateCurve(crv,t)

                    dist = rs.Distance(mycoord, clPt) #distance to closest point on each curve

                    if dist < minDist: #if distance is smaller than last one

                        minDist = dist #set minDist to this one

                        closestPt = clPt #set closest point to this one

        if closestPt != 0:

            vec = rs.VectorCreate(mycoord, closestPt)

            vec = rs.VectorScale(vec, sepMFct)

            return vec

        else: return None



    def separationSelf(self,CRVS, INDEX):

        mycoord = self.idsA[-1] #position at last item of ptsA list

        minDist = 5000000000000000000 #large number

        for pt in self.idsA:

            if pt is not mycoord:

                dist = rs.Distance(mycoord, pt)#distance to each previous point

                if dist < minDist: #if distance is smaller than last one

                    minDist = dist #set minDist to this one

                    closestPt = pt #set closest point to this one

        vec = rs.VectorCreate(mycoord, closestPt)

        vec = rs.VectorScale(vec, sepSFct)

        return vec



    def cohesion(self,TRAILS,TRAILINDEX,RANGE):

        closestPt = 0

        mycoord = self.ptsA[-1] #position at last item of ptsA list

        minDist = RANGE #large number

        for crv in TRAILS:

            if crv is not TRAILS[TRAILINDEX]:

                t = rs.CurveClosestPoint(crv, mycoord)

                clPt = rs.EvaluateCurve(crv,t)

                dist = rs.Distance(mycoord, clPt) #distance to closest point on each curve

                if dist < minDist: #if distance is smaller than last one

                    minDist = dist #set minDist to this one

                    closestPt = clPt #set closest point to this one

        if closestPt != 0:

            vec = rs.VectorCreate(closestPt, mycoord)

            vec = rs.VectorScale(vec, cohFct)

            return vec

        else: return None



    def delete(self):

        self.idsA.pop(0)

        self.trails.pop()

        rs.DeleteObjects(self.idsA)

        rs.DeleteObjects(self.idsB)

        rs.DeleteObjects(self.trails)



def Main():

    rs.EnableRedraw(drawOn)



    baseListLen = len(reflcrvs)



    ####TRAILS####

    trails = []



    ####MACHINE CREATION####

    myMachines = []

    for i in range(len(startPos)):

        myMachines.append(machine(startPos[i],reflcrvs, dist))



    ####RUN TEST####

    count = 0

    interval = 0

    for i in range(int(recurrence)):

        j = 0

        for m in myMachines:

            #print j

            if len(m.boundsCount) > limit: break

            k = baseListLen+j

            m.test(reflcrvs,trails,amplitude,max,k,j,i,interval)

            trajectory = m.makeTrails(i,int(recurrence))#append resulting trajectory

            if i == 0:

                reflcrvs.append(trajectory)#append resulting trajectory

                trails.append(trajectory)

            reflcrvs[k] = trajectory

            trails[j] = trajectory

            j = j + 1

        interval = count % divisor

        count = count +1



    ################

    for m in myMachines:

        m.delete()

    ################



#################################################################################

drawOn = False

startPos = rs.GetObjects("Select Machine Locations", rs.filter.point, preselect=True) #Initial Position

reflcrvs = rs.GetObjects("Select Reflective Curves", rs.filter.curve) #Mirrors

####AMPLITUDE####

amplitude = 24 #Amplitude Scale

max = 10.0 #Max Amplitude

####BOUNDS####

limit = 500 #limit to kill

dist = 10000.0 #distance to kill

####SCALING FROM REFLECTION####

scaleCurrent = True

unitizeCurrent = False

unitizePrevious = True

unitizeResult = True

####SEPARATION & COHESION####

cohFct = 0.1

sepSFct = 0.3

sepMFct = 0.7



####GLOBALS######################################################################

recurrence = 2000

maxMove = 10.0

RanOfVis = 100.0

divisor = RanOfVis/maxMove*10

div = divisor/5

#################################################################################

Main()
