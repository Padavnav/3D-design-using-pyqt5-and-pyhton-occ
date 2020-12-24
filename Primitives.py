import math
import sys

from OCC.Core.gp import (gp_Pnt, gp_Ax3, gp_Dir, gp_Circ, gp_Ax2)
from OCC.Core.BRepBuilderAPI import (BRepBuilderAPI_MakeEdge,
                                     BRepBuilderAPI_MakeFace,
                                     BRepBuilderAPI_MakeWire,
                                     BRepBuilderAPI_MakeVertex)
from OCC.Core.BRepPrimAPI import BRepPrimAPI_MakeBox
from OCC.Core.TColgp import TColgp_Array1OfPnt
from OCC.Core.Geom import Geom_BezierCurve
from OCC.Core.Geom2d import Geom2d_Line
from OCC.Core.AIS import AIS_Shaded, AIS_Shape, AIS_WireFrame
from OCC.Core.Quantity import Quantity_Color, Quantity_NOC_BLACK

#from OCC.Display.SimpleGui import init_display
#display, start_display, add_menu, add_function_to_menu = init_display()
    
def display1(shape, display, color = [0, 0, 0], transparency = 0):
    color = Quantity_Color(color[0], color[1], color[2], 0)
    ais_shape = AIS_Shape(shape)
    context = display.GetContext()
    #context.SetColor(ais_shape, color, False)
    ais_shape.SetColor(color)
    ais_shape.SetTransparency(transparency)
    # pass False if viewer should not be updated
    context.Display(ais_shape, True)
    display.FitAll()
    return ais_shape

