#!/usr/bin/python
# -*- coding: utf-8 -*-
 
# The modules required
import sys
import socket
import struct

'''
This program communicates with the haapa7.oulu.fi server,
first with TCP and then with UDP.

The TCP part takes the users arguments, creates a datastream-type socket
and proceeds to send the users encoded handshake message to the server.
The received CID and UDP port is then forwarded to the UDP
method.

The UDP part creates a datagram-type socket and sends a hello message
to the server. The message is encoded and packed into a struct with
additional info.
The server then sends a random number message with random words,
which the program reverses and sends back. After all this back-and-forth,
the server finally sends a message telling the exchange is finished,
and the program stops.
''' 
 
def send_and_receive_tcp(address, port, message):
    print("You gave arguments: {} {} {}".format(address, port, message))
    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_sock.connect((address, port))
    tcp_sock.send(message.encode())
    rcv_message = tcp_sock.recv(1024)
    #print(rcv_message.decode())
    tcp_sock.close()
    _, CID, UDP = rcv_message.split()
    send_and_receive_udp(address, CID, UDP)
    return
 
 
def send_and_receive_udp(address, CID, UDP):
    ACK = True
    END = False

    full_address = (address, int(UDP))
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    message = "Hello from {}".format(CID)
    data = struct.pack('!8s??HH128s', CID, ACK, END, 0, len(message), message.encode())
    udp_sock.sendto(data, (full_address))
    while(END == False):
        data, _ = udp_sock.recvfrom(1024)
        _,_,END,_,length,message = struct.unpack('!8s??HH128s', data)
        message = message.decode()[0:length]
        if(END):
            print(message)
        else:
            words = message.split(' ')
            #print("Ennen", words, "\n")
            words.reverse()
            message = " ".join(words)
            #print("Jalkeen", message, "\n")
            data = struct.pack('!8s??HH128s', CID, ACK, END, 0, len(message), message.encode())
            udp_sock.sendto(data, (full_address))
    udp_sock.close()
    return
 
 
def main():
    USAGE = 'usage: %s <server address> <server port> <message>' % sys.argv[0]
 
    try:
        # Get the server address, port and message from command line arguments
        server_address = str(sys.argv[1])
        server_tcpport = int(sys.argv[2])
        message = str(sys.argv[3])
    except IndexError:
        print("Index Error")
    except ValueError:
        print("Value Error")
    # Print usage instructions and exit if we didn't get proper arguments
        sys.exit(USAGE)
 
    send_and_receive_tcp(server_address, server_tcpport, message)
 
 
if __name__ == '__main__':
    # Call the main function when this script is executed
    main()
