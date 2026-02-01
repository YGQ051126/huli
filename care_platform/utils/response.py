from rest_framework.response import Response

class APIResponse(Response):
    """Custom API response format"""
    def __init__(self, code=200, message='Success', data=None, status=None, headers=None, **kwargs):
        response_data = {
            'code': code,
            'message': message,
            'data': data or {}
        }
        response_data.update(kwargs)
        super().__init__(response_data, status, headers)

class ErrorResponse(APIResponse):
    """Custom error response format"""
    def __init__(self, code=400, message='Request Failed', errors=None, **kwargs):
        super().__init__(code=code, message=message, data=errors, **kwargs)

# Common response functions
def success_response(data=None, code=200, message='Success', **kwargs):
    return APIResponse(code=code, message=message, data=data, **kwargs)

def error_response(code=400, message='Request Failed', errors=None, **kwargs):
    return ErrorResponse(code=code, message=message, errors=errors, **kwargs)

# Status code constants
HTTP_200_OK = 200
HTTP_201_CREATED = 201
HTTP_400_BAD_REQUEST = 400
HTTP_401_UNAUTHORIZED = 401
HTTP_403_FORBIDDEN = 403
HTTP_404_NOT_FOUND = 404
HTTP_500_INTERNAL_SERVER_ERROR = 500
