from django.db import models
import accounts.models
from django.conf import settings

# Create your models here.

User = settings.AUTH_USER_MODEL


class Course(models.Model):
    title = models.CharField(max_length=150)

    course_url = models.ImageField(upload_to="course_image/", blank=True, null=True)

    description = models.TextField()

    video_link = models.URLField(null=True, blank=True, help_text="Youtube video link")

    duration = models.CharField(max_length=50)

    created_at = models.DateField(auto_now_add=True)


class Enrollment(models.Model):
    ENROLLED = "enrolled"
    IN_PROGRESS = "in_progress"
    PENDING = "pending"
    COMPLETED = "completed"
    DROPPED = "dropped"

    STATUS_CHOICES = (
        (ENROLLED, "Not Started"),
        (IN_PROGRESS, "In Progress"),
        (PENDING, "Pending"),
        (COMPLETED, "Completed"),
        (DROPPED, "Dropped"),
    )

    student = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={"is_staff": False},
        related_name="enrollments",
    )

    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="enrollments"
    )

    status = models.CharField(
        max_length=50, choices=STATUS_CHOICES, default=ENROLLED, db_index=True
    )

    enrolled_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        unique_together = ("student", "course")
        ordering = ('-enrolled_at',)
        
    def __str__(self):
        return f"{self.student} is enrolled {self.course} status is {self.status}"