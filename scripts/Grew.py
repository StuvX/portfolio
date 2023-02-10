import rhinoscriptsyntax as rs
import random
import math

#Growth Settings
mingrow = 0.1
maxgrow = 1.0
searchradii = 3
edgedecay = 1.0
mvpts = []


#Find points on mesh to grow
def MeshOptions(a,b,c,d,e,f,g,h,i,j,k):
    mo="_DetailedOptions _JaggedSeams={} _PackTextures={} ".format(a,b)
    mo+="_Refine={} _SimplePlane={} _AdvancedOptions _Angle={} ".format(c,d,e)
    mo+="_AspectRatio={} _Distance={} _Density={} _Grid={} ".format(f,g,h,i)
    mo+="_MaxEdgeLength={} _MinEdgeLength={} _Enter _Enter".format(j,k)
    return mo

def NClosestPoint(arrPoints, arrPoint, N):
    NclosestPoint = []
    arrTemp = arrPoints
    if N > 0 then:
        x = 0
        while x < (N+1):
            closest = rs.PointArrayClosestPoint(arrTemp,arrPoint)
            NclosestPoint.append(closest)
            arrTemp.remove(closest)
            x += 1
    return NclosestPoint

msg="Select surfaces or polysurfaces to mesh"
rs.GetObjects(msg,8+16,preselect=True,select=True)
rs.Command("_-Mesh "+MeshOptions("No","Yes","Yes","Yes",0,0,0.01,0,0,0,0))
lco=rs.LastCreatedObjects()
t_meshes=[rs.MeshQuadsToTriangles(obj) for obj in lco]
mvpts = rs.MeshVertices(lco)
if mvpts: rs.AddPointCloud(mvpts)

#Iterate over points, find x nearest points and determine growth vector - as product of all vectors from nearest point to point. Growth distance is random within bounds. Move point by vector x growth length
for x in mvpts:
    #create edge
    edge = rs.DuplicateMeshBorder(lco)
#    if rs.Dis
    #find neighbouring points within radius
    pushpts = rs.NClosestPoint(mvpts,x,searchradii)
    #create vectors
    #multiply vectors
    #calculate transform
    #calculate growth step
    #apply movement, vector x growthstep
