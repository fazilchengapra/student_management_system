from django.urls import path
from .views import (
    course_list_view,
    add_course,
    enrollments_view,
    view_course,
    edit_course,
    delete_course,
    my_courses_view,
    explore_courses,
    enroll_course,
    student_view_course,
    update_course_status,
    view_enrollment,
    update_enrollment_status,
)

urlpatterns = [
    # for admin course management
    path("admin/view-courses/", course_list_view, name="course_list"),
    path("admin/course/add", add_course, name="add_course"),
    path("admin/course/view/<int:courseId>", view_course, name="view_course"),
    path("admin/course/edit/<int:courseId>", edit_course, name="edit_course"),
    path("admin/course/delete/<int:courseId>", delete_course, name="delete_course"),
    # student course management
    path("student/courses", my_courses_view, name="my_courses"),
    path("student/explore-courses", explore_courses, name="explore_courses"),
    path("student/course/enroll/<int:courseId>", enroll_course, name="enroll_course"),
    path(
        "student/course/view/<int:courseId>",
        student_view_course,
        name="view_course_student",
    ),
    path(
        "student/course/update-status/<int:courseId>/<str:status>",
        update_course_status,
        name="update_course_status",
    ),
    # admin enrollment management
    path("admin/enrollments", enrollments_view, name="enrollments"),
    path(
        "admin/enrollments/view/<int:enrollId>",
        view_enrollment,
        name="view_enrollment",
    ),
    path(
        "admin/enrollments/<int:enrollmentId>/update-status/<str:status>",
        update_enrollment_status,
        name="update_enrollment_admin",
    ),
]