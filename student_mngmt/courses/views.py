from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

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

    if req.method == "POST":
        form = CourseEditForm(req.POST, req.FILES, instance=course)

        if form.is_valid():
            form.save()
            return redirect("course_list")

    form = CourseEditForm(instance=course)

    context = {"course": course, "form": form}
    return render(req, "admin/course/edit_course.html", context)


# course deletion -> only admins can do this
@login_required  # it's a function that check session id is have the requester
def delete_course(req, courseId):
    if not req.user.is_staff:
        return redirect("login")

    if req.method == "POST":
        course = get_object_or_404(Course, id=courseId)
        course.delete()
        messages.success(req, "course deleted success!")
        return redirect("course_list")
    messages.error(req, "something went wrong!")
    return redirect("view_course", courseId)


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


# admin view specific enrollment
@login_required
def view_enrollment(req, enrollId):
    if not req.user.is_staff:
        return redirect("login")

    enrollment = get_object_or_404(Enrollment, id=enrollId)
    print(enrollment)
    context = {"enrollment": enrollment}

    return render(req, "admin/enrollments/view_enrollment.html", context)


@login_required
def update_enrollment_status(req, enrollmentId, status):
    print("called")
    if not req.user.is_staff:
        return redirect("login")

    enrollment = get_object_or_404(Enrollment, id=enrollmentId)
    validStatuses = [
        choice[0]
        for choice in Enrollment.STATUS_CHOICES
        if choice[0] not in ["in_progress", "pending", "Completed"]
    ]

    if status in validStatuses:
        enrollment.status = status
        enrollment.save()
        messages.success(req, "Enrollment status updated!")
    else:
        messages.success(req, "Something went wrong!")

    return redirect("view_enrollment", enrollmentId)


# student course view -> (student my courses section)
@login_required
def my_courses_view(req):
    if req.user.is_staff:
        return redirect("admin")

    enrollments = Enrollment.objects.filter(student=req.user)

    status_filter = req.GET.get("status")

    if status_filter:
        enrollments = enrollments.filter(status=status_filter)

    all_enrollments = Enrollment.objects.filter(student=req.user)

    total = all_enrollments.count()
    in_progress = enrollments.filter(status=Enrollment.IN_PROGRESS).count
    completed = enrollments.filter(status=Enrollment.COMPLETED).count
    pending = enrollments.filter(status=Enrollment.PENDING).count()

    context = {
        "enrollments": enrollments,
        "total": total,
        "in_progress_count": in_progress,
        "completed_count": completed,
        "pending_count": pending,
    }

    return render(req, "student/course/my_courses.html", context)


@login_required
def explore_courses(req):
    if req.user.is_staff:
        return redirect("admin")

    enrolled_ids = Enrollment.objects.filter(student=req.user).values_list(
        "course", flat=True
    )
    available_courses = Course.objects.exclude(id__in=enrolled_ids)

    context = {"available_courses": available_courses}

    return render(req, "student/course/explore_courses.html", context)


@login_required
def enroll_course(req, courseId):
    if req.user.is_staff:
        return redirect("admin")

    if req.method == "POST":
        course = get_object_or_404(Course, id=courseId)
        student = req.user

        is_already_enrolled = Enrollment.objects.filter(
            student=student, course=course
        ).exists()

        if is_already_enrolled:
            messages.warning(req, f"the {course.title} is already enrolled!")

        else:
            Enrollment.objects.create(student=student, course=course)
            messages.success(req, "Enrollment request sent to admin!")

    return redirect("my_courses")


@login_required
def student_view_course(req, courseId):
    if req.user.is_staff:
        return redirect("admin")
    student = req.user
    course = get_object_or_404(Course, id=courseId)
    enrollment = get_object_or_404(Enrollment, student=student, course=course)

    context = {"course": course, "enrollment": enrollment}

    return render(req, "student/course/view_course.html", context)


@login_required
def update_course_status(req, courseId, status):
    if req.user.is_staff:
        return redirect("admin")

    if req.method == "POST":
        student = req.user
        enrollment = get_object_or_404(Enrollment, student=student, course=courseId)

        validStatuses = [
            choice[0]
            for choice in Enrollment.STATUS_CHOICES
            if choice[0] not in ["enrolled", "pending", "rejected"]
        ]
        if status not in validStatuses:
            messages.error(req, "Something went wrong.")

        enrollment.status = status
        enrollment.save()
        messages.success(req, "Status updated success!")

    return redirect("view_course_student", courseId)
