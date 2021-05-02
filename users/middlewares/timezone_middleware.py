from django.utils import timezone


class TimezoneMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        if hasattr(request.user, 'timezone'):
            user_timezone = request.user.timezone

            if user_timezone:
                timezone.activate(user_timezone)
            else:
                timezone.deactivate()

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
