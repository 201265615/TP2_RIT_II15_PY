from math import sqrt
import re                       # para expresiones regulares
import csv
import snowballstemmer          # para aplicar el stemmer de snowball
from archivo import *
from archivo_invertido import *


########################
##
## Nombre:  aplicarStemmer
## Descripcion: aplica la técnica de Stemming a la lista de palabras y la retorna
##              
## Parametros:  pLista : lista con palabras de la busqueda [termino,importancia]
##              
## Return: [term,importancia]
##              
##              
##
########################

def aplicarStemmerConsulta(pLista):
    #print(pLista)
    print("aplicando stemming...")
    lista = []
    stemmer = snowballstemmer.stemmer('spanish')
    for i in pLista:
        #print(i[0])
        raiz = stemmer.stemWords([i[0]])[0]
        lista.append([raiz,i[1]])
        #print(i[0])
    #print(lista)
    return lista

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

def sustituirPalabrasConsulta(pTexto,pTablaReemplazo):
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
##              pTexto
## Return:
##              texto sin acentuaciones (sin tildes)
##
########################

def eliminarTildesConsulta(pLista):
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
    lista = []
    for i in pLista:
        lista.append([sustituirPalabrasConsulta(i[0],tablaReemplazo),i[1]])
    return lista


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

def ordenarLista(pLista,pLlave):
    return sorted(pLista,key=lambda x: x[pLlave], reverse=True)


########################
##
## Nombre: cargarDiccionario
## Descripcion:
##              lee el archivo de diccionario
## Parametros:
##              pRuta: ruta del archivo
## Return:
##              diccionario con terminos, inicio y longitud {termino: [inicio,longitud]}
##
########################

def cargarDiccionario(pRuta):
    # se abre el archivo y se indica que es unicode para que lea las tildes (en mi caso daba error si no lo hacia asi)
    archivo = open(pRuta,"r",encoding='utf-8');

    lista = {}

    # se leer el archivo linea por linea
    for linea in archivo:
        listaNueva = linea.rstrip("\n").split("\t")
        if(listaNueva[0] == ''):
            continue
        lista.update({str(listaNueva[0]):eval(listaNueva[1])})
    return lista



########################
##
## Nombre: cargarListaListas
## Descripcion:
##              lee el archivo csv y genera una lista de listas
## Parametros:
##              pRuta: ruta del archivo
## Return:
##              [[int,float],[int,float], ...]
##
########################

def cargarListaListas(pRuta):
    # se abre el archivo y se indica que es unicode para que lea las tildes (en mi caso daba error si no lo hacia asi)
    archivo = open(pRuta,"r",encoding='utf-8');

    lista = []

    # se leer el archivo linea por linea
    for linea in archivo:
        listaNueva = linea.rstrip("\n").split("\t")
        if(listaNueva[0] == ''):
            continue
        lista.append([int(listaNueva[0]),float(listaNueva[1])])
    return lista
    

########################
##
## Nombre: recibirConsultaBasica
## Descripcion:
##              ejecuta la consulta de tipo basica
## Parametros:
##              pTexto
## Return:
##              
##
########################

def recibirConsultaBasica(pTexto):
    #############################################################################
    #                                                                           #
    #                 DESCRIPCION DE LA EXPRESION REGULAR                       #
    #                                                                           #
    # group(termino)     ->    (?P<termino>\w*)      : termino                  #
    # group(importancia)  ->    (?P<importancia>\d)?      : importancia         #
    #                                                                           #
    #############################################################################
    
    # se declara el patron con los grupos
    patron = r'(?P<termino>[a-zA-Záéíóúñ]+|[0-9]+[\.\,0-9]*)\ (?P<importancia>\d)?'

    lista = []

    # se realiza la busqueda
    for busqueda in re.finditer(patron, pTexto):
        # se obtienen los valores de los grupos
        termino = busqueda.group('termino')
        importancia = busqueda.group('importancia')
        if(termino != "" and importancia != ""):
            if (importancia == None):
                importancia = 1 # valor default segun especificacion
            #print(str(termino)+"\t"+str(importancia))
            lista.append([str(termino),int(importancia)])
    return lista


def calcularNormaConsulta(pLista):
    norma = 0
    for i in pLista:
        norma += i[1]*i[1]
    return sqrt(norma)

########################
##
## Nombre: encontrarTermino
## Descripcion:
##              devuelve el inicio y la longitud del termino
## Parametros:
##              pK : termino
##              pDicc : diccionario
## Return:
##              [inicio,longitud]
##
########################

def encontrarTermino(pK,pDicc):
    if(pDicc.get(pK) == None):
        return [0,0]
    return pDicc.get(pK)


########################
##
## Nombre: extraerPostings
## Descripcion:
##              extrae los postings segun un rango
## Parametros:
##              pInicio
##              pLongitud
##              pPostings
## Return:
##              [inicio,longitud]
##
########################

def extraerPostings(pInicio,pLongitud,pPostings):
    return pPostings[pInicio:pInicio+pLongitud]
    


    
########################
##
## Nombre: calcularSimilitud
## Descripcion:
##              calcula la similitud de la consulta con los documentos
## Parametros:
##              pPesoDocumento,pPesoConsulta,pNormaDocumento,pNormaConsulta
## Return:
##              [docID,sim]
##
########################
def calcularSimilitud(pPesoDocumento,pPesoConsulta,pNormaDocumento,pNormaConsulta):
    return pPesoDocumento * (pPesoConsulta / pNormaConsulta)



########################
##
## Nombre: generarEscalafon
## Descripcion:
##              genera
## Parametros:
##              pRutaDirectorioIndices
##              pConsulta
## Return:
##              [docID,sim]
##
########################

