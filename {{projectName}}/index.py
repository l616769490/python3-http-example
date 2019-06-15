import sys
import json

def handler(environ, start_response):

    request_uri = environ['fc.request_uri']

    headers = {}
    for k, v in environ.items():
        if k.startswith("HTTP_"):
            # 请求头
            headers[k] = v
            pass

    # 请求体
    try:
        request_body_size = int(environ.get('CONTENT_LENGTH', 0))
    except (ValueError):
        request_body_size = 0

    request_body = environ['wsgi.input'].read(request_body_size)

    # 请求方式
    request_method = environ['REQUEST_METHOD']

    # 路径信息
    path_info = environ['PATH_INFO']

    # 查询字符串
    try:
        query_string = environ['QUERY_STRING']    
    except (KeyError):
        query_string = ""

    response = {
        'headers': headers,
        'query_string': query_string,
        'method': request_method,
        'request_uri': request_uri,
        'path_info': path_info,
        'body': request_body.decode("utf-8"),
        'content_type': environ.get('CONTENT_TYPE', '')
    }

    sys.stdout.flush()

    status = '200 OK'
    response_headers = [('Content-type', 'application/json')]
    start_response(status, response_headers)

    # 返回数据
    return [json.dumps(response).encode()]