import socket
from _thread import *
from time import sleep

host = '127.0.0.1'
port = 2345
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# TODO
# Check if client is still connected before sending message
# Find a time to disconnect clients (low priority)
# method "check_connection" needs testing


clients = []
responses = []

# words that change by more that just +ing are written two times
verblist = ["gaming", "run", "running", "code", "coding", "party", "draw", "act", "drive",
            "driving", "chat", "chatting", "walk", "fly", "dance", "dancing", "drink",
            "climb", "cook", "ride", "riding", "write", "writing", "hunt", "swim", "swimming",
            "sit", "sitting", "talk", "talking"]

try:
    serverSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print("Socket is listening...")
serverSocket.listen(10)


# pings all clients and removes "dead" clients
def connectionChecker():
    print("Pinging clients")
    for c in clients:
        try:
            c.send("ping".encode())
        except:
            print("A client has disconnected")
            clients.remove(c)
        else:
            print("Pinging complete")
            sleep(0.5)


# method responsible for sending messages to a client
def threaded_client_sender(clientSocket, message):
    # is client alive?
    for c in clients:  # sends message to all clients
        c.send(message.encode())


# prints all responses collected in the responses list
def printResponses():
    for response in responses:  # prints every response
        print(response)
    responses.clear()  # clears list for a new round of dialogue
    inputHandler()


# a method responsible for receiving messages from a client
def threaded_client_listener(clientSocket):
    while True:
        received = clientSocket.recv(1024)
        if received.decode() == "Alive":
            print("Client is still alive")
        else:
            clients.remove(clientSocket)
            print("Received a response")
            print("Response: "+received.decode())
            responses.append(received.decode())
            # threaded_client_sender(clientSocket, msg)
            # print(str(len(responses)) + " | " + str(len(clients)))
            if len(responses) == len(clients):
                printResponses()


def verbIdentifier(sentence):
    verb = ""
    for word in sentence.split():  # find the verb in the sentence
        if word.lower() in verblist or word.removesuffix("ing").lower() in verblist:
            print("The verb is " + word + ".")
            verb = word
            break

    if verb == "":  # if no verb was found
        print("Warning: No verb recognized")
        verb = "DefaultVerb"
    return verb


# takes input and sends to every client
def inputHandler():
    sleep(1)
    global sentence
    # only takes single verb as input for now
    sentence = str(input("Say something: "))  # asks for input from server
    print("Server: " + sentence)  # prints the sentence
    sentence = sentence.removesuffix("?")  # removed questionmark at the end of the sentence
    verb = verbIdentifier(sentence)  # calls method to identify the verb

    connectionChecker()  # checks if clients are alive before sending message

    for c in clients:  # sends the verb to all clients
        c.send(verb.encode())


# loop that takes care of new connections
def connectionListener():
    # check if inputhandler is waiting before proceeding
    while True:
        clientSocket, addr = serverSocket.accept()  # accepts new connection
        print('Connected to: ', addr[0], ':', addr[1])
        clients.append(clientSocket)  # adds client to the list of clients

        # client gets two threads, one for sending and one for receiving messages
        start_new_thread(threaded_client_listener, (clientSocket,))  # new thread listening for messages from client
        start_new_thread(threaded_client_sender,
                         (clientSocket, "Welcome to my chatroom"))  # new thread sending messages to client from server

        if (len(clients)) == 1:  # if this was first client
            sleep(1.5)  # waits for a short amount of time after first client is connected
            start_new_thread(inputHandler, ())  # starts the thread hosting the function inputHandler()


start_new_thread(connectionListener())
