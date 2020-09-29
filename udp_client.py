# program that models the behavior of the client module when using UDP

import socket
import time



# PROGRAM OPTIONS
# if set to true, this simulates the user pressing the bind button for the client (an unnecessary, but valid thing to do for the client)
# if set to false, the client automatically binds the socket to a port upon sending
USER_PRESSES_BIND_BUTTON = False 


# if set to true, simulates a scenario where the user decided to let the client automatically send data in its send loop.
# if set to False, then the user must press tell the client every time they wish to send data to the server
USER_PRESSES_AUTO_SEND_BUTTON = True

#(only applies if USER_PRESSES_AUTO_SEND_BUTTON = False)
# if set to true, simulates a scenario where the user chooses to type in a message to send to the server
#if set to false, simulates a scenario where the user presses the "send" button to send an automatically generated message
USER_SENDS_CUSTOM_MESSAGE = True






#------------ client socket setup ----------- #

# step 1: create a UDP socket
# IN-GAME: not 100% sure how we should represent socket creation. 
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


# (optional) step 2: bind the socket to the client's ip address and one of it's ports
# client ip address + random port are automatically assigned to the socket later if not bound.
# IN-GAME:  the user can opt in to press a "bind" button and go through bind process. or they can just move on to the next step.
#           after they press "bind," the port on the module's port that they specified should visually open up. if they don't press bind,
#           then no ports open yet. 
if USER_PRESSES_BIND_BUTTON:
    # ask user to enter a port
    client_address = input("please enter the ip address of this module: ")
    client_port = int(input("please enter a port to use on this module: "))

    # bind the socket to the desired port
    sock.bind((client_address, client_port))

# DEBUGGING: prints out the address & port bound to the socket
print("\tsocket address & port before sending data:", sock.getsockname())




# --------- user should now open up a bound socket on the server module, unless they have already bound a socket on the server --------- #
# if the user does not open up a bound socket on the server module, they can send data to a port on the server, but the server won't accept the data. the data will just never make it
# to its final destination (e.g., in game the sent datagram might just fall to the ground after colliding with a closed port)





# -------------- sending data -------------------- #

# step 3: get the server socket's address & port
server_address = input("please enter the server socket's ip address: ")
server_port = int(input("please enter the server socket's port number: "))


# step 4: send data to the server.
# IN-GAME: if the user hasn't bound the client socket to a port, the module will automatically choose a port on the cli1ent's first attempt to "send." that port will visibly open up on the module. 
# option 1: send data automatically. just sending a message with an incrementing number, with a 2-second pause between messages
if USER_PRESSES_AUTO_SEND_BUTTON: 
    count = 1
    while(True):
        # send data
        data_to_send = "message #: " + str(count)
        sock.sendto(data_to_send.encode('utf-8'), (server_address, server_port))
        
        # DEBUGGING: just some useful information about what's happening on the client side
        print("---------------------------------------------------------------")
        print("\tdata sent:", "\'" + data_to_send + "\'")
        print("\tdata sent from:", sock.getsockname())
        print("\tdata sent to:", (server_address, server_port))
        print("---------------------------------------------------------------")

        # update message count and wait before next send
        count += 1
        time.sleep(2)
        
# option 2: send data manually (user must press "send" every time they want to send data to the server)
else:
    count = 1;
    while(True):
        # prepare the data being sent
        # if set to true, simulates a scenario where the user chooses to send a 
        if USER_SENDS_CUSTOM_MESSAGE:
                data_to_send = input("enter a message to send: ")
        else:
            input("press enter to send a packet")
            data_to_send = "message #: " + str(count)
            count += 1
        
        # send the data
        sock.sendto(data_to_send.encode('utf-8'), (server_address, server_port))

        # DEBUGGING: just some useful information about what's happening on the client side
        print("---------------------------------------------------------------")
        print("\tdata sent:", "\'" + data_to_send + "\'")
        print("\tdata sent from:", sock.getsockname())
        print("\tdata sent to:", (server_address, server_port))
        print("---------------------------------------------------------------")
        