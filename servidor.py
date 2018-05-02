#Servidor TCP para proyecto de sistemas operativos

#!/usr/bin/python
# -*- coding: ascii -*-

import socket
import time
import sys



#------------------------------------------------------------------------------------
#funciones SRT Y SJF no expropiativo

SRTPID = 1
TIMESTAMP = 0

#se guardara con el formato (proceso, timestampInicio, CPU)
colaListosSRT = []
colaListosSJF = []

colaBloqueadosSRT = []
colaBloqueadosSJF = []

CPU = None
CPU2 = None

colaProcesosTerminadosSRT = []


def ordenaColaSRT():
    """Ordena la cola de listos del algoritmo SRT"""
    for indexI in range(0, colaListosSRT.length()):
        for indexJ in range(indexI, colaListosSRT.length()):
            if colaListosSRT[indexI][2] > colaListosSRT[indexJ][2]:
                container = colaListosSRT[indexI]
                colaListosSRT[indexI] = colaListosSRT[indexJ]
                colaListosSRT[indexJ] = container

def ordenaSJF():
    """Ordena la cola de listos del algoritmo SJF no expulsivo"""
    pass

def creaProcesoSRT(timestampLlegada, tiempoCPU):
    """Mete un nuevo proceso en la cola de listos SRT"""
    proceso = [SRTPID, timestampLlegada, tiempoCPU, tiempoCPU]
    colaListosSRT.append(proceso)
    SRTPID += 1
    return proceso[0]


def creaProcesoSJF():
    """Mete un nuevo proceso en la cola de listos SJF"""
    pass


def cambiaEstadoProcesoSRT(IOEstado, PID):
    """Mueve los procesos entre las diferentes colas y CPU"""
    if IOEstado == 'START':
        if PID == CPU[2]:
            colaBloqueadosSRT.append(CPU)
            CPU = colaListosSRT[0]
        else:
            for index in range(0, colaListosSRT.length()):
                if colaListosSRT[index] == PID:
                    colaBloqueadosSRT.append(colaListosSRT[index])
                    colaListosSRT.pop(index)

    elif IOEstado == 'END':
        for index in range(0, colaBloqueadosSRT.length()):
            if colaBloqueadosSRT[index] == PID:
                colaListosSRT.append(colaBloqueadosSRT[index])
                colaBloqueadosSRT.pop(index)
    else:
        print('error en IO ', IOEstado)


    pass

def cambiaEstadoProcesoSJF():
    """Mueve los procesos entre las diferentes colas y CPU"""
    pass

def ejecutaAlgoritmoSRT(usaCPU2):
    """Simulacion del algoritmo SRT despues de haber checado el orden, creacion y estados"""

    #checa si CPU esta vacio, si si entonces mete el primer proceso que este dentro de la 
    #cola de listos
    if CPU == None:
        CPU = colaListosSRT[0]
        colaListosSRT.pop(0)

    if usaCPU2 and CPU2 == None:
        CPU2 = colaListosSRT[0]
        colaListosSRT.pop(0)


    #checa si el proceso que esta adentro de CPU tiene mayor cputime que el que esta primero en la
    #cola de listos
    if CPU[2] > colaListosSRT[0][2]:
        colaListosSRT.append(CPU)
        CPU = colaListosSRT[0][2]

    if CPU2[2] > colaListosSRT[0][2] and usaCPU2:
        colaListosSRT.append(CPU2)
        CPU2 = colaListosSRT[0][2]

    #checa si el proceso que esta dentro de CPU ya termino con su cputime, si si lo manda a la 
    #cola de procesos terminados
    if CPU[2] > 0:
        TIMESTAMP += 1
        CPU[2] -= 1
    else:
        if not CPU == None: 
            procesoTerminado = [CPU[0], CPU[1], TIMESTAMP, CPU[3]]
            colaProcesosTerminadosSRT.append(procesoTerminado)
            CPU = None

    if CPU2[2] > 0:
        CPU[2] -= 1
    else:
        if not CPU2 == None:
            procesoTerminado = [CPU2[0], CPU2[1], TIMESTAMP, CPU2[3]]
            colaProcesosTerminadosSRT.append(procesoTerminado)
            CPU2 = None

    return mandaEstadoActualSRT()

