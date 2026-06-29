import logging
from django.db import transaction
from django.db.models import Sum

from ..models import Transaction

logger = logging.getLogger("business")


class TransactionService:

    def list_transactions(self, year=None, month=None, type_filter=None,
                          category_id=None):
        qs = Transaction.objects.filter(
            is_deleted=False).select_related("category")
        if year:
            qs = qs.filter(date__year=year)
        if month:
            qs = qs.filter(date__month=month)
        if type_filter:
            qs = qs.filter(type=type_filter)
        if category_id:
            qs = qs.filter(category_id=category_id)
        return qs

    def get_transaction(self, transaction_id):
        return Transaction.objects.get(id=transaction_id, is_deleted=False)

    def create_transaction(self, data):
        with transaction.atomic():
            t = Transaction.objects.create(**data)
            logger.info(
                "创建流水",
                extra={
                    "transaction_id": t.id,
                    "amount": str(t.amount),
                    "type": t.type,
                },
            )
            return t

    def update_transaction(self, transaction_id, data):
        with transaction.atomic():
            t = self.get_transaction(transaction_id)
            for key, value in data.items():
                setattr(t, key, value)
            t.save()
            logger.info("更新流水", extra={"transaction_id": t.id})
            return t

    def delete_transaction(self, transaction_id):
        with transaction.atomic():
            t = self.get_transaction(transaction_id)
            t.is_deleted = True
            t.save()
            logger.info("删除流水", extra={"transaction_id": t.id})

    def get_statistics(self, year, month):
        qs = Transaction.objects.filter(
            is_deleted=False, date__year=year, date__month=month,
        )
        income = (qs.filter(type="INCOME").aggregate(
            total=Sum("amount"))["total"] or 0)
        expense = (qs.filter(type="EXPENSE").aggregate(
            total=Sum("amount"))["total"] or 0)

        income_by_cat = (
            qs.filter(type="INCOME")
            .values("category__name", "category__icon")
            .annotate(total=Sum("amount"))
            .order_by("-total")
        )
        expense_by_cat = (
            qs.filter(type="EXPENSE")
            .values("category__name", "category__icon")
            .annotate(total=Sum("amount"))
            .order_by("-total")
        )

        return {
            "income": income,
            "expense": expense,
            "balance": income - expense,
            "income_by_cat": list(income_by_cat),
            "expense_by_cat": list(expense_by_cat),
        }
