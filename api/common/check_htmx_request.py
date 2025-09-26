from flask import request

def is_htmx_request():
    return 'text/html' in request.headers.get('Accepts', '') or \
            request.headers.get('HX-Request') == 'true'
