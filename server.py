import socket
from _thread import *
from time import sleep

host = '192.168.56.1'
port = 2345
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


#TODO
#Check if client is still connected before sending message
#Find a time to disconnect clients (low priority)
#method "check_connection" needs testing


clients = []
verblist = ["gaming", "run", "code", "coding", "party", "draw", "act", "drive", "driving", "chat", "chatting", "walk"]


try:
    serverSocket.bind((host, port))
except socket.error as e:
    print(str(e))


print("Socket is listening...")
serverSocket.listen(10)


#method responsible for sending messages to a client
def threaded_client_sender(clientSocket, message):
    #is client alive?
    #if check_connection(clientSocket):
        for c in clients:

            # if c != clientSocket:
            #    try:
            #        c.send("ping".encode())
            #    except:
            #        print("A client has disconnected.")
            #        # client is removed from the clients list
            #        clients.remove(clientSocket)
            #        c.close()
            #    else:
            c.send(message.encode())


#a method responsible for receiving messages from a client
def threaded_client_listener(clientSocket):
    while True:
        received = clientSocket.recv(1024)
        msg = "Server: "+received.decode()
        print(received.decode(), end='')
        # threaded_client_sender(clientSocket, msg)
        if(clientSocket == clients[0]):
            sleep(3)
            inputHandler()


#takes input and sends to every client
def inputHandler():
    sleep(1)
    global sentence
    # only takes single verb as input for now
    sentence = str(input("Say something: "))
    print("Server: "+sentence)
    sentence = sentence.removesuffix("?")
    verb = ""
    print(sentence.split())
    for word in sentence.split():
        if word.lower() in verblist or word.removesuffix("ing").lower() in verblist:
            print("The verb is "+word+".")
            verb = word
            break


    if verb == "":
        print("Warning: No verb recognized")
        verb = "DefaultVerb"


    for c in clients:
        if sentence != "Bananas are weird":
            c.send(verb.encode())
        else:
            try:
                c.send("ping".encode())
            except:
                print("A client has disconnected.")
                # client is removed from the clients list
                clients.remove(c)
            else:
                print("Sending: "+sentence)


# thread which operates the inputHandler() method

# loop that takes care of new connections
def connectionListener():
    while True:
        clientSocket, addr = serverSocket.accept()  # accepts new connection
        print('Connected to: ', addr[0], ':', addr[1])
        clients.append(clientSocket)  # adds client to the list "clients"

        # client gets two threads, one for sending and one for receiving messages to and from the client.
        start_new_thread(threaded_client_listener, (clientSocket,))
        start_new_thread(threaded_client_sender, (clientSocket, "Welcome to my chatroom"))
        if (len(clients)) == 1:
            sleep(6)  # waits for a short amount of time after first client is connected
            start_new_thread(inputHandler, ())

start_new_thread(connectionListener())
