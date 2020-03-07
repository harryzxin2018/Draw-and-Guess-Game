import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('localhost', 50003))
# if use s.bind(s.gethostname(), 50002) , server would be visiable to outside world
# if use s.bind('localhost, 50002), server is only visiable within the same machine """
# if address already in use: ps -fA | grep python or sudo lsof -i:8080

s.listen(1)
# queue up as many as 5 connection requestion.

(conn, addr) = s.accept()
# create a new socket "conn", and also return the client address
# only serving one incoming connection
idle = 0
while 1:
    print('Got connection from', addr)
    data = conn.recv(1024)
    # reads data from the socket in batches of 1024 bytes.
    print(data)
    conn.send(b'got you!')
    conn.send(data)
    if data.decode('UTF-8') == 'exit':
        conn.send(b'bye ~ ~')
        break # close the connection
