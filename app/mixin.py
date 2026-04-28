from django.contrib.auth.mixins import AccessMixin
from django.shortcuts import redirect


class StudentMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_student and request.user.is_authenticated:
            return self.handle_no_permission()

        if not request.user.is_active:
            pass

        return super().dispatch(request, *args, **kwargs)


class TeacherMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if (
            not request.user.is_teacher
            and request.user.is_staff
            and request.user.is_authenticated
        ):
            return self.handle_no_permission()

        if not request.user.is_active:
            pass

        return super().dispatch(request, *args, **kwargs)


class AdminMixin(AccessMixin):
    def dispatch(self, request, *args, **kwargs):
        if (
            not request.user.is_superuser
            and request.user.is_staff
            and request.user.is_authenticated
        ):
            return self.handle_no_permission()

        if not request.user.is_active:
            pass

        return super().dispatch(request, *args, **kwargs)
