#!/usr/bin/env python
# -*- coding: utf-8 -*-

######################################################
##                                                  ##
##       Instituto Tecnologico de Costa Rica        ##
##           Segundo Proyecto Programado            ##
##       Recuperacion de Informacion Textual        ##
##                                                  ##
######################################################
##                                                  ##
## Autores:                                         ##
##        Jose Ricardo Brenes Camacho - 201236179   ##
##        Kevin Alonso Escobar Miranda - 201265615  ##
## Profesor: Jose Enrique Araya Monge               ##
## FechaCreacion: 26 de octubre de 2015             ##
##                                                  ##
######################################################
##                                                  ##
##                  Nomenclatura                    ##
## Funciones:                                       ##
##              deben iniciar en minuscula          ##
##              primer palabra verbo infinitivo     ##
##              segunda palabra describe funcion    ##
##              cada palabra inicia con mayuscula   ##
##              Ejemplo: ejemplicarFuncion          ##
##                                                  ##
## Parametros:                                      ##
##              deben tener el prefijo p            ##
##              seguido de la descripcion           ##
##              cada palabra inicia en mayuscula    ##
##              Ejemplo: pParametroEjemplo          ##
##                                                  ##
## Bibliotecas Externas:                            ##
##              dehtml: elimina tags html del texto ##
##              snowball: genera raices (stemming)  ##
##              markup: para generar html           ##
##                                                  ##
######################################################

from time import gmtime, strftime # para la fecha y hora
from archivo import *
from archivo_invertido import *
from consultas import *


########################
##
## Nombre: main
## Descripcion:
##              funcion principal
##              
########################

def main():
    while(True):
        print("Escribe una de las siguientes acciones: \n"+
              "• indexar RutaDirectorioColeccion RutaArchivoStopwords RutaDirectorioIndices\n"+
              "• consultar RutaDirectorioIndices RutaEscalafon “Consulta”\n"+
              "• mostrar RutaEscalafon RangoInferior RangoSuperior RutaArchivoSalidaHTML\n"+
              "• refinar RutaEscalafon RutaNuevoEscalafon “ExpresionRegular”\n"+
              "• salir\n")
        
        opcion = str(input(""))
        opcion = opcion.split()
        accion = opcion[0]
        if(accion == "indexar"):
##            ..\Geografia .\stopwords.txt \
            print("indexar")
            rutaDirectorioColeccion = opcion[1]
            rutaArchivoStopwords = opcion[2]
            rutaDirectorioIndices = opcion[3]
            print(rutaDirectorioIndices+"documentos.csv")

            # Generar Archivo de Rutas
            listaRutasArchivos = obtenerRutasArchivos(rutaDirectorioColeccion)
            global ene
            ene = len(listaRutasArchivos)
            
            # Generar diccionario con el docId y la ruta del archivo
            dictTuplasRutas = generarTuplasRutasArchivos(listaRutasArchivos)

            crearCSVDict(rutaDirectorioIndices+"documentos.csv",dictTuplasRutas)##crear csv para un diccionario, arreglar ruta
            
##            # Generar Archivo Invertido (segun 071_Archivos_Invertidos TecDigital)
            
             # Obtener texto por documento
            dictTextoArchivos = extraerTextoArchivos(dictTuplasRutas)
            
             # Extraer palabras del texto de cada documento
            dictPalabrasArchivos = extraerPalabrasArchivos(dictTextoArchivos)
##
##            # Eliminar palabras comunes
##            ".\stopwords.txt"
            dictPalabrasArchivos = eliminarStopwords(dictPalabrasArchivos,rutaArchivoStopwords)
##
##            # Extraer de raices(stemming)
            dictRaices = aplicarStemmer(dictPalabrasArchivos) #falta hacer funcion de stemming
##
##            # Eliminar tildes
            dictRaicesSinTildes = eliminarTildes(dictRaices)
##            
##            # Ordenar por termino
            dictTerminosOrdenados = ordenarTerminosDict(dictRaicesSinTildes)
##
##            # Obtener frecuencia de palabras por documento
            dictFrecuencias = contarTerminos(dictTerminosOrdenados)

             # Calculo de ni para cada termino
            dictNi = calcularNi(dictFrecuencias)

             # Calculo de pesos
            dictPesos = calcularPesos(dictFrecuencias,ene,dictNi)
            
             # Creacion de diccionario y postings
            dictYPostings = crearDiccPosts(dictPesos)
            
        elif(accion == "consultar"):
            print("consultar")
            rutaDirectorioIndices = opcion[1]
            rutaEscalafon = opcion[2]
            consulta = opcion[3:]
            consulta = ' '.join([palabra for palabra in consulta])
            vectorSimilitudes = consultaVectorial(rutaDirectorioIndices,consulta)
            vectorSimilitudes.append([str(eval(consulta)) + strftime("%a, %d %b %Y %X", gmtime())])
            
            crearCSV(rutaEscalafon+"escalafon.csv",vectorSimilitudes)

        elif(accion == "mostrar"):
            print("mostrar")
            rutaEscalafon = opcion[1]
            rangoInferior = opcion[2]
            rangoSuperior = opcion[3]
            rutaArchivoSalidaHTML = opcion[4]
            crearHtml(rutaEscalafon,rangoInferior,rangoSuperior,rutaArchivoSalidaHTML)
            

        elif(accion == "refinar"):
            print("refinar")
            rutaEscalafon = opcion[1]
            rutaNuevoEscalafon = opcion[2]
            expresionRegular = opcion[3:]
            expresionRegular = ' '.join([palabra for palabra in expresionRegular])
            dictEscalafonNuevo = consultaAvanzada(rutaEscalafon,expresionRegular)
            dictEscalafonNuevo.append([str(eval(consulta)) + strftime("%a, %d %b %Y %X", gmtime())])
            crearCSV(rutaNuevoEscalafon+"escalafonNuevo.csv",dictEscalafonNuevo)
            

        elif(accion == "salir"):
            exit()

        else:
            print("Error, accion no definida.")

main()
