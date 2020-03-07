import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(('localhost', 50003)) # need to know server port
# sending one message
print('send: v1')
msg = b'--How are your doing?--'
s.send(msg)

# sending message v2: make sure whole message is sent to server
print('send: v2')
total_sent = 0
while total_sent < len(msg) :
    sent = s.send(msg[total_sent:])
    print(sent)
    if sent==0:
        print('server disconnected')
        break
    total_sent += sent

# receiving messages from server
print('receive one message from server')
data = s.recv(1024)
print ('Received', repr(data))

# user control the connection
print('\n \n \n --chatting--- \n')
while True:
    msg = input('enter your message: ')
    s.send(msg.encode('UTF-8'))
    data = s.recv(1024)
    print ('Received', repr(data))
    if msg == 'exit':
        data = s.recv(1024)
        print ('Received', repr(data))
        break

s.close()
