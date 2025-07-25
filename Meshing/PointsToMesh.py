"""
-------------------------------------------------------------------------------------------------------------------------------------------------
PointsToMesh.py
I/P: FileName, WeldPointsList, WeldSpline, PerimeterPoints, PerimeterSpline, lc
Method:
    (1). Convert points to GMSH points
    (2). Create curves through points
    (3). Copy and translate
    (4). Create surfaces
    (5). Create Physical Groups
    (6). Mesh geometry
    (7). Save GMSH mesh
O/P: FileName + ".geo_unrolled"
-------------------------------------------------------------------------------------------------------------------------------------------------
"""


"""
-------------------------------------------------------------------------------------------------------------------------------------------------
Modules to Import
-------------------------------------------------------------------------------------------------------------------------------------------------
"""
import gmsh
#import math
#import os


"""
-------------------------------------------------------------------------------------------------------------------------------------------------
Functions
-------------------------------------------------------------------------------------------------------------------------------------------------
"""
def PointsToGMSH(Points, lc):
    
    PointTagList = []
    for p in Points:
        PointTag = gmsh.model.geo.add_point(p[0], p[1], p[2], lc)
        #p(0, 1, 2) = Point(x, y, z)
        PointTagList.append(PointTag)
    return(PointTagList)
#convert point tuples to gmsh point - this structure was decided by me so that this gmsh module was reusable


def PointsToSplineGMSH(PointTagList, Close_Loop):
    
    SplineTagList = []

    if Close_Loop:
        PointTagList.append(PointTagList[0])
    # adds start point to list to ensure closed spline
    
    SplineTag = gmsh.model.geo.addSpline(PointTagList)
    SplineTagList.append(SplineTag)
    #this is using the GMSH solver spline not the opencascade(occ) spline so have to manually declare loop

    return(SplineTagList)   
#takes a list of gmsh point tags and returns the spline tag, if Close_Loop bool True then returns closed loop


def PointsToLineGMSH(PointTagList, Close_Loop):
    
    LineTagList= []

    for i in range(len(PointTagList)-1):
        LineTag = gmsh.model.geo.add_line(PointTagList[i], PointTagList[i+1])
        LineTagList.append(LineTag)

    if Close_Loop:
        LineTag = gmsh.model.geo.add_line(PointTagList[-1], PointTagList[0])
        LineTagList.append(LineTag)

    return(LineTagList)
#This creates a list of lines, if the close-loop bool is true, it creates a closed loop


def CopyAndTranslateGeometry(GMSHCurveList, ZTranslateDistance):
    GMSHCurveList_OffsetZ = []
    for GMSHCurve in GMSHCurveList:
        Curve_OffsetZ = gmsh.model.geo.copy([(1, GMSHCurve)])
        gmsh.model.geo.translate(Curve_OffsetZ, 0, 0, ZTranslateDistance)
        GMSHCurveList_OffsetZ.append(Curve_OffsetZ[0][1])
        # needs to be [0][1] as it is a little bit broken
    return(GMSHCurveList_OffsetZ)


def EmbedCurveInSurface(CurveTagList, SurfaceTag):

        for CurveTag in CurveTagList:
            gmsh.model.mesh.embed(1, CurveTag, 2, SurfaceTag)
    # runs embed curve command in gmsh


"""
-------------------------------------------------------------------------------------------------------------------------------------------------
Main
-------------------------------------------------------------------------------------------------------------------------------------------------
"""

