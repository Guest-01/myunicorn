import socket


def parse_http(http):
    request, *headers, _, body = http.split('\r\n')
    method, path, protocol = request.split(' ')
    headers = dict(
        line.split(':', maxsplit=1) for line in headers
    )
    return method, path, protocol, headers, body

def process_response(response):
    return (
        'HTTP/1.1 200 OK\r\n' +
        f'Content-Length: {len(response)}\r\n' +
        'Content-Type: text/html\r\n' +
        '\r\n' +
        response +
        '\r\n'
    )

if __name__ == "__main__":
    with socket.socket() as s:
        s.bind(('localhost', 8000))
        s.listen(1)
        conn, addr = s.accept()
        with conn:
            http_request = conn.recv(1024).decode('utf-8')
            request = parse_http(http_request)
            http_response = process_response('Hello World!')
            conn.sendall(http_response.encode('utf-8'))