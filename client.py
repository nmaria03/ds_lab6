import socket
import tqdm
import os
import sys

# Source code I inspired by:
# https://www.thepythoncode.com/article/send-receive-files-using-sockets-python

# Create the separator sting to make server know the filename
SEPARATOR = "<SEPARATOR>"
BUFFER_SIZE = 1024

# Get filename, ip and port number
filename = sys.argv[1]
host = sys.argv[2]
port = int(sys.argv[3])

# Get the file size
filesize = os.path.getsize(filename)
# Create the socket
s = socket.socket()

# Create socket connection
s.connect((host, port))

# Send the filename followed by separator and filesize
s.send(f"{filename}{SEPARATOR}{filesize}".encode())

# Send the file data
progress = tqdm.tqdm(range(filesize), f"Sending {filename}", unit="B", unit_scale=True, unit_divisor=1024)
with open(filename, "rb") as f:
    for _ in progress:
        bytes_read = f.read(BUFFER_SIZE)

        if not bytes_read:
            # There is no more data to send -> end the loop
            break

        # Send the portion of data to the server
        s.send(bytes_read)
        # Update the proggress bar
        progress.update(len(bytes_read))

print(f"File {filename} successfully sent!")

# Close the socket to end the connection
s.close()