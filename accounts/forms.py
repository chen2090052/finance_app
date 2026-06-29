from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class LoginForm(forms.Form):
    username = forms.CharField(label="用户名", max_length=150)
    password = forms.CharField(label="密码", widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(label="邮箱", required=False)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")


class AdminUserForm(forms.ModelForm):
    password = forms.CharField(
        label="密码", required=False,
        widget=forms.PasswordInput(attrs={"placeholder": "留空则不修改"}),
    )

    class Meta:
        model = User
        fields = ["username", "email", "is_staff", "is_active"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.setdefault("class", "form-control")
