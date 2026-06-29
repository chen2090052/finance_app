from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages

from transactions.models import Transaction
from .forms import AdminUserForm, LoginForm, RegistrationForm
from .services.accounts_service import AccountsService

svc = AccountsService()


def login_view(request):
    if request.user.is_authenticated:
        return redirect("transaction_list")
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd["username"], password=cd["password"])
            if user is not None:
                login(request, user)
                messages.success(request, f"欢迎回来，{user.username}")
                next_url = request.GET.get("next", "transaction_list")
                return redirect(next_url)
            messages.error(request, "用户名或密码错误")
    else:
        form = LoginForm()
    return render(request, "accounts/login.html", {"form": form})


def logout_view(request):
    logout(request)
    messages.success(request, "已退出登录")
    return redirect("login")


def register_view(request):
    if request.user.is_authenticated:
        return redirect("transaction_list")
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            svc.register_user(
                username=cd["username"],
                password=cd["password1"],
                email=cd.get("email", ""),
            )
            messages.success(request, "注册成功，请登录")
            return redirect("login")
    else:
        form = RegistrationForm()
    return render(request, "accounts/register.html", {"form": form})


@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_dashboard(request):
    total_users = User.objects.filter(is_active=True).count()
    total_tx = Transaction.objects.filter(is_deleted=False).count()
    income = Transaction.objects.filter(is_deleted=False, type="INCOME").aggregate(
        total=Sum("amount")
    )["total"] or 0
    expense = Transaction.objects.filter(is_deleted=False, type="EXPENSE").aggregate(
        total=Sum("amount")
    )["total"] or 0
    recent = (
        Transaction.objects.filter(is_deleted=False)
        .select_related("category", "user")
        .order_by("-created_at")[:10]
    )
    return render(request, "accounts/admin_dashboard.html", {
        "total_users": total_users,
        "total_transactions": total_tx,
        "total_income": income,
        "total_expense": expense,
        "total_balance": income - expense,
        "recent_transactions": recent,
    })


@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_user_list(request):
    users = svc.list_users()
    return render(request, "accounts/admin_user_list.html", {"users": users})


@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_user_create(request):
    if request.method == "POST":
        form = AdminUserForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            svc.create_user(
                username=cd["username"],
                password=cd["password"],
                email=cd.get("email", ""),
                is_staff=cd.get("is_staff", False),
                is_active=cd.get("is_active", True),
            )
            messages.success(request, "用户创建成功")
            return redirect("admin_user_list")
    else:
        form = AdminUserForm()
    return render(request, "accounts/admin_user_form.html", {
        "form": form, "is_edit": False,
    })


@login_required
@user_passes_test(lambda u: u.is_staff)
def admin_user_edit(request, pk):
    user_obj = get_object_or_404(User, id=pk)
    if request.method == "POST":
        form = AdminUserForm(request.POST, instance=user_obj)
        if form.is_valid():
            svc.update_user(pk, form.cleaned_data)
            messages.success(request, "用户更新成功")
            return redirect("admin_user_list")
    else:
        form = AdminUserForm(instance=user_obj)
    return render(request, "accounts/admin_user_form.html", {
        "form": form, "is_edit": True,
    })
