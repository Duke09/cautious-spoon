from rest_framework import status
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

def _handle_non_field_errors(error):
    if "non_field_errors" in error:
        return {
            "message": error["non_field_errors"][0]
        }

    return error

def set_response(data=None, error=None, status=status.HTTP_200_OK):
    if error:
        error = _handle_non_field_errors(error)

        if not status:
            status = 400

    if status >= 200 and status < 400:
        code = True
    else:
        code = False

    response = {
        'data': data,
        'success': code,
        'error': error
    }

    return Response(response, status=status)