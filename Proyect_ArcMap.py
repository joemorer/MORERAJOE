# 	AUTOMATIZACIÓN EN ARCMAP-PYTHON
#	EXTRACCIÓN DE MAPAS - CARACTERISTICAS ECO
#	NOMBRE			:	EXTRACCIONES_DE_POLIGONOS
#	Autor			:	Joel Fernando Morera Robles
#	Fecha Creado 	:	160823
#	Ultimo Cambio	:	231023
#		Por	:	Joel Fernando Morera Robles

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
  
  Este archivo compila la versión final de Proyect_ArcMap.py

  Exe_CODE: El código proporciona una herramienta eficaz para la generación de archivos PDF personalizados a partir de datos 
  geoespaciales almacenados en un archivo Shapefile. Utilizando una variedad de bibliotecas de Python, el código destaca polígonos 
  específicos en mapas geográficos al tiempo que permite un alto grado de personalización en términos de colores, 
  tamaños y estilos de los polígonos. Además, se integra una funcionalidad que verifica si los mapas generados caben en las páginas PDF, 
  proporcionando advertencias en caso de problemas de ajuste. Este código simplifica el proceso de exportar mapas geoespaciales 
  resaltados en un formato PDF, brindando a los usuarios la capacidad de comunicar y compartir visualmente información geográfica 
  de manera efectiva. El PDF generado por el código contiene una serie de páginas, una por cada polígono resaltado en 
  el archivo Shapefile de entrada. Cada página del PDF incluye: 
  	1. Un mapa geoespacial: El polígono de interés se resalta en un mapa geográfico, permitiendo la visualización precisa 
   	de su ubicación en contexto.
    	2. Números de identificación: Cada polígono se etiqueta con un número de identificación que facilita su seguimiento y referencia.
     	3. Título: El título del PDF se muestra en la parte superior de cada página, proporcionando un contexto general para 
      	los mapas generados.

