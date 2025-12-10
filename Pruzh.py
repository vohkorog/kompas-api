# -*- coding: utf-8 -*-
import pythoncom
from win32com.client import Dispatch, gencache


class Pruzh:
    def __init__(self, diam, step, turn, dia_sterj):
        self.diam = diam
        self.step = step
        self.turn = turn
        self.rad_sterj = dia_sterj/2
        
        self.radius = self.diam/2
        self.dist_z = self.turn/2 * self.step
        
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

    def createPruzh(self):
        
        # Создание спирали 
        obj = self.iPart.NewEntity(self.kompas6_constants_3d.o3d_cylindricSpiral)
        iDefinition = obj.GetDefinition()
        iDefinition.diam = self.diam
        iDefinition.step = self.step
        iDefinition.turn = self.turn
        iPlane = self.iPart.GetDefaultEntity(self.kompas6_constants_3d.o3d_planeXOY)
        iDefinition.SetPlane(iPlane)
        iDefinition.SetLocation(0,0)
        obj.Create()
        
        # Создание перпендикулярной плоскости
        obj = self.iPart.NewEntity(self.kompas6_constants_3d.o3d_planePerpendicular)
        iDefinition = obj.GetDefinition()
        iCollection = self.iPart.EntityCollection(self.kompas6_constants_3d.o3d_edge)
        iCollection.SelectByPoint(-self.radius, 0, self.dist_z)
        iEdge = iCollection.Last()
        iDefinition.SetEdge(iEdge)
        iCollection = self.iPart.EntityCollection(self.kompas6_constants_3d.o3d_vertex)
        iCollection.SelectByPoint(self.radius, 0, 0)
        iPoint = iCollection.First()
        iDefinition.SetPoint(iPoint)
        obj.Create()
        
        # Создание эскиза с окружностью 
        iSketch = self.iPart.NewEntity(self.kompas6_constants_3d.o3d_sketch)
        iDefinition = iSketch.GetDefinition()
        iCollection = self.iPart.EntityCollection(self.kompas6_constants_3d.o3d_planePerpendicular)
        iCollection.SelectByPoint(0, 0, 0)
        iPlane = iCollection.First()
        iDefinition.SetPlane(iPlane)
        iSketch.Create()
        iDocument2D = iDefinition.BeginEdit()
        iDocument2D = self.kompas_object.ActiveDocument2D()
        obj = iDocument2D.ksCircle(-self.radius, 0, self.rad_sterj, 1)
        iDefinition.EndEdit()
        iDefinition.angle = 180
        iSketch.Update()
        
        # Вытягивание по траектории
        
        obj = self.iPart.NewEntity(self.kompas6_constants_3d.o3d_bossEvolution)
        iDefinition = obj.GetDefinition()
        iDefinition.sketchShiftType = 1
        iCollection = self.iPart.EntityCollection(self.kompas6_constants_3d.o3d_edge)
        iCollection.SelectByPoint(self.radius + self.rad_sterj, 0, 0)
        iEdge = iCollection.Last()
        iEdgeDefinition = iEdge.GetDefinition()
        iSketch = iEdgeDefinition.GetOwnerEntity()
        iDefinition.SetSketch(iSketch)
        iArray = iDefinition.PathPartArray()
        iCollection = self.iPart.EntityCollection(self.kompas6_constants_3d.o3d_edge)
        iCollection.SelectByPoint(-self.radius, 0, self.turn / 2 * self.step)
        iCurve = iCollection.Last()
        iArray.Add(iCurve)
        obj.Create()
    
