#import gmsh
#import os
import Meshing.PointsToMesh as Mesh

if __name__ == "__main__":
        
    # p1 = gmsh.model.geo.add_point(0, 0, 0, lc)
    # p2 = gmsh.model.geo.add_point(0, 10, 0, lc)
    # p3 = gmsh.model.geo.add_point(10, 10, 0, lc)
    # p4 = gmsh.model.geo.add_point(10, 0, 0, lc)

    # PerimeterPoints = [p1, p2, p3, p4]
    

    # p5 = gmsh.model.geo.add_point(2, 5, 0, lc)
    # p6 = gmsh.model.geo.add_point(7, 4, 0, lc)
    # p7 = gmsh.model.geo.add_point(5, 8, 0, lc)
    
    # Points = [p5, p6, p7]


    p1 = (-5, -5, 0)
    #point = (x, y, z)
    p2 = (5, -5, 0)
    p3 = (5, 5, 0)
    p4 = (-5, 5, 0)

    p5 = (-2.5, -2.5, 0)
    p6 = (2.5, -2.5, 0)
    p7 = (2.5, 2.5, 0)
    p8 = (-2.5, 2.5, 0)

    WeldLine1 = [p5, p6, p7]
    WeldLine2 = [p7, p8, p1]

    WeldPointsList = [WeldLine1, WeldLine2]

    PerimeterPoints = [p1, p2, p3, p4]

    

    InflatableMesh = Mesh.CreateFlatMesh("test", WeldPointsList, True, PerimeterPoints, True, 0.5, 5)
    #CreateFlatMesh("FileName", WeldPointsList, WeldSpline, PerimeterPoints, PerimeterSpline, lc, TranslateDistance)
