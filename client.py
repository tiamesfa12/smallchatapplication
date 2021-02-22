# the client does two things, the client tells the server what the username is, and a infinite loop of sending and receiving messages with the server
import socket
import select
import errno 
import sys

HEADER_LENGTH = 10

IP = # in double quotes same from server.py you put your ipv4 from your wifi
PORT = 1234

my_username = input("Username: ")
# create the client socket
client_socket = socket.socket(socket.AF_INT, socket.SOCK_STREAM)
# now lets connect to ip and port
client_socket.connect((IP, PORT))
client_socket.setblocking(False)
# send information to the server
username = my_username.encode("utf-8")
username_header = f"{len(username):<{HEADER_LENGTH}}".encode("utf-8")
client_socket.send(username_header + username)

while True:
	message = input(f"{my_username} > ")

	if message:
		message = message.encode("utf-8")
		message_header = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")
		client_socket.send(message_header + message)

	
	try:
		while True:
			# receive things
			username_header = client_socket.recv(HEADER_LENGTH)
			if not len(username_header):
				print("connection has been closed by the server")
				sys.exit()

			username_length = int(username_header.decode("utf-8").strip())
			username = client_socket.recv(username_length).decode("utf-8")

			message_header = client_socket.recv(HEADER_LENGTH)
			message_length = int(message_header.decode("utf-8").strip())
			message = client_socket.recv(username_length).decode("utf-8")

			print(f"{username} > {message}")

	except IOError as e:
		if e.errno != errno.EAGAIN and e.errno != errno.EWOULDBLOCK:
			print('Reading error', str(e))
			sys.exit()
		continue


		except Exception as e:
			print('General error',str(e))
			sys.exit()
