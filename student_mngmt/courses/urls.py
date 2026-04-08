from django.urls import path
from .views import course_list_view, add_course, enrollments_view, view_course

urlpatterns = [
    # for admin course management
    path("admin/view-courses/", course_list_view, name='course_list'),
    path("admin/course/add", add_course, name='add_course'),
    path('admin/course/view/<int:courseId>', view_course, name='view_course'),
    # path("admin/course/edit/<int:courseId>"),
    # path("admin/course/delete/<int:courseId>"),
    
    # student course management
    # path('student/courses'),
    # path('student/course/enroll/<int:courseId>'),
    # path('student/course/update-status/<int:courseId>'),
    
    # admin enrollment management
    path('admin/enrollments', enrollments_view, name='enrollments')
]
