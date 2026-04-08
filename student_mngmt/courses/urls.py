from django.urls import path
from .views import (
    course_list_view,
    add_course,
    enrollments_view,
    view_course,
    edit_course,
    delete_course
)

urlpatterns = [
    # for admin course management
    path("admin/view-courses/", course_list_view, name="course_list"),
    path("admin/course/add", add_course, name="add_course"),
    path("admin/course/view/<int:courseId>", view_course, name="view_course"),
    path("admin/course/edit/<int:courseId>", edit_course, name="edit_course"),
    path("admin/course/delete/<int:courseId>", delete_course, name='delete_course'),
    # student course management
    # path('student/courses'),
    # path('student/course/enroll/<int:courseId>'),
    # path('student/course/update-status/<int:courseId>'),
    # admin enrollment management
    path("admin/enrollments", enrollments_view, name="enrollments"),
]