def generarEscalafon(pRuta, pVectorSimilitudes):
    # se abre el archivo y se indica que es unicode para que lea las tildes (en mi caso daba error si no lo hacia asi)
    archivo = open(pRuta,"r",encoding='utf-8');
    dictRutas = {}
    # se leer el archivo linea por linea
    for linea in archivo:
        listaNueva = linea.rstrip("\n").split("\t")
        docID = int(listaNueva[0])
        ruta = str(listaNueva[1])
        dictRutas[docID] = ruta

    vectorNuevo = []
    
    for i in range(len(pVectorSimilitudes)):
        docID = pVectorSimilitudes[i][0]
        sim = pVectorSimilitudes[i][1]
        ruta = dictRutas.get(docID)
        listaNueva = [docID,sim,ruta]
        #print(listaNueva)
        vectorNuevo.append(listaNueva)
    return vectorNuevo
    


    
########################
##
## Nombre: consultaVectorial
## Descripcion:
##              realiza la consulta vectorial en los archivos
## Parametros:
##              pRutaDirectorioIndices
##              pConsulta
## Return:
##              [docID,sim]
##
########################

def consultaVectorial(pRutaDirectorioIndices,pConsulta):
    print("Ejecutando consulta vectorial...")

    diccionario = cargarDiccionario("diccionario.csv")
    postings = cargarListaListas("postings.csv")
    normas = cargarListaListas("normas.csv")
    
    # se abre el archivo y se indica que es unicode para que lea las tildes (en mi caso daba error si no lo hacia asi)
    archivo = open(pRutaDirectorioIndices+"/documentos.csv","r",encoding='utf-8');
    for ultimaLinea in archivo: pass # para leer ultima linea
    
    cantidadDocumentos = int(ultimaLinea.split()[0]) # se obtiene el ultimo docId para saber cantidad de documentos
    #print(cantidadDocumentos)
    
    # inicializar vector de similitudes en 0
    vectorSimilitudes = [[i,0.0] for i in range(cantidadDocumentos)] #[docID,sim]

    # hacer consulta en vectores
    vectorConsulta = recibirConsultaBasica(pConsulta)
    normaConsulta = calcularNormaConsulta(vectorConsulta)
    #print(vectorConsulta)
    vectorConsulta = aplicarStemmerConsulta(vectorConsulta)
    vectorConsulta = eliminarTildesConsulta(vectorConsulta)
    #print(vectorConsulta)

    for i in vectorConsulta:
        inicioLongitud = encontrarTermino(i[0],diccionario) # devuelve lista con [inicio,longitud]
        listaTemporalTermino = extraerPostings(inicioLongitud[0],inicioLongitud[1],postings) # devuelve lista con [[docID,peso], ... ] por cada termino
        for j in range(len(listaTemporalTermino)-1):
            # i[0] : termino 
            # i[1] : peso termino
            # j[0] : docID
            # j[1] : peso documento
            #print(i[0],i[1],listaTemporalTermino[j][0],listaTemporalTermino[j][0])
            vectorSimilitudes[listaTemporalTermino[j][0]][1] =  calcularSimilitud(listaTemporalTermino[j][1],float(i[1]),normas[listaTemporalTermino[j][0]][1],normaConsulta) # se calcula la similitud ## FALTA hacer como en espe
            vectorSimilitudes = generarEscalafon(pRutaDirectorioIndices+"documentos.csv",vectorSimilitudes)
            vectorSimilitudes = ordenarLista(vectorSimilitudes,1) # ordenado por peso o similitud
    return vectorSimilitudes



def cargarEscalafon(pRuta):
    # se abre el archivo y se indica que es unicode para que lea las tildes (en mi caso daba error si no lo hacia asi)
    archivo = open(pRuta,"r",encoding='utf-8');
    dictRutasEscalafon = {}
    # se leer el archivo linea por linea
    for linea in archivo:
        listaNueva = linea.rstrip("\n").split("\t")
        if(len(listaNueva) == 3):
            docID = int(listaNueva[0])
            sim = float(listaNueva[1])
            ruta = str(listaNueva[2])
            if(sim != 0):
                dictRutasEscalafon[docID] = [sim,ruta]
    return dictRutasEscalafon


def cargarEscalafonHtml(pRuta):
    # se abre el archivo y se indica que es unicode para que lea las tildes (en mi caso daba error si no lo hacia asi)
    archivo = open(pRuta,"r",encoding='utf-8');
    listaListas = []
    # se leer el archivo linea por linea
    for linea in archivo:
        listaLocal = linea.rstrip("\n").split("\t")
        listaListas.append(listaLocal)        
    return listaListas


def consultaAvanzada(pRutaEscalafon,pExpresionRegular):
    dictSimRutasEscalafon = cargarEscalafon(pRutaEscalafon+"escalafon.csv")
    dictRutasEscalafon = {}
    for docID,SimRuta in dictSimRutasEscalafon.items():
        dictRutasEscalafon[docID] = SimRuta[1]
        
    dictTextoEscalafon = extraerTextoArchivos(dictRutasEscalafon)
    
    listaNuevoEscalafon = []
    for docID,texto in dictTextoEscalafon.items():
        listaResultado = re.findall(r''+pExpresionRegular, texto)
        if(len(listaResultado) > 0):
            listaNueva = dictSimRutasEscalafon.get(docID)
            listaNuevoEscalafon.append([docID,listaNueva[0],listaNueva[1]])
##    crearCSVDict("palabras.csv",dictPalabras)
    return ordenarLista(listaNuevoEscalafon,1)   
    