def CreateFlatMesh(FileName, WeldPointsList, WeldSpline, PerimeterPoints, PerimeterSpline, lc, ZTranslateDistance):

    gmsh.initialize()
    #initialises GMSH environment
    
    gmsh.clear()
    #clear all previous GMSH geometry
    

    """
    (1) Convert points to GMSH points
    """
    WeldPointListGMSH = []

    for WeldPoints in WeldPointsList:
        WeldPointsGMSH = PointsToGMSH(WeldPoints, lc)
        WeldPointListGMSH.append(WeldPointsGMSH)
    #convert weld curve points to GMSH points


    PerimeterPointsGMSH = PointsToGMSH(PerimeterPoints, lc)
    #PerimeterPointsGMSH.append(PerimeterPointsGMSH)
    #convert perimeter points to GMSH points

        
    """
    (2) Create curves through points
    """
    WeldCurveListGMSH = []
    #software is assuming there will be one perimeter and multiple weld curves
    
    if WeldSpline:
        for CurvePts in WeldPointListGMSH:
            WeldCurveGMSH = PointsToSplineGMSH(CurvePts, False)
            WeldCurveListGMSH.append(WeldCurveGMSH)
    else:
        for CurvePts in WeldPointListGMSH:
            WeldCurveGMSH = PointsToLineGMSH(CurvePts, False)
            WeldCurveListGMSH.append(WeldCurveGMSH)
    #if WeldSpline true makes a spline, otherwise creates individual line segments, this just smooths basically

    if PerimeterSpline:
        PerimeterCurve = PointsToSplineGMSH(PerimeterPointsGMSH, True)
    else:
        PerimeterCurve = PointsToLineGMSH(PerimeterPointsGMSH, True)
    #Acts the same as WeldSpline but assumes single loop and it is assumed only perimeter loop is closed for now       
    
    PerimeterLoop = gmsh.model.geo.add_curve_loop(PerimeterCurve)
    Surface = gmsh.model.geo.addPlaneSurface([PerimeterLoop])


    """
    (3) Copy and translate to create the 2 sides of the mesh
    """
    WeldCurveListGMSH_OffsetZ =[]

    for WeldCurve in WeldCurveListGMSH:
        WeldCurve_OffsetZ = CopyAndTranslateGeometry(WeldCurve, ZTranslateDistance)
        WeldCurveListGMSH_OffsetZ.append(WeldCurve_OffsetZ)
    
    PerimeterCurve_OffsetZ = CopyAndTranslateGeometry(PerimeterCurve, ZTranslateDistance)
    

    Surface_OffsetZ = gmsh.model.geo.copy([(2, Surface)])
    gmsh.model.geo.translate(Surface_OffsetZ, 0, 0, ZTranslateDistance)


    """
    (4) Define surfaces
    """
    
    gmsh.model.geo.synchronize()


    """
    (5) Define Physical groups
    """


    
    """
    (6) Mesh geometry
    """
    EmbedCurveInSurface(WeldCurveListGMSH, Surface) #EmbedCurveInSurface(CurveTagList, SurfaceTag)
    print("curve list" , WeldCurveListGMSH, "surface", Surface)
    
    EmbedCurveInSurface(WeldCurveListGMSH_OffsetZ, Surface_OffsetZ[0][1])
    print("curve list" , WeldCurveListGMSH_OffsetZ, "surface", Surface_OffsetZ[0][1])
    #Embed curves in surfaces

    gmsh.model.geo.synchronize()
    

    try:
        #gmsh.model.mesh.setRecombine(2, SurfaceTag) #if only one surface 
        gmsh.option.setNumber("Mesh.RecombineAll", 2) #if multiple surfaces
        #(2) corresponds to dimension of mesh generated, 2 = surface, 1 = curve .etc.
        gmsh.model.mesh.generate(2)
    except:
        print("Angle in curve to sharp for quad mesh, meshing with triangles")
        gmsh.option.setNumber("Mesh.RecombineAll", 1) #if multiple surfaces
     
        gmsh.model.mesh.generate(2)
    #If quad mesh is not possible flags error and continues with triangle mesh, this may have to be remedied in future iterations, if optimisation is to be done
    
    
    """
    (7) Save GMSH mesh
    """
    #gmsh.write(FileName + ".geo_unrolled")

    gmsh.fltk.run()
    #opens up GMSH pop up window
    
    gmsh.finalize()
    #end gmsh process

    return(FileName + ".geo_unrolled")
    #output file name



"""
-------------------------------------------------------------------------------------------------------------------------------------------------
End
-------------------------------------------------------------------------------------------------------------------------------------------------
"""