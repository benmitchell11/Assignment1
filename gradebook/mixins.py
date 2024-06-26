from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseForbidden
from django.shortcuts import redirect


class AdminRequiredMixin(UserPassesTestMixin):
    login_url = 'admin_login'

    def test_func(self):
        user = self.request.user if hasattr(self, 'request') else None
        return user and user.is_authenticated and user.is_superuser

    def handle_no_permission(self):
        user = self.request.user if hasattr(self, 'request') else None
        if not user or not user.is_authenticated:
            return redirect(self.login_url)
        else:
            return HttpResponseForbidden("You do not have permission to view this page.")


class LecturerRequiredMixin(UserPassesTestMixin):
    login_url = 'lecturer_login'

    def test_func(self):
        user = self.request.user if hasattr(self, 'request') else None
        return (
                user and user.is_authenticated and hasattr(user, 'lecturer') and user.lecturer
        )

    def handle_no_permission(self):
        user = self.request.user if hasattr(self, 'request') else None
        if not user or not user.is_authenticated:
            return redirect(self.login_url)
        else:
            return HttpResponseForbidden("You do not have permission to view this page.")


from django.contrib.auth.mixins import UserPassesTestMixin
from django.http import HttpResponseForbidden
from django.shortcuts import redirect


class StudentRequiredMixin(UserPassesTestMixin):
    login_url = 'student_login'

    def test_func(self):
        user = self.request.user if hasattr(self, 'request') else None
        return (
                user and user.is_authenticated and hasattr(user, 'student') and user.student
        )

    def handle_no_permission(self):
        user = self.request.user if hasattr(self, 'request') else None
        if not user or not user.is_authenticated:
            return redirect(self.login_url)
        else:
            return HttpResponseForbidden("You do not have permission to view this page.")
