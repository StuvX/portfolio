#rhinoscript for drawing wood floor designed to reflect light to focal point
import rhinoscriptsyntax as rs
import math
from Rhino.Geometry import Point3d
intX = 0 # initialise X to zero
intY = 0 # init Y to zero
intZ = 0 # init Z to zero
fltD = 0 # distance from origin
FCL = 2.4
dblRmLngth = 4.510 # room depth from window
unit = 0.05 #thickness of wood members
diag = math.sqrt(unit*unit+unit*unit)
overhang = 0.510 #length of overhang, should be length of opp for highest sun angle
wedge = 0.01
SMR = 10
inc = 0.003
zee = wedge
# class drwbase()
while fltD < dblRmLngth :
    STRT = [intX,intY,intZ]
    TWO = [intX+unit,intY,intZ]
    THREE = [intX+unit,intY+unit,intZ]
    FOUR = [intX,intY+unit,intZ]
    #    rs.AddSrfPt([STRT,TWO,THREE,FOUR])
    fltD = rs.Distance([0,0,0],THREE)
    if fltD < SMR :
        h = (fltD+overhang-diag)*diag/(FCL+wedge)
        CERO = [intX,intY,wedge]
        DOS = [intX+unit,intY,h*0.5+wedge]
        TRES = [intX+unit,intY+unit,h+wedge]
        QUATRO = [intX,intY+unit,h*0.5+wedge]
    else :
        h = (SMR+overhang-diag)*diag/FCL
        zee = zee + inc
        zed = min(h,zee)
        CERO = [intX,intY,zed+wedge]
        DOS = [intX+unit,intY,zed+(h-zed)/2+wedge]
        TRES = [intX+unit,intY+unit,h+wedge]
        QUATRO = [intX,intY+unit,zed+(h-zed)/2+wedge]
#    rs.AddSrfPt([STRT,DOS,TRES,QUATRO])
    rs.AddBox([STRT,TWO,THREE,FOUR,CERO,DOS,TRES,QUATRO])
    intX += unit
    intY += unit

intX = 0+unit
intY = 0
intZ = 0
fltD = 0
wedge = 0.01
zee = wedge
while fltD < dblRmLngth :
    STRT = [intX,intY,intZ]
    TWO = [intX+unit,intY,intZ]
    THREE = [intX+unit,intY+unit,intZ]
    FOUR = [intX,intY+unit,intZ]
    #    rs.AddSrfPt([STRT,TWO,THREE,FOUR])
    fltD = rs.Distance([0+unit,0,0],THREE)
    if fltD < SMR :
        h = (fltD+overhang-diag)*diag/FCL
        CERO = [intX,intY,wedge]
        DOS = [intX+unit,intY,h*0.5+wedge]
        TRES = [intX+unit,intY+unit,h+wedge]
        QUATRO = [intX,intY+unit,h*0.5+wedge]
    else :
        h = (SMR+overhang-diag)*diag/FCL
        zee = zee + inc
        zed = min(h,zee)
        CERO = [intX,intY,zed+wedge]
        DOS = [intX+unit,intY,zed+(h-zed)/2+wedge]
        TRES = [intX+unit,intY+unit,h+wedge]
        QUATRO = [intX,intY+unit,zed+(h-zed)/2+wedge]
#    rs.AddSrfPt([STRT,DOS,TRES,QUATRO])
    rs.AddBox([STRT,TWO,THREE,FOUR,CERO,DOS,TRES,QUATRO])
    intX += unit
    intY += unit
