import arcpy

# Ruta al archivo shapefile de entrada
input_shapefile = r"D:\Proyecto USTA-ECO\input\MGN2021_URB_MANZANA\MGN_URB_MANZANA.shp"

# Ruta al directorio donde se creará el nuevo shapefile
output_workspace = r"D:\Proyecto USTA-ECO\working"

# Nombre para el nuevo shapefile
output_shapefile_name = "Top10Selection.shp"

# Crear un nuevo shapefile con los primeros 10 registros
arcpy.MakeFeatureLayer_management(input_shapefile, "SelectionLayer")
arcpy.SelectLayerByAttribute_management("SelectionLayer", where_clause="FID <= 10")
output_shapefile_path = output_workspace + "\\" + output_shapefile_name
arcpy.CopyFeatures_management("SelectionLayer", output_shapefile_path)

print("Nuevo shapefile creado con la selección de los primeros 10 registros.")

# Obtener el mapa activo
mxd = arcpy.mapping.MapDocument("CURRENT")

# Obtener el DataFrame activo
df = arcpy.mapping.ListDataFrames(mxd)[0]

# Nombre de la capa que deseas ocultar
layer_to_hide_name = "SelectionLayer"

# Buscar la capa por su nombre en el DataFrame
for lyr in arcpy.mapping.ListLayers(mxd, "*", df):
    if lyr.name == layer_to_hide_name:
        lyr.visible = False  # Establecer la propiedad 'visible' en False para ocultar la capa

print("Se ha ocultado el Layer: SelectionLayer")

# Refrescar la vista
arcpy.RefreshActiveView()

# Hacer zoom a la capa "Top10Selection"
for lyr in arcpy.mapping.ListLayers(mxd, "*", df):
    if lyr.name == "Top10Selection":
        arcpy.SelectLayerByAttribute_management(lyr, "CLEAR_SELECTION")  # Despejar cualquier selección
        arcpy.SelectLayerByAttribute_management(lyr, "NEW_SELECTION", "FID <= 10")  # Seleccionar las primeras 10 filas
        df.zoomToSelectedFeatures()  # Hacer zoom a las características seleccionadas

# Refrescar la vista nuevamente
arcpy.RefreshActiveView()

# Activar la actualización de pantalla nuevamente
arcpy.env.addOutputsToMap = True

print("Cambios guardados en el mapa.")

