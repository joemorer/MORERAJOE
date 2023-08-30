import arcpy

# Desactivar la actualización de pantalla
arcpy.env.addOutputsToMap = False

# Obtener el DataFrame activo
mxd = arcpy.mapping.MapDocument("CURRENT")
df = arcpy.mapping.ListDataFrames(mxd)[0]

# Nombre del layer "Top10Selection"
nombre_capa_top10 = "Top10Selection"

# Buscar el layer "Top10Selection"
capa_top10 = None
for capa in arcpy.mapping.ListLayers(mxd, "", df):
    if capa.name == nombre_capa_top10:
        capa_top10 = capa
        break

# Cambiar el símbolo de los polígonos a hueco (hollow)
if capa_top10:
    simbolo = capa_top10.symbology
    if isinstance(simbolo, arcpy.mapping.Layer):
        simbolo = simbolo.symbology

    if isinstance(simbolo, arcpy.mapping.PolygonSymbology):
        simbolo.renderer.symbol.applySymbolFromGallery("Layers\\Hollow Fill")
        arcpy.RefreshActiveView()

# Activar la actualización de pantalla nuevamente
arcpy.env.addOutputsToMap = True

# Guardar los cambios en el mapa
mxd.save()

print("Cambios guardados en el mapa.")
