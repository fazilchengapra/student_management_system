from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .forms import CourseForm, CourseEditForm
from .models import Course, Enrollment

# Create your views here.


@login_required
def course_list_view(req):
    if not req.user.is_staff:
        return redirect("login")

    courses = Course.objects.all()
    total_enrollments = Enrollment.objects.count()

    return render(
        req,
        "admin/course/course_list.html",
        {
            "courses": courses,
            "total_courses": len(courses),
            "total_enrollments": total_enrollments,
        },
    )


@login_required
def add_course(req):
    if not req.user.is_staff:
        return redirect("login")

    if req.method == "POST":
        form = CourseForm(req.POST, req.FILES)
        if form.is_valid():
            form.save()
            return redirect("course_list")
        return redirect("add_course")
    form = CourseForm()

    return render(req, "admin/course/add_course.html", {"form": form})


@login_required
def view_course(req, courseId):
    if not req.user.is_staff:
        return redirect("login")

    course = Course.objects.get(id=courseId)
    return render(req, "admin/course/course_view.html", {"course": course})

# edit course details, only can edit admins
@login_required
def edit_course(req, courseId):
    if not req.user.is_staff:
        return redirect("login")
    
    course = get_object_or_404(Course, id=courseId)
    
    if req.method == 'POST':
        form = CourseEditForm(req.POST, req.FILES, instance=course)
        
        if form.is_valid():
            form.save()
            return redirect('course_list')
    
    form = CourseEditForm(instance=course)
    
    context = {
        'course':course,
        'form':form
    }
    return render(req, "admin/course/edit_course.html", context)

# admin view
@login_required
def enrollments_view(req):
    if not req.user.is_staff:
        return redirect("login")

    enrollments = Enrollment.objects.all()
    approved = enrollments.filter(status="enrolled").count()
    pending = enrollments.filter(status="pending").count()
    total = enrollments.count()

    return render(
        req,
        "admin/enrollments/enrollments.html",
        {
            "enrollments": enrollments,
            "approved_count": approved,
            "pending_count": pending,
            "total_enrollments": total,
        },
    )
