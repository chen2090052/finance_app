from django.contrib.auth.hashers import make_password
from django.db import migrations


def assign_existing_transactions(apps, schema_editor):
    User = apps.get_model("auth", "User")
    Transaction = apps.get_model("transactions", "Transaction")

    admin, created = User.objects.get_or_create(
        username="admin",
        defaults={
            "is_staff": True,
            "is_superuser": True,
            "password": make_password("admin123"),
        },
    )

    Transaction.objects.filter(user__isnull=True).update(user=admin)


def reverse_func(apps, schema_editor):
    Transaction = apps.get_model("transactions", "Transaction")
    Transaction.objects.all().update(user=None)


class Migration(migrations.Migration):

    dependencies = [
        ("transactions", "0002_transaction_user"),
    ]

    operations = [
        migrations.RunPython(assign_existing_transactions, reverse_func),
    ]
