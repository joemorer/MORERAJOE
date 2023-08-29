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

# Definir el nombre de la capa a ocultar
nombre_capa_a_ocultar = "SelectionLayer"

# Crear un nuevo shapefile con los primeros 10 registros
arcpy.MakeFeatureLayer_management(input_shapefile, "SelectionLayer")
arcpy.SelectLayerByAttribute_management("SelectionLayer", where_clause="FID <= 10")
output_shapefile_path = output_workspace + "\\" + output_shapefile_name
arcpy.CopyFeatures_management("SelectionLayer", output_shapefile_path)

print("Nuevo shapefile creado con la selección de los primeros 10 registros.")

# Ocultar la capa "SelectionLayer"
for capa in arcpy.mapping.ListLayers(mxd, "", df):
    if capa.name == nombre_capa_a_ocultar:
        capa.visible = False

print("Capa '" + nombre_capa_a_ocultar + "' ocultada en ArcMap.")

# Refrescar la vista
arcpy.RefreshActiveView()

# Activar la actualización de pantalla nuevamente
arcpy.env.addOutputsToMap = True

# Crear un objeto Layer con el shapefile "Top10Selection"
output_shapefile_full_path = output_workspace + "\\" + output_shapefile_name
capa_top_10 = arcpy.mapping.Layer(output_shapefile_full_path)

# Agregar la capa "Top10Selection" al DataFrame
arcpy.mapping.AddLayer(df, capa_top_10, "TOP")
print("Capa '" + nombre_capa_a_ocultar + "' ocultada en ArcMap.")

# Guardar los cambios en el mapa
# mxd.save()

print("Cambios guardados en el mapa.")
