"""
-------------------------------------------------------------------------------------------------------------------------------------------------
PointsToMesh
I/P: Filename, Perimeter points list (for closed loop), List of Weld points lists and spline bool for each and bool to join perimeter surfaces
Method:
    (1). Convert weld points to points, then join these into weld curves
    (2). Convert perimeter points to points and join these into perimeter curves
    (3). Copy and translate
    (4). Create surfaces
    (5). Create Physical Groups
    (6). Mesh
    (7). Save mesh
O/P: Save .msh file to file name specified on input, return filename (and location?) ready for next step
-------------------------------------------------------------------------------------------------------------------------------------------------
"""


"""
-------------------------------------------------------------------------------------------------------------------------------------------------
Modules to Import
-------------------------------------------------------------------------------------------------------------------------------------------------
"""
import gmsh
import math
import os



"""
def PtsToGMSH(Pts):
    PtTags = []
    for p in Pts:

#point structure needs to be decided, I am thinking for the time being it could be smart to put this in main
"""





def curveSplineLoop(PtTags, Close_Loop):

    if Close_Loop:
        PtTags.append(PtTags[0])
    
    SplineTag = gmsh.model.geo.addSpline(PtTags)

    if Close_Loop:
        SplineLoop = gmsh.model.geo.add_curve_loop([SplineTag])
        return (SplineLoop)
    else:
        return(SplineTag)
    
#takes a list of gmsh point tags and returns the spline tag (hopefully)


def curveLoop(PtTags, Close_Loop):
    LineTags= []

    for i in range(len(PtTags)-1):
        LineTag = gmsh.model.geo.add_line(PtTags[i], PtTags[i+1])
        LineTags.append(LineTag)

    if Close_Loop:
        LineTag = gmsh.model.geo.add_line(PtTags[-1], PtTags[0])
        LineTags.append(LineTag)

        LoopTag = gmsh.model.geo.add_curve_loop(LineTags)
        
        return(LoopTag)
    else:
        return(LineTags)

#I am really unsure that this will work, I am not very smart and such







def CreateFlatMesh(FileName, WeldPoints, WeldSpline, PerimeterPoints, PerimeterSpline, JoinPerimeterSurf):

    
    #gmsh.initialize()
    #initialises GMSH environment
    
    #gmsh.clear()
    #clear all previous GMSH geometry
    
    
    
    #(1) + (2) Define curves and loops
    

    WeldCurves = []
    
    if WeldSpline:
        for CurvePts in WeldPoints:
            WeldLoop = curveSplineLoop(CurvePts, False)
            #WeldCurves.append(WeldLoop)
    else:
        for CurvePts in WeldPoints:
            
            WeldLoop = curveLoop(CurvePts, False)
            WeldCurves.append(WeldLoop)
    #


    if PerimeterSpline:
        PerimeterLoop = curveSplineLoop(PerimeterPoints, True)

    else:
        PerimeterLoop = curveLoop(PerimeterPoints, True)
    
    #(3) Copy and translate to create the 2 sides of the mesh
    
    s2 = gmsh.model.geo.addPlaneSurface([PerimeterLoop])
    c2 = WeldCurves[int(0)]
    
      
    print(c2)

    gmsh.model.geo.synchronize()

    gmsh.model.mesh.embed(1, [c2[0]], 2, s2)
    gmsh.model.mesh.embed(1, [c2[1]], 2, s2)
    #..embed(dimension to be embedded, tag, dimension embedded into, tag)
    
    #(4) Define surfaces

    


    
    #(5) Define Physical groups
    



    gmsh.model.geo.synchronize()
    #updates all the geometry in file

    
    #(6) Generate Mesh
    

    gmsh.model.mesh.generate(2)
    # 2 corresponds to dimension of mesh generated, 2 = surface mesh


    
    #(7) Write file
    

    gmsh.write(FileName + ".geo_unrolled")

    gmsh.fltk.run()
    #opens up GMSH pop up window
    
    gmsh.finalize()
    #end gmsh process

    return(FileName + ".geo_unrolled")
    #output file name


