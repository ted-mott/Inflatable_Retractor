import gmsh
import os
import Meshing.PointsToMesh as Mesh


if __name__ == "__main__":
        
    gmsh.initialize()

    gmsh.clear()


    lc = 0.5

    p1 = gmsh.model.geo.add_point(0, 0, 0, lc)
    p2 = gmsh.model.geo.add_point(0, 10, 0, lc)
    p3 = gmsh.model.geo.add_point(10, 10, 0, lc)
    p4 = gmsh.model.geo.add_point(10, 0, 0, lc)

    PerimeterPoints = [p1, p2, p3, p4]
    

    p5 = gmsh.model.geo.add_point(2, 5, 0, lc)
    p6 = gmsh.model.geo.add_point(7, 4, 0, lc)
    p7 = gmsh.model.geo.add_point(5, 8, 0, lc)
    
    Points = [p5, p6, p7]

    WeldPoints = [Points]
    
    Mesh.CreateFlatMesh("test", WeldPoints, False, PerimeterPoints, False, False)
    #FileName, WeldPoints, WeldSpline, PerimeterPoints, PerimeterSpline, JoinPerimeterSurf

    