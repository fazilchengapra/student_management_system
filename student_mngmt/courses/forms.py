from django import forms
from .models import Course


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            "title",
            "course_url",
            "description",
            "video_link",
            "duration",
        ]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-input","placeholder":'Eg. Python'}),
            "course_url": forms.FileInput(attrs={"class": "form-input"}),
            "description": forms.Textarea(attrs={"class": "form-input","placeholder":'Description'}),
            "video_link": forms.URLInput(attrs={"class": "form-input","placeholder":'Past a video link'}),
            "duration": forms.TextInput(attrs={"class": "form-input","placeholder":'eg. 2hours'}),
        }
