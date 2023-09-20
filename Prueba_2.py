import arcpy

# Desactivar la actualización de pantalla
arcpy.env.addOutputsToMap = False

# Obtener el DataFrame activo
mxd = arcpy.mapping.MapDocument("CURRENT")
df = arcpy.mapping.ListDataFrames(mxd)[0]

# Ruta al archivo shapefile de entrada
input_shapefile = r"D:\Proyecto USTA-ECO\input\MGN2021_URB_MANZANA\MGN_URB_MANZANA.shp"

# Ruta al directorio donde se creará el nuevo layer
output_workspace = r"D:\Proyecto USTA-ECO\working"

# Nombre para el nuevo shapefile
output_shapefile_name = "Top10Selection.shp"

# Crear un nuevo shapefile con los primeros 10 registros
arcpy.MakeFeatureLayer_management(input_shapefile, "SelectionLayer")
arcpy.SelectLayerByAttribute_management("SelectionLayer", where_clause="FID <= 10")
output_shapefile_path = output_workspace + "\\" + output_shapefile_name
arcpy.CopyFeatures_management("SelectionLayer", output_shapefile_path)

print("Nuevo shapefile creado con la selección de los primeros 10 registros.")

# Deshabilitar la capa "SelectionLayer"
selection_layer = arcpy.mapping.Layer("SelectionLayer")
selection_layer.visible = False

# Agregar la capa "Top10Selection" al DataFrame
top10_layer = arcpy.mapping.Layer(output_shapefile_path)
arcpy.mapping.AddLayer(df, top10_layer)

# Hacer zoom a la extensión de la nueva capa
df.extent = top10_layer.getExtent()

# Refrescar la vista
arcpy.RefreshActiveView()

# Activar la actualización de pantalla nuevamente
arcpy.env.addOutputsToMap = True

# Guardar los cambios en el mapa
mxd.save()

print("Cambios guardados en el mapa.")
