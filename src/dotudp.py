#!/usr/bin/env python3

import socket
import logging
import ssl
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
    # converting udp data to tcp by adding 2 byte integer before sending it over tcp
    toTcpData = b"\x00" + bytes(chr(len(data)), encoding='utf-8') + data
    sslSocket.send(toTcpData)
    response = sslSocket.recv(1024)
    return response

def handler(data, address, socket):
    response = createSSLSocket(data)
    if response:
        udpData = response[2:]
        socket.sendto(udpData, address)
    else:
        LOGGER.error("DNS over TLS lookup failed")


def createUdpSocket(ip, port):
    try:
        # creating a udp socket using AF_INET address family (IPv4) of type SOCK_DGRAM, a datagram oriented socket used by UDP
        udpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # binding the socket to address: ip at port: port
        udpSocket.bind((ip, port))

        while True:
            # receving data from socket in bytes with buffersize as 1024
            data, address = udpSocket.recvfrom(1024)
            # Use of threading to allow multiple requests at same time
            _thread.start_new_thread(handler, (data, address, udpSocket))
    except socket.error as e:
        LOOGER.error(str(e))
        udpSocket.close()

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
    LOOGER = createLogger()
    createUdpSocket(args.listenerip, args.listenerport)
