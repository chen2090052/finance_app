from datetime import date

from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CategoryForm, TransactionForm
from .models import Category, Transaction
from .services.category_service import CategoryService
from .services.transaction_service import TransactionService

tx_svc = TransactionService()
cat_svc = CategoryService()


def _get_year_month(request):
    today = date.today()
    year = int(request.GET.get("year", today.year))
    month = int(request.GET.get("month", today.month))
    return year, month


def _years_range(current_year):
    return list(range(current_year - 2, current_year + 3))


def _months_list():
    return list(range(1, 13))


@login_required
def transaction_list(request):
    year, month = _get_year_month(request)
    type_filter = request.GET.get("type", "")
    category_id = request.GET.get("category", "")

    transactions = tx_svc.list_transactions(
        user=request.user,
        year=year, month=month,
        type_filter=type_filter or None,
        category_id=category_id or None,
    )
    stats = tx_svc.get_statistics(request.user, year, month)
    categories = Category.objects.filter(is_deleted=False)

    return render(request, "transactions/transaction_list.html", {
        "transactions": transactions,
        "stats": stats,
        "categories": categories,
        "year": year,
        "month": month,
        "years": _years_range(year),
        "months": _months_list(),
        "filter_type": type_filter,
        "filter_category": category_id,
    })


@login_required
def transaction_create(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            tx_svc.create_transaction(form.cleaned_data, request.user)
            messages.success(request, "流水添加成功")
            return redirect("transaction_list")
    else:
        initial = {"date": date.today()}
        t = request.GET.get("type", "")
        if t:
            initial["type"] = t
        form = TransactionForm(initial=initial)

    return render(request, "transactions/transaction_form.html", {
        "form": form,
        "is_edit": False,
    })


@login_required
def transaction_edit(request, pk):
    t = get_object_or_404(Transaction, id=pk, is_deleted=False)
    if not request.user.is_staff and t.user != request.user:
        messages.error(request, "无权操作此记录")
        return redirect("transaction_list")
    if request.method == "POST":
        form = TransactionForm(request.POST, instance=t)
        if form.is_valid():
            tx_svc.update_transaction(pk, form.cleaned_data)
            messages.success(request, "流水更新成功")
            return redirect("transaction_list")
    else:
        form = TransactionForm(instance=t)

    return render(request, "transactions/transaction_form.html", {
        "form": form,
        "is_edit": True,
    })


@login_required
def transaction_delete(request, pk):
    if request.method == "POST":
        t = get_object_or_404(Transaction, id=pk, is_deleted=False)
        if not request.user.is_staff and t.user != request.user:
            messages.error(request, "无权操作此记录")
        else:
            tx_svc.delete_transaction(pk)
            messages.success(request, "流水已删除")
    return redirect("transaction_list")


@login_required
@user_passes_test(lambda u: u.is_staff)
def category_list(request):
    categories = cat_svc.list_categories()
    return render(request, "transactions/category_list.html", {
        "categories": categories,
    })


@login_required
@user_passes_test(lambda u: u.is_staff)
def category_create(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            cat_svc.create_category(form.cleaned_data)
            messages.success(request, "分类添加成功")
            return redirect("category_list")
    else:
        form = CategoryForm()

    return render(request, "transactions/category_form.html", {
        "form": form,
        "is_edit": False,
    })


@login_required
@user_passes_test(lambda u: u.is_staff)
def category_edit(request, pk):
    c = get_object_or_404(Category, id=pk, is_deleted=False)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=c)
        if form.is_valid():
            cat_svc.update_category(pk, form.cleaned_data)
            messages.success(request, "分类更新成功")
            return redirect("category_list")
    else:
        form = CategoryForm(instance=c)

    return render(request, "transactions/category_form.html", {
        "form": form,
        "is_edit": True,
    })


@login_required
@user_passes_test(lambda u: u.is_staff)
def category_delete(request, pk):
    if request.method == "POST":
        try:
            cat_svc.delete_category(pk)
            messages.success(request, "分类已删除")
        except ValueError as e:
            messages.error(request, str(e))
    return redirect("category_list")


@login_required
def statistics(request):
    year, month = _get_year_month(request)
    stats = tx_svc.get_statistics(request.user, year, month)

    base_qs = Transaction.objects.filter(is_deleted=False, date__year=year)
    if not request.user.is_staff:
        base_qs = base_qs.filter(user=request.user)

    annual_income = (
        base_qs.filter(type="INCOME").aggregate(total=Sum("amount"))["total"] or 0
    )
    annual_expense = (
        base_qs.filter(type="EXPENSE").aggregate(total=Sum("amount"))["total"] or 0
    )

    return render(request, "transactions/statistics.html", {
        "stats": stats,
        "year": year,
        "month": month,
        "years": _years_range(year),
        "months": _months_list(),
        "annual_income": annual_income,
        "annual_expense": annual_expense,
        "annual_balance": annual_income - annual_expense,
    })


@login_required
def load_categories(request):
    t = request.GET.get("type")
    qs = Category.objects.filter(is_deleted=False)
    if t:
        qs = qs.filter(type=t)
    return render(request, "transactions/category_options.html", {
        "categories": qs,
    })
