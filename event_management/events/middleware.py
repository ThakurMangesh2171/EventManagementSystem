from django.http import JsonResponse
from .customException import EventExistsError, EventNotFoundException

class CustomExceptionHandlerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_exception(self, request, exception):
        if isinstance(exception, (EventExistsError, EventNotFoundException)):
            return JsonResponse({'error': str(exception)}, status=400)
        return None
