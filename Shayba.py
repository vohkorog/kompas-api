# -*- coding: utf-8 -*-
import pythoncom
from win32com.client import Dispatch, gencache


class Shayba:
    def __init__(self, innerD, outD, tolsh):
        self.__VnutrenniyDiametrShayb = innerD
        self.__VneshniyDiametrShayb = outD
        self.__TolshinaShayb = tolsh
        
        self.kompas_object = None
        self.kompas6_constants_3d = None
        self.iDocument3D = None
        self.iDocument2D = None
        self.iPart = None

        self.__conection_kompas()
        self.__setup_document()
        
    def __conection_kompas(self):

        #  Подключим константы API Компас
        self.kompas6_constants_3d = gencache.EnsureModule("{2CAF168C-7961-4B90-9DA2-701419BEEFE3}", 0, 1, 0).constants

        #  Подключим описание интерфейсов API5
        kompas6_api5_module = gencache.EnsureModule("{0422828C-F174-495E-AC5D-D31014DBBE87}", 0, 1, 0)
        self.kompas_object = kompas6_api5_module.KompasObject(Dispatch("Kompas.Application.5")._oleobj_.QueryInterface(kompas6_api5_module.KompasObject.CLSID, pythoncom.IID_IDispatch))
        

    def __setup_document(self):
        
#  Получим активный документ
        self.iDocument3D = self.kompas_object.ActiveDocument3D()
        self.iDocument2D = self.kompas_object.ActiveDocument2D()
        self.iPart = self.iDocument3D.GetPart(self.kompas6_constants_3d.pTop_Part)

    def createShayb(self):
        iSketch = self.iPart.NewEntity(self.kompas6_constants_3d.o3d_sketch)
        iDefinition = iSketch.GetDefinition()
        iPlane = self.iPart.GetDefaultEntity(self.kompas6_constants_3d.o3d_planeXOY)
        iDefinition.SetPlane(iPlane)
        iSketch.Create()

        self.iDocument2D = iDefinition.BeginEdit()

        obj = self.iDocument2D.ksCircle(0, 0, self.__VneshniyDiametrShayb, 1) # задание окружности x, y, радиус 
        iDefinition.EndEdit()
        iDefinition.angle = 180

        #Создание тела первого диска (выдавливание все дела)

        obj = self.iPart.NewEntity(self.kompas6_constants_3d.o3d_bossExtrusion)
        iDefinition = obj.GetDefinition()
        iCollection = self.iPart.EntityCollection(self.kompas6_constants_3d.o3d_edge)
        iDefinition.SetSketch(iSketch)
        iExtrusionParam = iDefinition.ExtrusionParam()
        iExtrusionParam.direction = self.kompas6_constants_3d.dtNormal
        iExtrusionParam.depthNormal = self.__TolshinaShayb
        iExtrusionParam.typeNormal = self.kompas6_constants_3d.etBlind

        obj.Create()

        #Создание второго эскиза


        iSketch = self.iPart.NewEntity(self.kompas6_constants_3d.o3d_sketch)
        iDefinition = iSketch.GetDefinition()
        iCollection = self.iPart.EntityCollection(self.kompas6_constants_3d.o3d_face)
        iPlane = iCollection.First()
        iDefinition.SetPlane(iPlane)
        iSketch.Create()

        self.iDocument2D = iDefinition.BeginEdit()
        obj = self.iDocument2D.ksCircle(0, 0, self.__VnutrenniyDiametrShayb, 1)
        iDefinition.EndEdit()

        iDefinition.angle = 180
        iSketch.Update()

        #Создание тела второго диска (выдавливание все дела)

        obj = self.iPart.NewEntity(self.kompas6_constants_3d.o3d_cutExtrusion)
        iDefinition = obj.GetDefinition()
        iCollection = self.iPart.EntityCollection(self.kompas6_constants_3d.o3d_edge)
        iDefinition.SetSketch(iSketch)
        iDefinition.cut = True
        iExtrusionParam = iDefinition.ExtrusionParam()
        iExtrusionParam.direction = self.kompas6_constants_3d.dtNormal
        iExtrusionParam.depthNormal = self.__TolshinaShayb
        iExtrusionParam.typeNormal = self.kompas6_constants_3d.etBlind

        obj.Create()
