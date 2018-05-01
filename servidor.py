#Servidor TCP para proyecto de sistemas operativos

import socket
import time
import sys

#Establece un socket para el servidor
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#se utiliza '' para la direccion y el puerto 5555 (se puede usar cualquiera)
direccion_servidor = ('localhost', 10000)
serverSocket.bind(direccion_servidor)

#el servidor empieza a escuchar por peticiones
serverSocket.listen(1)

conexion,cliente_direccion = serverSocket.accept()

#------------------------------------------------------------------------------------
#funciones SRT Y SJF no expropiativo

#------------------------------------------------------------------------------------

#Recibe el primer mensaje del cliente y con esto elige que algoritmo utilizar
try:
    print >>sys.stderr, 'connection from', cliente_direccion

    # Receive the data 
    while True:   
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