class Primitives():
    def Cube(display):
        transparency = 0.67
        color = [0.9, 0.9, 0.9]
        cube = BRepPrimAPI_MakeBox(1, 1, 1)
        display1(cube.Shape(), display, color, transparency)
    
    def Line(display):
        p1 = gp_Pnt()
        p2 = gp_Pnt()

        p1.SetCoord(-5,-5,-5)
        p2.SetCoord(5,5,5)

        p1_vertex = BRepBuilderAPI_MakeVertex(p1)
        p2_vertex = BRepBuilderAPI_MakeVertex(p2)
        p1_vertex.Vertex()
        line = BRepBuilderAPI_MakeEdge(p1_vertex.Vertex(), p2_vertex.Vertex())
        #display.DisplayColoredShape(line.Edge(), 'CYAN')
        #display.DisplayColoredShape(p1_vertex.Vertex(),'WHITE')
        #display.DisplayColoredShape(p2_vertex.Vertex(),'WHITE')
        #display.FitAll()
        return display1(line.Edge(), display)

    def Disk(display, parent):
        color=[1, 0, 0]
        x = parent.input.getDouble("Center", "Disk", "x coordinate")
        y = parent.input.getDouble("Center", "Disk", "y coordinate")
        z = parent.input.getDouble("Center", "Disk", "z coordinate")
        center = gp_Pnt(x,y,z)
        normal = gp_Dir(0,0,1)
        radius = parent.input.getDouble("Disk", "Disk", "Radius")
        circle = gp_Circ( gp_Ax2(center,normal) , radius)
        circle_edge = BRepBuilderAPI_MakeEdge(circle)
        circle_wire = BRepBuilderAPI_MakeWire(circle_edge.Edge())
        circle_face = BRepBuilderAPI_MakeFace(circle_wire.Wire())
        #display.DisplayColoredShape(circle_face.Face(),'RED')
        #canva._display.FitAll()
        return display1(circle_face.Face(), display, color)

    def Rectangle(display, parent):
        color=[0, 1, 0]
        x = parent.input.getDouble("Starting Point", "Rectangle", "x coordinate")
        y = parent.input.getDouble("Starting Point", "Rectangle", "y coordinate")
        z = parent.input.getDouble("Starting Point", "Rectangle", "z coordinate")
        
        x_length = parent.input.getDouble("Rectangle", "Rectangle", "Length in x direction")
        y_length = parent.input.getDouble("Rectangle", "Rectangle", "Length in y direction")
        
        p1 = gp_Pnt()
        p2 = gp_Pnt()
        p3 = gp_Pnt()
        p4 = gp_Pnt()

        p1.SetCoord(x, y, z)
        p2.SetCoord(x, y+y_length, z)
        p3.SetCoord(x+x_length, y+y_length, z)
        p4.SetCoord(x+x_length, y, z)

        Edge1 = BRepBuilderAPI_MakeEdge(p1, p2)
        Edge2 = BRepBuilderAPI_MakeEdge(p2, p3)
        Edge3 = BRepBuilderAPI_MakeEdge(p3, p4)
        Edge4 = BRepBuilderAPI_MakeEdge(p4, p1)

        rect_wire = BRepBuilderAPI_MakeWire(Edge1.Edge(), Edge2.Edge(), Edge3.Edge(), Edge4.Edge())
        if not rect_wire.IsDone():
            raise AssertionError("rect_wire is not done.")
        rect_face = BRepBuilderAPI_MakeFace(rect_wire.Wire())
        #display.DisplayColoredShape(rect_face.Face(),'BLUE')
        #display.FitAll()
        return display1(rect_face.Face(), display, color)

    def Triangle(display, parent):
        color=[0, 0, 1]
        
        z = parent.input.getDouble("Triangle", "Triangle", "z coordinate")
        
        x1 = parent.input.getDouble("First Point", "Triangle", "x coordinate")
        y1 = parent.input.getDouble("First Point", "Triangle", "y coordinate")
        
        x2 = parent.input.getDouble("Second Point", "Triangle", "x coordinate")
        y2 = parent.input.getDouble("Second Point", "Triangle", "y coordinate")
        
        x3 = parent.input.getDouble("Third Point", "Triangle", "x coordinate")
        y3 = parent.input.getDouble("Third Point", "Triangle", "y coordinate")
        
        p1 = gp_Pnt()
        p2 = gp_Pnt()
        p3 = gp_Pnt()

        p1.SetCoord(x1,y1,z)
        p2.SetCoord(x2,y2,z)
        p3.SetCoord(x3,y3,z)

        Edge1 = BRepBuilderAPI_MakeEdge(p1, p2)
        Edge2 = BRepBuilderAPI_MakeEdge(p2, p3)
        Edge3 = BRepBuilderAPI_MakeEdge(p1, p3)

        tri_wire = BRepBuilderAPI_MakeWire(Edge1.Edge(), Edge2.Edge(), Edge3.Edge())
        if not tri_wire.IsDone():
            raise AssertionError("rect_wire is not done.")
        tri_face = BRepBuilderAPI_MakeFace(tri_wire.Wire())
        #display.DisplayColoredShape(tri_face.Face(),'YELLOW')
        #display.FitAll()
        return display1(tri_face.Face(), display, color)

    def Curve(display):
        P1 = gp_Pnt(-15, 20, 10)
        P2 = gp_Pnt(5, 20, 0)
        P3 = gp_Pnt(15, 20, 0)
        P4 = gp_Pnt(-15, 20, 15)
        P5 = gp_Pnt(-5, 20, 0)
        P6 = gp_Pnt(15, 20, 0)
        P7 = gp_Pnt(24, 12, 0)
        P8 = gp_Pnt(-24, 12, 12.5)
        array = TColgp_Array1OfPnt(1, 8)
        array.SetValue(1, P1)
        array.SetValue(2, P2)
        array.SetValue(3, P3)
        array.SetValue(4, P4)
        array.SetValue(5, P5)
        array.SetValue(6, P6)
        array.SetValue(7, P7)
        array.SetValue(8, P8)
        curve = Geom_BezierCurve(array)
        curve_edge = BRepBuilderAPI_MakeEdge(curve)
        #display.DisplayColoredShape(curve_edge.Edge(), 'CYAN')
        #display.DisplayColoredShape(curve_edge.Vertex1(),'WHITE')
        #display.DisplayColoredShape(curve_edge.Vertex2(),'WHITE')
        #display.FitAll()
        return display1(curve.Edge(), display)

    def Polygon(display, parent):
        
        n = parent.input.getInteger("Polygon", "Polygon", "No of sides", 3)
        z = parent.input.getDouble("Polygon", "Polygon", "z coordinate")
        
        #for i in n:
        #    x = parent.input.getDouble(i + " Point", "Polygon", "x coordinate")
        #    y = parent.input.getDouble(i + " Point", "Polygon", "y coordinate")
        #    P = gp_Pnt(x, y, z)
            
        P1 = gp_Pnt(-15, 20, 10)
        P2 = gp_Pnt(5, 20, 0)
        P3 = gp_Pnt(15, 20, 0)
        P4 = gp_Pnt(-15, 20, 15)
        P5 = gp_Pnt(-5, 20, 0)
        P6 = gp_Pnt(15, 20, 0)
        P7 = gp_Pnt(24, 12, 0)
        P8 = gp_Pnt(-24, 12, 12.5)
        array = TColgp_Array1OfPnt(1, 8)
        array.SetValue(1, P1)
        array.SetValue(2, P2)
        array.SetValue(3, P3)
        array.SetValue(4, P4)
        array.SetValue(5, P5)
        array.SetValue(6, P6)
        array.SetValue(7, P7)
        array.SetValue(8, P8)
        curve = Geom_BezierCurve(array)
        curve_edge = BRepBuilderAPI_MakeEdge(curve)
        #display.DisplayColoredShape(curve_edge.Edge(), 'CYAN')
        #display.DisplayColoredShape(curve_edge.Vertex1(),'WHITE')
        #display.DisplayColoredShape(curve_edge.Vertex2(),'WHITE')
        #display.FitAll()
        return display1(curve_edge.Edge(), display)

    def Erase_all(event=None): 
        #display.EraseAll()
        print("Aditya")