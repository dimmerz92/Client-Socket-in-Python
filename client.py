### MODULES
import sys
import socket

### FUNCTIONS
def error(msg):
    print(msg)
    sys.exit(1)

### CONSTANTS
MAX_BUFFER = 256

### VARIABLES
buffer = ""

### SERVER INFO
try:
    HOST = socket.gethostbyname(sys.argv[1])
    PORT = int(sys.argv[2])
except IndexError:
    error("ERROR insufficient arguments")
except OSError:
    error("ERROR no such host")

### CREATE SOCKET
try:
    skt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
except OSError:
    error("ERROR creating socket")

### CONNECT TO SERVER
try:
    skt.connect((HOST, PORT))
except OSError:
    skt.close()
    error("ERROR connecting")

### COMMUNICATE WITH SERVER
while(1):
    ## SEND MESSAGE
    # get user input
    buffer = input()

    # handle length and final character
    if len(buffer) > 255:
        buffer = buffer [0:255] + '\n'
    else:
        buffer = buffer + '\n'
    try:
        buffer = buffer.encode("ascii")
    except UnicodeEncodeError:
        skt.close()
        error("ERROR message contains non-ASCII characters")
    
    # send the message
    try:
        skt.send(buffer)
    except OSError:
        skt.close()
        error("ERROR sending message")
    
    ## RECEIVE MESSAGE
    try:
        buffer = skt.recv(256)
        buffer = buffer.decode('ascii')
    except OSError:
        skt.close()
        error("ERROR receiving")
    except UnicodeDecodeError:
        skt.close()
        error("ERROR message contained non-ASCII characters")

    # evaluate response
    if buffer:
        if buffer != "ACK":
            print(buffer)
        if buffer == "DISCONNECT: OK" or buffer == "CONNECT: ERROR":
            skt.close()
            sys.exit(0)
    else:
        skt.close()
        sys.exit(1)