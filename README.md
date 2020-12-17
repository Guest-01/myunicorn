# myunicorn (마이+유니콘 = 뮤니콘)
custom-made web server with WSGI built-in   
소켓부터 시작하는 웹서버 + WSGI 구현하기
## socket_direct.py
8000번 포트에서 HTTP를 해석하고 응답하는 단순한 웹서버이다.   
기초적인 소켓 프로그래밍.
## socket_wsgi.py
`socket_direct.py`를 기반으로 wsgi-compatible하게 만든 웹서버이다.   
[PEP-333](https://www.python.org/dev/peps/pep-0333/)에 의거하여 HTTP를 환경변수 형태로 파싱하고 `application` 함수에 넘겨주어 응답한다.   
*(여기 예제에선 실제로 환경변수로 저장하진 않고 해당 모양의 딕셔너리로 직접 `application` 함수에 전달)*
```python
def to_environ(method, path, protocol, headers, body):
    """format http into env, as specified in PEP-333"""
    return {
        'REQUEST_METHOD': method,
        'PATH_INFO': path,
        'SERVER_PROTOCOL': protocol,
        'wsgi.input': StringIO(body),
        **format_headers(headers),  # needs HTTP_ prefix on headers, PEP-333
    }
```
이때 PEP-333에 의하면 HTTP헤더는 `HTTP_`라는 prefix를 붙여야한다.
```python
def format_headers(headers):
    """prefix headers with 'HTTP_'"""
    return {
        f'HTTP_{k}': v for k, v in headers.items()
    }
```
이렇게 파싱된 HTTP는 여러가지 웹프레임워크에서 `application` 함수에 전달된다.
```python
def application(start_response, environ):
    response = view(environ)
    headers = [('Content-Length', len(response))]
    start_response('200 OK', headers)
    return [response]
```
예를 들어, Flask의 경우 처음에 정의하는 `app = Flask(__name__)`이 바로 이 `application`이다.
- - -
**느낀점:**   
파이썬의 훌륭한 추상화 덕분에 가끔은 실제로 어떻게 데이터들이 오고가는지 궁금할 때가 있다.   
그럴땐 이렇게 직접 밑바닥부터 공식문서(PEP)를 통해 구현해보면 재밌다!   
끝.
