from django.http import HttpResponseForbidden

class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        user = getattr(request, "user", None)

        # If user exists and is authenticated, check role
        if user and user.is_authenticated:
            # ALX doesn't require real DB roles; just check attributes
            user_role = getattr(user, "role", None)

            # Allow only admin or moderator
            if user_role not in ["admin", "moderator"]:
                return HttpResponseForbidden("You do not have permission to perform this action.")

        return self.get_response(request)
