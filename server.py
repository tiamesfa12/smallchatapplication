# we start with importing and some starting values
import socket
import select

HEADER_LENGTH = 10
IP = # look at your ipv4 and use that for your ip when you run the code
PORT = 1234

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # setup our socket
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) # this modifies the socket to allow us to reuse the address

# we bind and listen
server_socket.bind((IP, PORT))

# next is to create a list of sockets for select to keep track of, as well as begin our clients dict
server_socket.listen()
sockets_list = [server_socket]

clients = {}
# the main job of the server is to receive messages, and then send them to clients that are connected clients. for receiving messages we create a function
def receive_message(client_socket): # handles message receiving
	try:
		message_header = client_socket.recv(HEADER_LENGTH)

		if not len(message_header): # if the client closes the connection, a socket.close() will be handed out and there will be no header
			return False

		message_length = int(message_header.decode("utf-8").strip()) # we do this to convert our header to a length
		return  {"header": message_header, "data": client_socket.recv(message_length)} # this allows to return data

	except:
		return False
while True:
	read_sockets, _, exception_sockets = select.select(sockets_list, [], sockets_list) # this is written as a read list, write list, and error list

	for notified_socket in read_sockets: # we iterate over the read_sockets list
		if notified_socket == server_socket: # this means someone just connected to the server and we need to accept and handle this connection
			client_socket, client_address = server_socket.accept() # will bring in that connection 

			user = receive_message(client_socket)
			if user is False: # if someone were to discontinue
				continue

			sockets_list.append(client_socket)

			clients[client_socket] = user # this saves the client's username, which is saved as the value key pair that is the socket object

			print(f"Accepted new connection from {client_address[0]}:{client_address[1]} username:{user['data'].decode('utf-8')}")

		else: # now we want a handle on this
			message = receive message(notified_socket)

			if message is False:
				print(f"Closed connection from {clients[notified_socket]['data'].decode('utf-8')}")
				sockets_list.remove(notified_socket) # we do this to take it out of the list
				del clients[notified_socket]
				continue



			user = clients[notified_socket]
			print(f"Received message from {user['data'].decode('utf-8')}: {message['data'].decode('utf-8')}")

			# now we need to share this message with everybody
			 for client_socket in clients:
			 	if client_socket != notified_socket:
			 		client_socket.send(user['header'] + user['data'] + message['header'] + message['data']) # we send all that information and we send a message as well so for the client it will display the username and the actual message

	for notified_socket in exception_sockets:
		sockets_list.remove(notified_socket)
		del clients[notified_socket]











