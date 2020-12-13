import socket
from io import StringIO


def parse_http(http):
    request, *headers, _, body = http.split('\r\n')
    method, path, protocol = request.split(' ')
    headers = dict(
        line.split(':', maxsplit=1) for line in headers
    )
    return method, path, protocol, headers, body

# def process_response(response):
#     return (
#         'HTTP/1.1 200 OK\r\n' +
#         f'Content-Length: {len(response)}\r\n' +
#         'Content-Type: text/html\r\n' +
#         '\r\n' +
#         response +
#         '\r\n'
#     )

def format_headers(headers):
    """prefix headers with 'HTTP_'"""
    return {
        f'HTTP_{k}': v for k, v in headers.items()
    }

def to_environ(method, path, protocol, headers, body):
    """format http into env, as specified in PEP-333"""
    return {
        'REQUEST_METHOD': method,
        'PATH_INFO': path,
        'SERVER_PROTOCOL': protocol,
        'wsgi.input': StringIO(body),
        **format_headers(headers),  # needs HTTP_ prefix on headers, PEP-333
    }

def start_response(status, headers):
    conn.sendall(f'HTTP/1.1 {status}\r\n'.encode())  # closure
    for key, value in headers:
        conn.sendall(f'{key}: {value}\r\n'.encode())
    conn.sendall('\r\n'.encode())

def application(start_response, environ):
    response = view(environ)
    headers = [('Content-Length', len(response))]
    start_response('200 OK', headers)
    return [response]

# typical view function in web-framework
def view(environ):
    path = environ['PATH_INFO']
    return f'Hello from {path}'

if __name__ == "__main__":
    with socket.socket() as s:
        s.bind(('localhost', 8000))
        s.listen(1)
        print('listening on port 8000...')
        conn, addr = s.accept()
        print(f'from client: {addr}')
        with conn:
            http_request = conn.recv(1024).decode('utf-8')
            request = parse_http(http_request)
            print(f'{request=}')
            environ = to_environ(*request)
            print(f'{environ=}')
            response = application(start_response, environ)
            print(f'{response=}')
            for data in response:
                conn.sendall(data.encode('utf-8'))