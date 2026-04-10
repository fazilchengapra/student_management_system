from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    home_view,
    login_view,
    register_view,
    logout_view,
    my_profile,
    admin_students_view,
    view_student,
    edit_student,
    toggle_student_status,
    delete_student,
    add_new_student,
)

urlpatterns = [
    path("", home_view, name="landing"),
    path("login/", login_view, name="login"),
    path("register", register_view, name="register"),
    path("logout", logout_view, name="logout"),
    path("student/profile", my_profile, name="my_profile"),
    path("admin/students", admin_students_view, name="student_mgmt"),
    path("admin/student/add-student/", add_new_student, name="add_new_student"),
    path("admin/student/<int:stdId>", view_student, name="view_student"),
    path("admin/student/<int:stdId>/edit", edit_student, name="edit_student_admin"),
    path(
        "admin/student/toggle-user/<int:stdId>",
        toggle_student_status,
        name="toggle_student",
    ),
    path(
        "admin/student/delete-user/<int:stdId>", delete_student, name="delete_student"
    ),
    path(
        "forgot-password/",
        auth_views.PasswordResetView.as_view(),
        name="password_reset",
    ),
    path(
        "forgot-password/done/",
        auth_views.PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
]
