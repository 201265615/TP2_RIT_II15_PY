import re                       # para expresiones regulares
from math import log10,sqrt
import snowballstemmer          # para aplicar el stemmer de snowball
import dehtml
import archivo
from collections import *

########################
##
## Nombre:  aplicarStemmer
## Descripcion: aplica la técnica de Stemming a la lista de palabras y la retorna
##              
## Parametros:  diccionario de palabras de archivos -> diccionario {docId : [palabras]}
##              
## Return:  diccionario de raíces de palabras -> diccionario {docId : [raices]}
##              
##              
##
########################

def aplicarStemmer(pDictPalabrasArchivos):
    print("aplicando stemming...")
    dictRaices = {}
    stemmer = snowballstemmer.stemmer('spanish')
    for docId,palabras in pDictPalabrasArchivos.items():
        raices = stemmer.stemWords(palabras)
        dictRaices[docId] = raices
##    archivo.archivo.crearCSVDict(".\stemming.csv",dictRaices)
    return dictRaices

########################
##
## Nombre: sustituirPalabras
## Descripcion: 
##              lee el texto y sustituye las palabras segun la tabla de reemplazo
## Parametros:
##              pTexto: texto al cual hay que sustituir las palabras
##              tablaReemplazo: contiene las llaves y valores a sustituir
## Return:
##              nuevoTexto
##
########################

def sustituirPalabras(pTexto,pTablaReemplazo):
    # se crea una expresion regular desde el diccionario
    regex = re.compile("(%s)" % "|".join(map(re.escape, pTablaReemplazo.keys())))

    # se analiza el texto y si con tiene una abreviatura se reemplaza
    nuevoTexto = regex.sub(lambda x: str(pTablaReemplazo[x.string[x.start() :x.end()]]), pTexto)
    return nuevoTexto


########################
##
## Nombre: eliminarTildes
## Descripcion:
##              sustituye las letras tildadas por letras sin tildar
## Parametros:
##              pDictPalabrasArchivos -> {docId : texto}
## Return:
##              dictSinTildes -> {docId : texto sin acentuaciones (sin tildes)}
##
########################

def eliminarTildes(pDictPalabrasArchivos):
    print("eliminando tildes de las raices...")
    tablaReemplazo = {
            "á"     :   "a",
            "é"     :   "e",
            "í"     :   "i",
            "ó"     :   "o",
            "ú"     :   "u",
            "\r"    :   " ",
            "\n"    :   " ",
            "\t"    :   " "
        }
    dictSinTildes = {}
    for docId, raices in pDictPalabrasArchivos.items():
        raicesSinTildes = []
        for raiz in raices:
            raizSinTildes = sustituirPalabras(raiz,tablaReemplazo)
            raicesSinTildes.append(raizSinTildes)
        dictSinTildes[docId] = raicesSinTildes
    return dictSinTildes
        

########################
##
## Nombre: extraerTextoArchivos
## Descripcion:
##              elimina los tags HTML de todos los documentos
## Parametros:
##              pDictRutasArchivos: diccionario con las rutas de todos los documentos -> {docId : ruta}
## Return:
##              diccionario con el docId y el texto sin tags HTML -> {docId : texto}
##
########################

def extraerTextoArchivos(pDictRutasArchivos):
    print("extrayendo texto de los archivos...")
    dictTexto = {}
    for docId,rutaArchivo in pDictRutasArchivos.items():
        texto = archivo.eliminarTagsHTML(archivo.cargarArchivo(rutaArchivo))
        dictTexto[docId] = texto;
##    archivo.archivo.crearCSVDict("texto.csv",dictTexto)
    return dictTexto
        


########################
##
## Nombre: extraerPalabrasArchivos
## Descripcion:
##              extrae las palabras o terminos de todos los arhivos
## Parametros:
##              pListaTextoArchivos: lista con el texto sin tags HTML
## Return:
##              lista con las palabras
##              [(idDocumento,termino)]
##
########################

def extraerPalabrasArchivos(pDictTextoArchivos):
    print("extrayendo palabras de archivos...")
    dictPalabras = {}
    for docId,texto in pDictTextoArchivos.items():
        listaPalabras = re.findall(r'[a-zA-Záéíóúñ]+|[0-9]+[\.\,0-9]*', texto)
        dictPalabras[docId] = listaPalabras
##    archivo.archivo.crearCSVDict("palabras.csv",dictPalabras)
    return dictPalabras


########################
##
## Nombre: ordenarListaTuplas
## Descripcion:
##              ordena las listas de tuplas segun el elemento de la tupla que se seleccione(llave)
## Parametros:
##              pLista: lista a ordenar
##              pLlave: valor por el cual se ordenara (numero de columna)
## Return:
##              lista ordenada
##              [(idDocumento,termino)]
##
########################

