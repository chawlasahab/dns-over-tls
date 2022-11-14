#!/usr/bin/env python3

import socket
import ssl
import logging
import _thread
import argparse

DOT_IP = ''
LOGGER = None

def createSSLSocket(data):
    # creating a tcp socket using AF_INET address family (IPv4) of type SOCK_STREAM, a stream oriented socket used by TCP
    tcpSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # creating ssl wrapped tcp socket with TLS protocol version 1.2
    sslSocket = ssl.wrap_socket(tcpSock, ssl_version=ssl.PROTOCOL_TLSv1_2)
    # connect to the socket at address: DOT_IP and port: 853
    sslSocket.connect((DOT_IP, 853))
    sslSocket.send(data)
    response = sslSocket.recv(1024)
    return response

def handler(data, connection):
    response = createSSLSocket(data)
    if response:
        connection.send(response)
        connection.close()
    else:
        LOGGER.error("DNS over TLS lookup failed")

def createTcpSocket(ip, port):
    try:
        # creating a tcp socket using AF_INET address family (IPv4) of type SOCK_STREAM, a stream oriented socket used by TCP
        tcpSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # binding the socket to address: ip at port: port
        tcpSocket.bind((ip, port))
        # enabling socket to accept connections
        tcpSocket.listen()

        while True:
            # returning a new socket object to send/receive data on the connection
            connection = tcpSocket.accept()[0]
            # receving data from socket in bytes with buffersize as 1024
            data = connection.recv(1024)
            # Use of threading to allow multiple requests at same time
            _thread.start_new_thread(handler, (data, connection))
    except socket.error as e:
        LOGGER.error(str(e))
        tcpSocket.close()

def createLogger():
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)
    return logger

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="DNS over TLS")
    parser.add_argument('--listenerip', type=str, default='0.0.0.0', help='Listener IP address')
    parser.add_argument('--listenerport', type=int, default=53, help='Listener port')
    parser.add_argument('--dotip', type=str, default='1.1.1.1', help='IP address for DNS over TLS lookup')
    args = parser.parse_args()
    DOT_IP = args.dotip
    LOGGER = createLogger()
    createTcpSocket(args.listenerip, args.listenerport)