"""

from fpdf import FPDF
from fpdf.enums import XPos
from fpdf.enums import YPos
import matplotlib.pyplot as plt
import geopandas as gpd
import contextily as ctx
from tqdm import tqdm
from PIL import Image
from PIL import ImageOps

# Define las rutas de los archivos
shapefile_path = "/Users/joelmorera/Documents/Proyecto USTA-ECONO/etapa1/input/MGN_2021_COLOMBIA/URBANO/MGN_URB_MANZANA.shp"
output_pdf_path = "/Users/joelmorera/Documents/PDFs_poligonos/poligonos_destacados.pdf"

def cargar_shapefile(shapefile_path):
    """
    Carga un shapefile y lo proyecta en el sistema de coordenadas adecuado.

    Args:
        shapefile_path (str): Ruta del archivo shapefile.

    Returns:
        gpd.GeoDataFrame: GeoDataFrame cargado desde el shapefile.
        str: Sistema de coordenadas proyectadas.
    """
    print("Iniciando la carga del shapefile...")

    try:
        shapefile = gpd.read_file(shapefile_path)
        proyecto_crs = 'EPSG:21897'

        # Cambiar el CRS del GeoDataFrame al sistema de coordenadas proyectadas adecuado
        shapefile = shapefile.to_crs(proyecto_crs)

        print("Carga del shapefile completada.")

    except Exception as e:
        print(f"Error al cargar el shapefile: {e}")
        shapefile = None
        proyecto_crs = None

    return shapefile, proyecto_crs


def generar_poligonos_en_pdf(shapefile, output_pdf_path, proyecto_crs):
    """
    Genera un PDF con mapas de polígonos resaltados.

    Args:
        shapefile (gpd.GeoDataFrame): GeoDataFrame con los datos de polígonos.
        output_pdf_path (str): Ruta de salida para el archivo PDF.
        proyecto_crs (str): Sistema de coordenadas proyectadas.

    Returns:
        None
    """
    if shapefile is None:
        print("No se pudo cargar el shapefile. No se generará el PDF.")
        return

    # Obtén el número total de polígonos
    total_poligonos = len(shapefile)

    # Crear un objeto PDF
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)

    # Crear una barra de progreso para la generación del PDF
    pdf_bar = tqdm(total=total_poligonos, desc="Generando PDF", unit=" página(s)")

    # Título
    titulo = "Automatización de procesos de extracción en Python"
    pdf.set_font("Helvetica", size=16)

    for i, polygon in enumerate(shapefile.geometry):
        if polygon.area > 0:
            pdf.add_page()

            # Crear una figura de Matplotlib con un tamaño personalizado
            fig, ax = plt.subplots(figsize=(8, 8))

            # Configurar los límites del mapa
            bounds = shapefile.total_bounds
            ax.set_xlim(bounds[0], bounds[2])  # Límites x (longitud)
            ax.set_ylim(bounds[1], bounds[3])  # Límites y (latitud)

            # Dibujar los polígonos
            for j, poly in enumerate(shapefile.geometry):
                color = 'red' if j == i else 'black'
                linewidth = 1.0 if j == i else 0.5
                gpd.GeoSeries(poly).plot(ax=ax, color='none', edgecolor=color, linewidth=linewidth, label="")

                # Obtener el centro del polígono y agregar el número
                centro = poly.centroid
                label = str(j + 1)
                if j == i:
                    ax.text(centro.x, centro.y, label, ha='left', va='center', fontsize=12, color='red', weight='bold')
                else:
                    ax.text(centro.x, centro.y, label, ha='left', va='center', fontsize=12, color='black')

            # Agregar OpenStreetMap como fondo utilizando contextily
            ctx.add_basemap(ax, crs=proyecto_crs, source=ctx.providers.OpenStreetMap.Mapnik)

            # Eliminar ejes y etiquetas
            ax.set_axis_off()

            # Guardar la figura como una imagen temporal
            temp_image_filename = f"temp_image_{i}.png"
            fig.savefig(temp_image_filename, format='png', bbox_inches='tight', pad_inches=0, dpi=500)
            plt.close(fig)

            # Obtén el ancho y alto de la página
            pdf_w = pdf.w
            pdf_h = pdf.h

            # Título de la página en mayúsculas
            titulo = "Automatización de procesos de extracción en Python"
            pdf.set_font("Helvetica", size=16)
            pdf.cell(200, 10, text=titulo, align="C")
            pdf.ln()

            numero_poligono = f"NÚMERO DE POLÍGONO: {str(i + 1).zfill(4)}".upper()
            pdf.set_font("Helvetica", size=14, style="B")
            pdf.set_xy(10, pdf.get_y())  # Alinea a la izquierda
            pdf.cell(200, 10, text=numero_poligono, align="L")
            pdf.ln()

            # Calcular la posición x para centrar horizontalmente la imagen
            img_w = pdf_w * 0.65
            x = (pdf_w - img_w) / 2

            # Calcular la posición y para centrar verticalmente en la línea del medio
            img_h = img_w  # Suponiendo que la imagen tenga las mismas dimensiones de ancho y alto
            y = 30

            # Verificar si el mapa se sale de la página
            if x < 0 or x + img_w > pdf_w or y < 0 or y + img_h > pdf_h:
                print("Advertencia: El mapa no cabe en la página. Ajusta el tamaño del mapa o la página del PDF.")
                return  # Detiene la generación del PDF y sale de la función

            # Insertar la imagen en el PDF
            pdf.image(temp_image_filename, x=x, y=y, w=img_w)

            # Actualizar la barra de progreso de la generación del PDF
            pdf_bar.update(1)

    # Cerrar la barra de progreso de la generación del PDF
    pdf_bar.close()

    # Guardar el PDF
    pdf.output(output_pdf_path)

    print(f"Archivo PDF generado exitosamente con polígonos destacados en {output_pdf_path}")

# Cargar el shapefile y obtener el CRS
shapefile, proyecto_crs = cargar_shapefile(shapefile_path)

# PARAMETROS PARA MUESTRA - Pruebas operativas
# Cargar el shapefile y obtener el CRS
shapefile_sample = shapefile.iloc[500021:500031]

# Generar polígonos en el PDF
generar_poligonos_en_pdf(shapefile_sample, output_pdf_path, proyecto_crs)

########
