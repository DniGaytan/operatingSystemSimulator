#Servidor TCP para proyecto de sistemas operativos

import socket
import time

#Establece un socket para el servidor
serverSocket = socket.socket(socket.AF_STREAM, socket.SOCK_STREAM)

#se utiliza '' para la direccion y el puerto 5555 (se puede usar cualquiera)
serverSocket.bind(str(socket.gethostbyname(socket.gethostname())), 5555)

#el servidor empieza a escuchar por peticiones
serverSocket.listen(1)

cliente_conexion,cliente_direccion = serverSocket.accept()

while True:
	#recibe un buffer de 256 bytes de parte del cliente	
	data = cliente_conexion.recv(256)

	

	if data == 'cierra':
		cliente_conexion.close()

	print('El cliente con direccion:{} dice: {} a la hora: {}'.append(cliente_direccion,data, time.localtime())
	cliente_conexion.sendall('Mensaje recibido')



