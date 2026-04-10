from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .forms import RegisterForm, UpdateStudentForm, StudentSelfUpdateForm
from .models import User
from courses.models import Course, Enrollment


# Create your views here.
def home_view(req):
    if req.user.is_authenticated:
        if req.user.is_staff:
            return redirect("admin")
        else:
            return redirect("student")
    return render(req, "landing.html")


def login_view(req):
    if req.user.is_authenticated:
        return redirect("landing")
    if req.method == "POST":
        username = req.POST.get("username")
        password = req.POST.get("password")

        user = User.objects.filter(username=username).first()

        if user and not user.is_active:
            messages.error(req, "Your account is blocked please contact admin!")
            return redirect("login")

        user = authenticate(req, username=username, password=password)

        if user is not None:
            login(req, user)

            if user.is_staff:
                return redirect("admin")
            else:
                return redirect("student")
        else:
            messages.error(req, "Username or password is incorrect")

    return render(req, "login.html")


def register_view(req):
    if req.method == "POST":
        form = RegisterForm(req.POST, req.FILES)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.is_staff = False
            user.save()

            messages.success(req, "Account registered successfully!")
            return redirect("login")
    else:
        form = RegisterForm()

    return render(req, "register.html", {"form": form})


@login_required
def logout_view(req):
    logout(req)
    messages.success(req, "Logout successfully!", extra_tags="logout_tag")
    return redirect("login")


@login_required
def admin_base(req):
    if req.user.is_staff:

        students = User.objects.all()
        courses = Course.objects.all()
        enrollments = Enrollment.objects.all()

        tot_students = students.filter(is_staff=False).count()
        tot_courses = courses.count()
        tot_enrollments = enrollments.count()
        pending_req = enrollments.filter(status="pending").count()
        recent_requests = enrollments.filter(status="pending")

        context = {
            "total_students": tot_students,
            "total_courses": tot_courses,
            "total_enrollments": tot_enrollments,
            "pending_requests": pending_req,
            "recent_requests": recent_requests,
        }
        return render(req, "admin/dashboard/dashboard.html", context)
    return redirect("login")


@login_required
def student_base(req):
    if req.user.is_staff:
        return redirect("admin")

    enrollments = Enrollment.objects.filter(student=req.user)

    in_progress_count = enrollments.filter(status="in_progress").count()
    completed_count = enrollments.filter(status="completed").count()
    pending_count = enrollments.filter(status="pending").count()

    active_courses = enrollments.filter(status="in_progress")

    context = {
        "in_progress_count": in_progress_count,
        "completed_count": completed_count,
        "pending_count": pending_count,
        "active_courses": active_courses,
    }

    print(enrollments)
    return render(req, "student/dashboard/dashboard.html", context)

# for individual students only.
@login_required
def my_profile(req):
    if req.user.is_staff:
        return redirect("admin")
    if req.method == "POST":
        form = StudentSelfUpdateForm(req.POST, req.FILES, instance=req.user)

        print(req.POST)
        if form.is_valid():
            form.save()
            messages.success(req, "Profile updated success!")
            return redirect("my_profile")

    return render(req, "student/profile/profile.html")


@login_required
def admin_students_view(req):
    if req.user.is_staff:
        students = User.objects.filter(is_staff=False)
        q = req.GET.get("q", "")

        if q:
            students = students.filter(Q(username__icontains=q) | Q(email__icontains=q))
        return render(req, "admin/students/students.html", {"students": students})
    return redirect("login")


@login_required
def view_student(req, stdId):
    if req.user.is_staff:
        student = get_object_or_404(User, id=stdId, is_staff=False)
        return render(req, "admin/students/view_student.html", {"student": student})
    return redirect("login")


@login_required
def edit_student(req, stdId):
    if not req.user.is_staff:
        return redirect("login")

    student = get_object_or_404(User, id=stdId)
    form = UpdateStudentForm(req.POST or None, req.FILES, instance=student)

    if req.method == "POST":
        print(req.POST)
        if form.is_valid():
            obj = form.save(commit=False)

            print(req.POST.get("is_active"))
            # handle is_active manually
            obj.is_active = req.POST.get("is_active") == "1"

            obj.save()

            messages.success(req, f"user #{obj.id} details updated")

            return redirect("view_student", stdId=student.id)
        else:
            messages.error("User change is not saved!")

    return render(
        req, "admin/students/edit_student.html", {"form": form, "student": student}
    )


@login_required
def toggle_student_status(req, stdId):
    if not req.user.is_staff:
        return redirect("login")

    user = get_object_or_404(User, id=stdId)

    user.is_active = not user.is_active
    user.save()
    messages.success(req, f"user #{user.id} activation status updated!")

    return redirect("view_student", stdId)


@login_required
def delete_student(req, stdId):
    if not req.user.is_staff:
        return redirect("login")

    user = get_object_or_404(User, id=stdId)
    user.delete()

    messages.success(req, f"user {user.id} deleted success!")

    return redirect("student_mgmt")


@login_required
def add_new_student(req):
    if req.user.is_staff:
        if req.method == "POST":
            form = RegisterForm(req.POST, req.FILES)
            if form.is_valid():
                user = form.save(commit=False)
                print(req.POST.get("is_active"))
                user.is_active = req.POST.get("is_active") == "1"
                user.set_password(form.cleaned_data["password"])
                user.save()
                messages.success(req, "user created success")
                return redirect("student_mgmt")

        return render(req, "admin/students/add_student.html")
    return redirect("login")
