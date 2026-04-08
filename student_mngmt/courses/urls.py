from django.urls import path
from .views import course_list_view

urlpatterns = [
    # for admin routes
    path("admin/view-courses/", course_list_view, name='course_list'),
    # path("admin/course/add"),
    # path("admin/course/edit/<int:courseId>"),
    # path("admin/course/delete/<int:courseId>"),
    
    # path('student/courses'),
    # path('student/course/enroll/<int:courseId>'),
    # path('student/course/update-status/<int:courseId>'),
]
