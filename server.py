import socket
import tqdm
import os

# Source code I inspired by:
# https://www.thepythoncode.com/article/send-receive-files-using-sockets-python

# Specify the server parameters
SERVER_HOST = ""
SERVER_PORT = 8800
BUFFER_SIZE = 1024

# Introduce the separator string to identify the filename
SEPARATOR = "<SEPARATOR>"

# Create socket
s = socket.socket()

# Bind socket to IP and port number
s.bind((SERVER_HOST, SERVER_PORT))

s.listen()
print(f"[*] Listening as {SERVER_HOST}:{SERVER_PORT}")

# Accept connection
client_socket, address = s.accept() 
print(f"[+] {address} is connected.")

# Get file information
received = client_socket.recv(BUFFER_SIZE).decode()
filename, filesize = received.split(SEPARATOR)
filename = os.path.basename(filename)
filesize = int(filesize)

# Start receiving the file
progress = tqdm.tqdm(range(filesize), f"Receiving {filename}", unit="B", unit_scale=True, unit_divisor=1024)

# Making the copy of file if needed
counter = 1
if os.path.exists(filename):
    # Get file head and extension
    file_head = filename[:filename.find(".")]
    file_ext = filename[filename.find("."):]
	while os.path.exists(f"{file_head}_copy{counter}{file_ext}"):
		counter += 1
	filename = f"{file_head}_copy{counter}{file_ext}"

# Write the file content
with open(filename, "wb") as f:
    for _ in progress:
        # Recieve 1024 bytes from the client
        bytes_read = client_socket.recv(BUFFER_SIZE)
        if not bytes_read:
            # There is no more data to recieve -> end the loop
            break

        f.write(bytes_read)
        # Update the proggress bar
        progress.update(len(bytes_read))

# Close the client socket
client_socket.close()
# Close the server socket
s.close()