def ordenarListaTuplas(pLista,pLlave):
    return sorted(pLista,key=lambda x: x[pLlave])

########################
##
## Nombre: ordenarTerminosDict
## Descripcion:
##              ordena los elementos de un diccionario
## Parametros:
##              pDictSinTildes -> diccionario que tiene como valor texto sin tildes
## Return:
##              diccionario ordenado
##              
##
########################

def ordenarTerminosDict(pDictSinTildes):
    dictOrdenado = {}
    for docId, raices in pDictSinTildes.items():
        raices = sorted(raices)
        dictOrdenado[docId] = raices
    return dictOrdenado

########################
##
## Nombre: contarTerminos
## Descripcion:
##              cuenta la frecuencia los terminos por documento
## Parametros:
##              pDictTerminosOrdenados -> diccionario
## Return:
##              frecuencia de las palabras por documento -> diccionario
##
########################

def contarTerminos(pDictTerminosOrdenados):
    print("contando terminos por documento")
    dictFrecuenciasTerm = {}#diccionario de frecuencias por termino
    for docId, terminos in pDictTerminosOrdenados.items():
        terminos = sorted(list(Counter(terminos).items()))
        for termino in terminos:
            try:
                dictFrecuenciasTerm[termino[0]] += [[docId,termino[1]]]
            except KeyError:
                dictFrecuenciasTerm[termino[0]] = [[docId,termino[1]]]
##    archivo.archivo.crearCSVDict("frecTerm.csv",dictFrecuenciasTerm)
##    archivo.archivo.crearCSVDict("frecDoc.csv",dictFrecuenciasDoc)
    return dictFrecuenciasTerm

########################
##
## Nombre: calcularPesos
## Descripcion:
##              calcula los pesos de los terminos dado un conjunto de frecuencias,
##              el N y el Ni (en cuantos documentos aparece un termino)
## Parametros:
##              pDIctFrecuenciasTerm: 
##              N: (numero de documentos)
##              pDictNi : diccionario con los ni respectivos a cada termino
## Return:
##              diccionario de pesos por terminio
##
########################

def calcularPesos(pDictFrecuenciasTerm,pN,pDictNi):
    print("calculando pesos de los terminos")
    dictPesos = {}
    cuadrados = {}
    for termino, frecuencias in pDictFrecuenciasTerm.items():
        for frecuencia in frecuencias:
            frecuencia[1] = (1+log10(frecuencia[1]))*(log10(pN/pDictNi[termino]))
            try:
                cuadrados[frecuencia[0]] += frecuencia[1]**2
            except KeyError:
                cuadrados[frecuencia[0]] = frecuencia[1]**2
        dictPesos[termino] = frecuencias
    for docId,cuadrado in cuadrados.items():
        cuadrados[docId] = sqrt(cuadrado)
    archivo.crearCSVDict("normas.csv",cuadrados)
    for termino, pesos in dictPesos.items():
        for peso in pesos:
            peso[1] = peso[1]/cuadrados[peso[0]]
        dictPesos[termino] = pesos
##    archivo.archivo.crearCSVDict("pesos.csv",dictPesos)
    return dictPesos

########################
##
## Nombre: calcularNi
## Descripcion:
##              calcula la cantidad de documentos en los que aparece un termino
##              
## Parametros:
##              pDIctFrecuenciasTerm
##              
##              
## Return:
##              diccionario de ni por termino {termino : ni}
##
########################

def calcularNi(pDictFrecuenciasTerm):
    dictNi = {}
    for termino,frecuencias in pDictFrecuenciasTerm.items():
        dictNi[termino] = len(frecuencias)
##    archivo.archivo.crearCSVDict("ni.csv",dictNi)
    return dictNi

########################
##
## Nombre: crearDiccPosts
## Descripcion:
##              crea el archivo de diccionario y postings
##  
## Parametros:
##              pDictPesos -> diccionario de pesos por termino
##              
##              
## Return:
##              [diccionario,postings] -> diccionario {}, postings []
##
########################
        
def crearDiccPosts(pDictPesos):
    diccionario = {}
    postings = []
    indice_postings = 0
    for termino,pesos in pDictPesos.items():
        diccionario[termino] = [indice_postings,0]
        for peso in pesos:
            docId = peso[0]
            postings += [[docId,peso[1]]]
            indice_postings += 1
        diccionario[termino][1] = len(pesos)
    archivo.crearCSVDict("diccionario.csv",diccionario)
    archivo.crearCSV("postings.csv",postings)
    return [diccionario,postings]
        
        

            
    

















