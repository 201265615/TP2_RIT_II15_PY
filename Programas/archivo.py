import csv                      # para crear csv
import os                       # para obtener listado de directorios y subdirectorios
from collections import Counter # para contar apariciones de palabras
import collections              # para las colecciones
import random                   # para generar el nombre del archivo
import codecs                   # para leer unicode
import dehtml
from markup import markup       # para generar el html
from consultas import *
from archivo_invertido import *


########################
##
## Nombre: cargarArchivo
## Descripcion:
##              Abre y carga el archivo que se seleccione segun la ruta
## Parametros:
##              pRuta: ruta donde se encuentra el archivo
## Return:
##              texto leido
##              string
##
########################

def cargarArchivo(pRuta):
    # se abre el archivo y se indica que es unicode para que lea las tildes (en mi caso daba error si no lo hacia asi)
    archivo = open(pRuta,"r",encoding='utf-8');

    textoLeido = ""

    # se leer el archivo linea por linea
    for linea in archivo:
        textoLeido += linea
    return textoLeido.lower() #convierte texto a minuscula

########################
##
## Nombre: crearCSV
## Descripcion:
##              crea un archivo csv (valores separados por comas)
## Parametros:
##              pRuta: ruta y nombre donde se creara
##              pListaValores : lista de valores
## Return:
##              0
##
########################
        
def crearCSV(pRuta,pListaValores):
    print("creando archivo csv " + pRuta + "...")
    c = csv.writer(open(pRuta, "w",encoding='utf-8'), delimiter = "\t", lineterminator="\n")
    c.writerows(pListaValores)

def crearCSVDict(pRuta,pDictValores):
    print("creando archivo csv " + pRuta + " desde diccionario...")
    c = csv.writer(open(pRuta,'w',encoding='utf-8'),delimiter = "\t", lineterminator="\n")
    for key, value in pDictValores.items():
        c.writerow([key,value])

########################
##
## Nombre: eliminarTagsHTML
## Descripcion:
##              elimina los tags HTML
## Parametros:
##              pDocumento: texto del documento
## Return:
##              texto sin tags HTML
##              string
##
########################
# quizas hace falta quitar ↑ y @import "/static/skins/monobook/IE50Fixes.css";
    
def eliminarTagsHTML(pDocumento):
    return dehtml.dehtml(pDocumento)

########################
##
## Nombre: obtenerRutasArchivos
## Descripcion:
##              genera todas las rutas de achivos (incluso dentro de subdirectorios)
## Parametros:
##              pDirectorio: directorio raiz
## Return:
##              lista con las rutas de los archivos
##              [listaRutasArchivos]
##
########################

def obtenerRutasArchivos(pDirectorio):
    print("obteniendo rutas de archivos...")
    rutasArchivos = []

    # Recorrer el arbol
    for raiz, directorios, archivos in os.walk(pDirectorio):
        for nombreArchivo in archivos:
            # Unir los dos strings en orden desde la ruta del archivo
            if(nombreArchivo != ".DS_Store"): # evitar que se cree una ruta con .DS_Store como nombre
                rutaArchivo = os.path.join(raiz, nombreArchivo)
                rutasArchivos.append(rutaArchivo)
    return rutasArchivos

########################
##
## Nombre: generarTuplasRutasArchivos
## Descripcion:
##              Genera las tuplas un id de documento y la ruta del documento
## Parametros:
##              pListaRutasArchivos: lista de las rutas generadas con obtenerRutasArchivos(pDirectorio)
## Return:
##              lista de tuplas con idDocumento y la ruta
##              [(idDocumento,rutaDocumento)]
##
########################

def generarTuplasRutasArchivos(pListaRutasArchivos):
    print("generando tuplas de rutas de archivos...")
    dictDocumentos = {}
    docId = 0
    for ruta in pListaRutasArchivos:
        dictDocumentos[docId] = ruta
        docId += 1
    return dictDocumentos

########################
##
## Nombre: eliminarStopwords
## Descripcion: 
##              lee el texto y eliminar los stopwords
## Parametros:
##              pListaPalabras: texto al cual hay que eliminar stopwords
##              pUbicacionStopwords: ruta o path donde se encuenta el archivo de stopwords
## Return:
##              texto sin stopwords
##              [listaPalabrasSinStopwords]
##
########################

def eliminarStopwords(pListaPalabras,pUbicacionStopwords):
    print("eliminando stopwords...")
    dictPalabras = {}
    listaStopwords = cargarArchivo(pUbicacionStopwords)
    for docId, palabras in pListaPalabras.items():
        palabras = list(filter(lambda palabra: palabra not in listaStopwords, palabras))
        dictPalabras[docId] = palabras
    return dictPalabras

########################
##
## Nombre: crearHtml
## Descripcion: 
##              dado un conjunto de similitudes crea un archivo html
## Parametros:
##              pListaSimilitudes: lista de similitudes de la forma [[docId,similitud]]
##              
## Return:
##              0
##              
##
########################
        
def crearHtml(pRutaEscalafon,pRangoInf,pRangoSup,pRutaArchivoSalidaHTML):
    pRangoInf = int(pRangoInf)
    pRangoSup = int(pRangoSup)
    print("Creando reporte HTML...")
    escalafon = cargarEscalafonHtml(pRutaEscalafon)

    consulta = escalafon[len(escalafon)-1][0]

    fileName = ''.join(random.choice('0123456789abcdef') for i in range(8))

    print("Nombre del archivo de reporte: " + fileName)

    reportTableHeaders = ('Posición','DocId','Similitud','Ruta','Texto Ejemplo')

    reportTitle = "Reporte " + fileName

    reportStyles = ( './css/styles.css' )

    reportCharset = ("utf-8")

    report = markup.page()

    report.init( css = reportStyles, title = reportTitle, charset = reportCharset)

    report.h1( "Reporte " + fileName + " || Consulta: '" + consulta + "'", class_="report-header")

    report.p( "La ruta de los archivos son en base a la ruta del archivo de indices" )

    report.table( class_ = 'ranking' )

    report.tr()

    report.th(reportTableHeaders, class_= 'ranking-headers')

    report.tr.close()
    #print(pRangoInf)
    #print(pRangoSup)

    escalafonTemporal = escalafon[pRangoInf:pRangoSup]
    #print(escalafonTemporal)
    posicion = pRangoInf
    for i in escalafonTemporal:
        report.tr()
        
        textoEjemplo = obtenerTextoEjemplo(i[2],i[0])

        report.td([posicion+1]+i+[textoEjemplo])
        
        report.tr.close()

        posicion += 1
        
    report.table.close()

    report.h5( "Autores: José Ricardo Brenes Camacho && Kevin Escobar Miranda", class_= 'footer' )

    f = open(pRutaArchivoSalidaHTML+fileName+".html",'w', encoding="utf-8")

    f.write(str(report))

    f.close()

def obtenerTextoEjemplo(pRuta,pDocId):

    archivo = cargarArchivo(pRuta)

    primerP = archivo.find("<p>")
    segundoP = archivo.find("<p>",primerP+3)

##    print(archivo[segundoP+3:segundoP+200])
    
    texto = procesarTextoEjemplo(archivo[segundoP+3:segundoP+200])
    return(texto+"...")

def procesarTextoEjemplo(pTexto):

    tablaReemplazo = {
        "<" : "&lt",
        ">" : "&gt",
        "\n" : ""
    }

    textoNuevo = sustituirPalabras(pTexto,tablaReemplazo)

    return textoNuevo
    

    
    

    
            
                
        
