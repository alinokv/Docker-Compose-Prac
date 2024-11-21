from django.utils.datetime_safe import datetime


class LogErrorsMiddleware(object):
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            response = self.get_response(request)
        except Exception as e:
            self.log_error(request, e)
            raise

        return response

    def log_error(self, request, exception):
        # Log the error to a file
        with open('logs.log', 'a') as f:
            f.write(f"{datetime.now()} - {request.method} {request.path} {exception}\n")
        print(f"{datetime.now()} - {request.method} {request.path} {exception}")
