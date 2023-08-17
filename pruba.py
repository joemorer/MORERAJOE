import arcpy

# Ruta al archivo shapefile de entrada
input_shapefile = r"RUTA\AL\ARCHIVO\input.shp"

# Ruta al directorio donde se creará el nuevo layer
output_workspace = r"RUTA\AL\DIRECTORIO\DE\SALIDA"

# Nombre para el nuevo layer
output_layer_name = "Top10Selection"

# Realizar la selección de las 10 primeras filas
arcpy.MakeFeatureLayer_management(input_shapefile, "SelectionLayer")
arcpy.SelectLayerByAttribute_management("SelectionLayer", "NEW_SELECTION", "", "", "OID ASC")
top_10_selection = arcpy.CopyFeatures_management("SelectionLayer", arcpy.Geometry())

# Crear un nuevo layer a partir de la selección
output_layer_path = arcpy.CreateFeatureclass_management(output_workspace, output_layer_name,
                                                        "POINT", spatial_reference=input_shapefile)

# Insertar las geometrías seleccionadas en el nuevo layer
with arcpy.da.InsertCursor(output_layer_path, ["SHAPE@"]) as cursor:
    for feature in top_10_selection:
        cursor.insertRow([feature])

print("Nuevo layer creado con las 10 primeras filas seleccionadas.")
