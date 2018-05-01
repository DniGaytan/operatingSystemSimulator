#Servidor TCP para proyecto de sistemas operativos

import socket
import time
import sys



#------------------------------------------------------------------------------------
#funciones SRT Y SJF no expropiativo

#se guardara con el formato (proceso, timestampInicio, CPU)
colaListosSRT = []
colaListosSJF = []

colaBloqueadosSRT = []
colaBloqueadosSJF = []


def ordenaSRT():
    """Ordena la cola de listos del algoritmo SRT"""

    pass

def ordenaSJF():
    """Ordena la cola de listos del algoritmo SJF no expulsivo"""
    pass

def creaProcesoSRT():
    """Mete un nuevo proceso en la cola de listos SRT"""
    pass

def creaProcesoSJF():
    """Mete un nuevo proceso en la cola de listos SJF"""
    pass


def cambiaEstadoProcesoSRT():
    """Mueve los procesos entre las diferentes colas y CPU"""
    pass

def cambiaEstadoProcesoSJF():
    """Mueve los procesos entre las diferentes colas y CPU"""
    pass


def main(politica):
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
            print('funciona')

            while True:
                #recibe datos del cliente   
                data = conexion.recv(256)
                #Elimina los comentarios de data
                data = data[0:data.find('/')]
                #divide data en palabras
                data = data.split()
                datos = []
                i = 0   

                for palabra in data:
                    datos[i] = palabra
                    i += 1


                if 'CREATE' == datos[1] :
                    #ejecuta la funcion creaProcesoSRT y guarda el PID retornado por la funcion
                    pid = creaProcesoSRT(int(datos[0]), int(datos[3]))
                    conexion.sendall('process with pid: ', pid, ' was created' )

                elif 'I/O' == datos[1]:
                    if 'START' == datos[2]:
                        cambiaEstadoProcesoSRT('IOSTART', int(datos[3]))
                        conexion.sendall('process with pid: ', pid, ' has been blocked')
                    else:
                        cambiaEstadoProcesoSRT('IOSEND', int(datos[3]))
                        conexion.sendall('process with pid: ', pid, ' has been take out of blocked list')
                else:
                    print('terminando conexion')
                    conexion.close()
                    sys.exit()
    

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
    finally:
        # Clean up the connection
        print >>sys.stderr, 'se fue al finally'
        conexion.close()

        

    # Receive the data 
    


#------------------------------------------------------------------------------------





#Verifica si el programa se esta ejecutando por si solo y no como modulo
if __name__ == "__main__":
    

    #recibe la politica a ejecutar como parametro en consola
    politica = sys.argv[1]
    main(politica)



