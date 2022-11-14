# DNS-over-TLS Proxy

## Description
This project creates a DNS to DNS-over-TLS proxy which accepts both TCP and UDP traffic. The idea is to enable our application to query a DNS-over-TLS server, to make this happen, I have made use of python's [socket](https://docs.python.org/3/library/socket.html) library. Using this library I have created TCP and UDP sockets, binded them with local port 53 to listen on local IP address 0.0.0.0. Next I created handlers to handle multiple incoming TCP/UDP requests, I have used python's [_thread](https://docs.python.org/3/library/_thread.html) library to support multiple requests. Next I used python's [ssl](https://docs.python.org/3/library/ssl.html) library to create ssl wrapped TCP sockets using TLS 1.2 protocol and finally queried Cloudflare's DNS server (1.1.1.1).


## Prerequisites:
* Make sure docker is running before you execute the application


## Execution:
Execute the below command to start the application container

`make run`

You can verify if the application container is running using:

`make verify`

You should be able to see your running container listening on ports 53/tcp and 53/udp.


## Testing
Execute the following commands from your host machine to test the application.
* `dig google.com @172.17.0.2 +tcp`     # to test TCP
* `dig google.com @172.17.0.2`          # to test UDP

Here `172.17.0.2` is my application container's IP, this could change for your machine.

You can also login to the application container using the following command:

`make login`

Once inside, you can run `tcpdump -ni docker0` to see the incoming requests, their acknowledgement, incoming to DNS-over-TLS server, and finally the response back to the requesting body.

## Cleanup
Execute the below command to stop the application container

`make clean`
