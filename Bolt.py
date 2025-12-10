# -*- coding: utf-8 -*-
import pythoncom
from win32com.client import Dispatch, gencache
import math
import numpy as np


class Bolt:
    def __init__(self, edge_length, head_height, kernel_dia, kernel_height):
        
        self.edge_length = edge_length
        self.head_height = head_height 
        self.kernel_dia = kernel_dia/2
        self.kernel_height = kernel_height
        
        self.kompas_object = None
        self.kompas6_constants_3d = None
        self.kompas_document = None
        self.kompas_document_2d = None
        self.kompas_document_3d = None
        self.application = None
        self.iPart = None
        self.kompas6_api5_module = None
        self.kompas_api7_module = None

        self.__conection_kompas()
        self.__setup_document()

        
    def __conection_kompas(self):

        #  Подключим константы API Компас
        self.kompas6_constants_3d = gencache.EnsureModule("{2CAF168C-7961-4B90-9DA2-701419BEEFE3}", 0, 1, 0).constants

        #  Подключим описание интерфейсов API5
        self.kompas6_api5_module = gencache.EnsureModule("{0422828C-F174-495E-AC5D-D31014DBBE87}", 0, 1, 0)
        self.kompas_object = self.kompas6_api5_module.KompasObject(Dispatch("Kompas.Application.5")._oleobj_.QueryInterface(self.kompas6_api5_module.KompasObject.CLSID, pythoncom.IID_IDispatch))
        
        #  Подключим описание интерфейсов API7
        self.kompas_api7_module = gencache.EnsureModule("{69AC2981-37C0-4379-84FD-5DD2F3C0A520}", 0, 1, 0)
        self.application = self.kompas_api7_module.IApplication(Dispatch("Kompas.Application.7")._oleobj_.QueryInterface(self.kompas_api7_module.IApplication.CLSID, pythoncom.IID_IDispatch))

    def __setup_document(self):
        iDocument3D = self.kompas_object.ActiveDocument3D()
        
        #  Получим активный документ
        self.kompas_document = self.application.ActiveDocument
        self.kompas_document_2d = self.kompas_api7_module.IKompasDocument2D(self.kompas_document)
        self.iPart = iDocument3D.GetPart(self.kompas6_constants_3d.pTop_Part)

    def __get_hexagon_coordinates(self):
        # коородинаты вершин
        
        angles = np.linspace(0, 2 * np.pi, 7)
        
        x_coords = self.edge_length * np.cos(angles)
        y_coords = self.edge_length * np.sin(angles)
        
        return x_coords, y_coords 
    
    
    def createBolt(self):
        
        # Отрисовка эскиза шестигранника и внутренней окружности
        iSketch = self.iPart.NewEntity(self.kompas6_constants_3d.o3d_sketch)
        iDefinition = iSketch.GetDefinition()
        iPlane = self.iPart.GetDefaultEntity(self.kompas6_constants_3d.o3d_planeXOY)
        iDefinition.SetPlane(iPlane)
        iSketch.Create()
        iDocument2D = iDefinition.BeginEdit()
        self.kompas_document_2d = self.kompas_api7_module.IKompasDocument2D(self.kompas_document)
        iDocument2D = self.kompas_object.ActiveDocument2D()
        x, y = self.__get_hexagon_coordinates()
        
        obj = iDocument2D.ksLineSeg(x[0], y[0], x[1], y[1], 1)
        obj = iDocument2D.ksLineSeg(x[1], y[1], x[2], y[2], 1)
        obj = iDocument2D.ksLineSeg(x[2], y[2], x[3], y[3], 1)
        obj = iDocument2D.ksLineSeg(x[3], y[3], x[4], y[4], 1)
        obj = iDocument2D.ksLineSeg(x[4], y[4], x[5], y[5], 1)
        obj = iDocument2D.ksLineSeg(x[5], y[5], x[6], y[6], 1)
        iDefinition.EndEdit()
        iDefinition.angle = 180
        iSketch.Update()
    
        # выдавливание эскиза шестиугольника
        obj = self.iPart.NewEntity(self.kompas6_constants_3d.o3d_bossExtrusion)
        iDefinition = obj.GetDefinition()
        iDefinition.SetSketch(iSketch)
        iExtrusionParam = iDefinition.ExtrusionParam()
        iExtrusionParam.direction = self.kompas6_constants_3d.dtNormal
        iExtrusionParam.depthNormal = self.head_height
        obj.Create()
        
        # Создание эскиза для внешней фаски 
        iSketch = self.iPart.NewEntity(self.kompas6_constants_3d.o3d_sketch)
        iDefinition = iSketch.GetDefinition()
        iPlane = self.iPart.GetDefaultEntity(self.kompas6_constants_3d.o3d_planeYOZ)
        iDefinition.SetPlane(iPlane)
        iSketch.Create()
        
        # Отрисовка треугольников для выреза
        iDocument2D = iDefinition.BeginEdit()
        iDocument2D = self.kompas_object.ActiveDocument2D()
        
        angle_30 = math.radians(30)
        base_length = 5                                                 # Длина основания
        height_triangle = (base_length / 2) * math.tan(angle_30)        # Высота треугольника рассчитывается через тангенс
        
        obj1 = iDocument2D.ksLineSeg(-y[1], 0, -y[1] - base_length, 0, 1)
        obj2 = iDocument2D.ksLineSeg(-y[1] - base_length, 0, -y[1] - base_length/2, height_triangle, 1)
        obj3 = iDocument2D.ksLineSeg(-y[1] - base_length/2, height_triangle, -y[1], 0, 1)      
        
        iDefinition.EndEdit()
        iDefinition.angle = 90
        iSketch.Update()
        
        # вырез вращением
        
        obj = self.iPart.NewEntity(self.kompas6_constants_3d.o3d_cutRotated)
        iDefinition = obj.GetDefinition()
        iDefinition.cut = True
        
        iCollection = self.iPart.EntityCollection(self.kompas6_constants_3d.o3d_edge)       
        iDefinition.SetSketch(iSketch)
        iRotatedParam = iDefinition.RotatedParam()
        iRotatedParam.direction = self.kompas6_constants_3d.dtNormal
        obj.Create()
        
        # создание эскиза с окружностью для ножки болта 
        iSketch = self.iPart.NewEntity(self.kompas6_constants_3d.o3d_sketch)
        iDefinition = iSketch.GetDefinition()
        iCollection = self.iPart.EntityCollection(self.kompas6_constants_3d.o3d_face)
        iCollection.SelectByPoint(0, 0, self.head_height)
        iPlane = iCollection.First()
        iDefinition.SetPlane(iPlane)
        iSketch.Create()
        iDocument2D = iDefinition.BeginEdit()
        iDocument2D = self.kompas_object.ActiveDocument2D()
        obj = iDocument2D.ksCircle(0, 0, self.kernel_dia, 1)
        iDefinition.EndEdit()
        iDefinition.angle = 180
        iSketch.Update()
        
        # выдавливание ножки болта 
        obj = self.iPart.NewEntity(self.kompas6_constants_3d.o3d_bossExtrusion)
        iDefinition = obj.GetDefinition()
        iDefinition.SetSketch(iSketch)
        iExtrusionParam = iDefinition.ExtrusionParam()
        iExtrusionParam.direction = self.kompas6_constants_3d.dtNormal
        iExtrusionParam.depthNormal = self.kernel_height
        obj.Create()
        
              
    