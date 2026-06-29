from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("transactions", "0003_assign_existing_transactions"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transaction",
            name="user",
            field=models.ForeignKey(
                on_delete=models.deletion.CASCADE,
                to="auth.user",
                verbose_name="用户",
                db_index=True,
            ),
            preserve_default=False,
        ),
    ]
