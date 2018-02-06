# cloud-ping
Client/server utility to ping a cloud VM instance and determine latency and bandwidth.

# Usage
## Server
Start the server listening for ping requests
> python cloud-ping.py -s -p [listen-port]

## Client
Start client to send pings to server and measure round-trip time
> python cloud-ping.py -c --addr [remote-addr] --port [remote-port]
