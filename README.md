# What is CHIA monitor:

One server monitor all clients's CPU usage, disk freespace.
Later, we can monitor SSD I/O times.

# Prepare:

1. you need python 3.6+
2. your can connect to the internet or instll package "psutil" in advance.

    `< pip install psutil >`

# Usage:
## Server
1. Download this repo to your server
2. Run server.py

## Client
1. Download this repo to your client
2. Run client.py

# Server Interface :

 Hostname  | CPU%  | C | D | M | Z |
 ---- | ----- | ------  
 A1  | 55 | 50 | 1000 | 888 | 20 
 A2  | 20 | 80 | 1555 | 123 | 1000  
 
 > disk freespace unit is GB

# Contact:

Any problem you can contact edwardliqi@163.com
