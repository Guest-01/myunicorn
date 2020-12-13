import socket

with socket.socket() as s:
    s.bind(('localhost', 8000))
    s.listen(1)
    conn, addr = s.accept()

    while True:
        with conn:
            request = conn.recv(1024).decode('utf-8')
            print(request)
            # conn.sendall('Hello World'.encode('utf-8'))
            break