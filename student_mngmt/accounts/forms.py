from django import forms
from .models import User
from datetime import date


class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(),
        min_length=4,
        error_messages={"min-length": "minimum 4 character required!"},
    )

    confirm_password = forms.CharField(widget=forms.PasswordInput())

    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}), required=False
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "password",
            "phone",
            "date_of_birth",
            "profile_picture",
            "confirm_password",
        ]

    def clean_username(self):
        username = self.cleaned_data.get("username")

        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username is already exist!")

        return username

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get("date_of_birth")

        if date_of_birth and date_of_birth > date.today():
            raise forms.ValidationError("Invalid date of birth")

        return date_of_birth

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password:
            if password != confirm_password:
                self.add_error("confirm_password", "Passwords do not match!")

        return cleaned_data


class UpdateStudentForm(forms.ModelForm):

    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}), required=False
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "phone",
            "date_of_birth",
            "profile_picture",
            "is_active",
        ]

    def clean_username(self):
        username = self.cleaned_data.get("username")

        qs = User.objects.filter(username=username)

        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError("Username already exists!")

        return username

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get("date_of_birth")

        if date_of_birth and date_of_birth > date.today():
            raise forms.ValidationError("Invalid date of birth")

        return date_of_birth


class StudentSelfUpdateForm(forms.ModelForm):

    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}), required=False
    )

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "phone",
            "date_of_birth",
            "profile_picture",
        ]

    def clean_username(self):
        username = self.cleaned_data.get("username")

        qs = User.objects.filter(username=username)

        if self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)

        if qs.exists():
            raise forms.ValidationError("Username already exists!")

        return username

    def clean_date_of_birth(self):
        date_of_birth = self.cleaned_data.get("date_of_birth")

        if date_of_birth and date_of_birth > date.today():
            raise forms.ValidationError("Invalid date of birth")

        return date_of_birth
