from django.shortcuts import redirect

class RedirectAdminMiddleware:
    
    ADMIN_PREFIXES = ("/admin", "/admin/")

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path
        # اسمح بخروج/تغيير كلمة المرور لأن روابطها تحت /admin
        allowed = ("/admin/logout/", "/admin/password_change/")
        if (path == "/admin" or path.startswith("/admin/")) and path not in allowed:
            return redirect("custom_admin:dashboard")
        return self.get_response(request)
