import socket
import sys
import random

# args to be used when creating an instance of the client
ip = sys.argv[1]
port = int(sys.argv[2])
bot = sys.argv[3]

# bot named john
def john(word):
    print("Test (J). Word is "+word)
    # lists of preferred and disliked actions
    preferred_actions = ["coding", "running", "gaming", "football", "partying"]
    bad_actions = ["homework", "driving", "reading", "acting", "drawing"]

    # lists of responses for each category of actions
    preferred_actions_responselist = ["I enjoy " + word, "I'd love to do some " + word, word + "? Sounds awesome!"]

    neutral_responselist = ["We can do some "+word+", but "+preferred_actions[random.randint(0, len(preferred_actions)-1)] + " sounds better"]

    bad_actions_responselist = ["i don't like " + word, "I'd rather do something else",
                                "I don't want to do any " + word + ". I would love to do some " + preferred_actions[
                                    random.randint(0, len(preferred_actions)-1)] + "."]

    if word in preferred_actions:
        return "John: " + preferred_actions_responselist[random.randint(0, len(preferred_actions_responselist)-1)]+"\n"
    elif word in bad_actions:
        return "John: " + bad_actions_responselist[random.randint(0, len(bad_actions_responselist)-1)]+"\n"
    else:
        return "John: "+neutral_responselist[random.randint(0, len(neutral_responselist)-1)]+"\n"

# bot named alexandra
def alexandra(action):
    print("Test (A). Value is "+action)

    # a list of possible responses
    actions = ["I'm down. See you in 30 minutes?",
               "I was just about to suggest that.",
               "I don't mind, but i'd rather do something else...",
               "I don't think "+action+" is something for me.",
               "I don't have time today, sorry. I'll be there for some "+action+" tomorrow!"]

    # returns a randomly selected string from the list above
    randomNumber = random.randint(0, len(actions)-1)
    return "Alexandra: "+actions[randomNumber]+"\n"


# bot named oscar
def oscar(action):
    return "Oscar: "+action+" sounds great!\n"


# bot named nathan. Makes a respons from command-line input
def nathan(action):

    response = input("Provide a response: ")
    return "Nathan: "+response+"\n"


def client(ip, port, bot):
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((ip, port))

    while True:
        # receives and prints message 1
        msg = clientSocket.recv(1024)  # msg 1
        wordlist = msg.decode().split()
        if wordlist[0] == "Server:":
            print(msg.decode())
        elif msg.decode() == "Welcome to my chatroom":
            print("Someone has appeared. Godrick?")
        # elif wordlist[0].startswith('ping'):
        #    print("pinged by server")
        else:
            print(msg)
            response = eval(bot + "(msg.decode())")
            print(response)
            clientSocket.send(response.encode())


# calls method
client(ip, port, bot)
