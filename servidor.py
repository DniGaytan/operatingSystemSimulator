#Servidor TCP para proyecto de sistemas operativos

import socket
import time

#Establece un socket para el servidor
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#se utiliza '' para la direccion y el puerto 5555 (se puede usar cualquiera)
direccion_servidor = (str(socket.gethostbyname(socket.gethostname())), 10000)
serverSocket.bind(direccion_servidor)

#el servidor empieza a escuchar por peticiones
serverSocket.listen(1)

conexion,cliente_direccion = serverSocket.accept()

#------------------------------------------------------------------------------------
#funciones SRT Y SJF no expropiativo

#------------------------------------------------------------------------------------

#Recibe el primer mensaje del cliente y con esto elige que algoritmo utilizar
while True:
	data = conexion.recv(256)

	if data:
		#recibio datos
		pass
	else:
		#No recibio datos y por ende cerrara la conexion
		conexion.close()

print(data)



