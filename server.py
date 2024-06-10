import socket
from _thread import *  # / allow multiple instance to run at once
from game import Game
import pickle

server = ''  # server IP address
port = 5555  # Destination Port Number

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # / create socket

try:
    s.bind((server, port))  # / bind the socket to this server and port
except socket.error as e:
    str(e)

s.listen()  # / open up the port
print("waiting for a connection, Server started")

connected = set() #store the ip address of the connected client
games = {}
idCount = 0 #keep track of our current id


def threaded_client(conn, p, gameId):  # / run in background
    global idCount
    conn.send(str.encode(str(p))) #know if this is player 0 or player 1

    reply = ""
    while True:
        try:
            data = conn.recv(4096).decode()  # / 4096: amount of bits, decode information received

            if gameId in games: #check if the game still exist
                game = games[gameId]

                if not data:  # / if the client disconnected, the server will stop trying to get the information
                    break
                else:
                    if data == "reset":
                        game.resetWent() #reset the game
                    elif data != "get":
                        game.play(p, data) #this is the move, send the move
                    reply = game
                    conn.sendall(pickle.dumps(reply)) #send back the object
            else:
                break
        except:
            break
    try:
        del games[gameId] #delete the game
        print("closing game", gameId)
    except:
        pass
    idCount -= 1
    conn.close() #close connection


while True:  # / continously see if there is any connection
    conn, addr = s.accept()  # / accept incoming connection, store ip address and object
    print("connected to:", addr)

    idCount += 1 #keep track of how many clients are conneting at once
    p = 0 #current player
    gameId = (idCount - 1) // 2 #keep track of how many games
    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("creating a new game...")
    else:
        games[gameId].ready = True #if 2 players are connected into 1 game
        p = 1 #player = 1
    start_new_thread(threaded_client, (conn, p, gameId))  # / allow multiple connection
