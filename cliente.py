#cliente para pruebas
#cliente for testing purposes

import socket
import sys

Clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

direccion_servidor = (str(socket.gethostbyname(socket.gethostname())), 10000)

Clientsocket.connect(direccion_servidor)

mensajes = ['create //process A', 'create //process B']

try:
	for mensaje in mensajes:
		Clientsocket.sendall(mensaje)

		respuesta = Clientsocket.recv(256)
finally:
	
	Clientsocket.close() 