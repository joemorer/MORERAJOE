# 	AUTOMATIZACIÓN EN ARCMAP-PYTHON
#	EXTRACCIÓN DE MAPAS - CARACTERISTICAS ECO
#	NOMBRE			:	EXTRACCIONES_DE_POLIGONOS
#	Autor			:	Joel Fernando Morera Robles
#	Fecha Creado 	:	160823
#	Ultimo Cambio	:	
#		Por			:	

#################

""" 
	Descripcion:
		La automatización es un proceso cuyo objetivo es la optimización de tiempo en el procesamiento de información, 
  la automatización en programación Python se refiere al desarrollo de scripts o programas que ejecutan tareas 
  automáticamente sin intervención manual. Utilizando bibliotecas de Python, se accede a datos, se realizan cálculos 
  y se toman decisiones lógicas para automatizar tareas repetitivas. El proceso involucra identificar la tarea a automatizar, 
  escribir el código, probarlo y programar su ejecución periódica si es necesario. La automatización en Python ofrece ahorro 
  de tiempo y mejora la eficiencia al eliminar tareas manuales y evitar errores humanos.
  En particular, en este proyecto se busca diseñar un algoritmo en lenguaje Python con el objetivo de automatizar tareas 
  manuales inherentes al proceso de exportación de mapas con características particulares, tanto de formato como desde 
  los datos cruzados y geolocalizados, con el objetivo de optimización de recursos y tiempo, adicionalmente el algoritmo debe 
  contener protocolos de actualización del código para futuras tareas corporativas. Para el desarrollo de este diseño, 
  se cuenta con un tiempo límite de tres meses.

	Este archivo compila las versiones anteriores de Proyect_ArcMap.py
"""

# Import system modules  (Importa ArcGis)
import arcpy
from arcpy import env

# Folders de trabajo
FldOn = "C:/MyWork/Dropbox/MisionRural/"
# FldOn = "C:/Users/nury.bejarano/Dropbox/MisionRural/"
FldIn = FldOn + "Input/PREDIOS/"
FldWork = FldOn + "Working/"
FldOut = FldWork + "DistanciasLineal/"
FolderDest = FldOn + "Input/MapaDigitalIntegrado_MDI/proyectados/"
NearRange = "1000 Kilometers"
# Lista de layers destinos
ListaDest = ['cabecera', 'carretera_pavimentada', 'carretera_sinpavimentar']

# Lista de zonas (layers origen)
ListaPredios = ['CORDOBA', 'BUENAVISTA', 'EL_CERRITO', 'PALMIRA']
#'BUENAVISTA', 'EL_CERRITO', 'PALMIRA'

# Iterar sobre destinos
for dest in ListaDest :
	LayerDest = FolderDest + dest + ".shp"
	
	# Iterar sobre los predios
	for zona in ListaPredios :
		LayerOn = FldIn + zona + "/RURAL/TPR_" + zona + ".shp" 
		# Eliminar PointsShape.shp
		PointsShape = FldWork + "PointsShape.shp" # Este .shp es temporal 
		try:
			arcpy.Delete_management(PointsShape , "")
		except: 
			arcpy.AddMessage('Points no existe')

		# Transformar los predios en puntos - Nombre temporal PointsShape.shp
		arcpy.FeatureToPoint_management(LayerOn, PointsShape, "CENTROID")

		# Calcular la distancia a la cabecera más cercana
		arcpy.Near_analysis(PointsShape,LayerDest,NearRange,"NO_LOCATION","NO_ANGLE")
		
		# Exportar a dbf (Primero debo borrar el archivo.dbf si existe)
		FileOut =  FldOut + zona + "_DistTo_" + dest + "_Linear.dbf"
		try:
			arcpy.Delete_management(FileOut, "")
		except:
			arcpy.AddMessage('No existia')

		arcpy.TableToDBASE_conversion(PointsShape,FldOut)
		arcpy.Rename_management(FldOut + "PointsShape.dbf",FileOut)

# Finaliza
Fin = 'LISTO EL BURRO CABALLERO'
print Fin

########