def mandaEstadoActualSRT():
    """cada segundo manda el reporte del estado actual del algoritmo"""
    mensaje = "Proceso , CPUtime , bloqueado , turnaround , tiempoEspera \n"

    for proceso in colaListosSRT:
        mensaje += "{}  ,  {}  ,  'no'  ,  {}  ,  {}  , \n".format(proceso[0], proceso[2], 'aun no acaba', 'aun no acaba')
    if not CPU is None:
        mensaje += "{}  ,  {}  ,  'no'  ,  {}  ,  {}  , \n".format(CPU[0], CPU[2], 'aun no acaba', 'aun no acaba')

    if not CPU2 is None:
        mensaje += "{}  ,  {}  ,  'no'  ,  {}  ,  {}  , \n".format(CPU2[0], CPU2[2], 'aun no acaba', 'aun no acaba')

    for proceso in colaProcesosTerminadosSRT:
        mensaje += "{}  ,  '0'  ,  'no'  ,  {}  ,  {}  , \n".format(proceso[0], proceso[1] - proceso[2],(proceso[1] - proceso[2]) - proceso[3])
    return mensaje




def main(politica, cpusUso):
    if cpusUso > 1:
        usaCPU2 = True;
    #Establece un socket para el servidor
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    #se utiliza '' para la direccion y el puerto 5555 (se puede usar cualquiera)
    direccion_servidor = ('localhost', 10000)
    serverSocket.bind(direccion_servidor)

    #el servidor empieza a escuchar por peticiones
    serverSocket.listen(1)

    conexion,cliente_direccion = serverSocket.accept()

    try:

        if politica == 'SRT':
            primerMensaje = True

            while True:
                #recibe datos del cliente   
                data = conexion.recv(256)

                #si no hay datos en el mensaje termina la conexion 
                if not data:
                    print('terminando conexion')
                    conexion.close()
                    sys.exit()

                #Elimina los comentarios de data
                data = data[0:data.find('/')]
                #divide data en palabras
                data = data.split()
                datos = []
                i = 0   

                for palabra in data:
                    datos[i] = palabra
                    i += 1

                if primerMensaje:
                    TIMESTAMP = int(datos[0])
                    primerMensaje = False


                if 'CREATE' == datos[1] :
                    #ejecuta la funcion creaProcesoSRT y guarda el PID retornado por la funcion
                    pid = creaProcesoSRT(int(datos[0]), int(datos[3]))
                    conexion.sendall('process with pid: ', pid, ' was created' )

                elif 'I/O' == datos[1]:
                    if 'START' == datos[2]:
                        cambiaEstadoProcesoSRT('START', int(datos[3]))
                        conexion.sendall('process with pid: ', pid, ' has been blocked')
                    else:
                        cambiaEstadoProcesoSRT('END', int(datos[3]))
                        conexion.sendall('process with pid: ', pid, ' has been take out of blocked list')
                else:
                    pass

                #Ejecuta el algoritmo SRT despues de analizar el mensaje recibido
                mensaje = ejecutaAlgoritmoSRT(usaCPU2)
                conexion.sendall(mensaje)
                    

        elif politica == 'SJF':

            while True:
                #recibe datos del cliente   
                data = conexion.recv(256)
                print >>sys.stderr, 'server received "%s"' % data
                if data:
                    print >>sys.stderr, 'sending answer back to the client'
            
                    conexion.sendall('process created')
                else:
                    print >>sys.stderr, 'no data from', cliente_direccion
                    conexion.close()
                    sys.exit()
        else:
            print('Politica incorrecta')

    finally:
        # Clean up the connection
        print >>sys.stderr, 'se fue al finally'
        conexion.close()
#------------------------------------------------------------------------------------





#Verifica si el programa se esta ejecutando por si solo y no como modulo
if __name__ == "__main__":
    #recibe la politica a ejecutar como parametro en consola
    politica = sys.argv[1]
    contexto = sys.argv[2]
    cpus = sys.argv[3]
    main(politica)



