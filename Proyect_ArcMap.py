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
# Crear archivo en blanco de trabajo

# Ruta y nombre del nuevo archivo MXD
nuevo_mxd_path = r"D:\Proyecto USTA-ECO\mxd\Proyecto_USTA-ECO.mxd"

# Crear un objeto MapDocument en blanco
mxd = arcpy.mapping.MapDocument("CURRENT")  # Crea un nuevo MXD en blanco

# Guardar el nuevo archivo MXD en la ubicación especificada
mxd.saveACopy(nuevo_mxd_path)

# Ruta al archivo shapefile y al archivo MXD (Map Document)
shapefile_path = r"D:\Proyecto USTA-ECO\base\MGN2021_URB_MANZANA\MGN_URB_MANZANA.shp"
mxd_path = r"D:\Proyecto USTA-ECO\mxd\Proyecto_USTA-ECO.mxd"

# Conexión al documento MXD
mxd = arcpy.mapping.MapDocument(mxd_path)



# Finaliza
Fin = 'LISTO EL BURRO CABALLERO'
print Fin

########

