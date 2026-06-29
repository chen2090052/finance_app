from django.db import models


class Category(models.Model):
    TYPE_CHOICES = [
        ("INCOME", "收入"),
        ("EXPENSE", "支出"),
    ]

    name = models.CharField("分类名称", max_length=50)
    type = models.CharField("类型", max_length=10, choices=TYPE_CHOICES)
    icon = models.CharField("图标", max_length=10, default="📄")
    sort_order = models.IntegerField("排序", default=0)
    is_deleted = models.BooleanField("是否删除", default=False)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        verbose_name = "分类"
        verbose_name_plural = "分类"
        ordering = ["sort_order", "id"]

    def __str__(self):
        return f"{self.icon} {self.name}"


class Transaction(models.Model):
    TYPE_CHOICES = [
        ("INCOME", "收入"),
        ("EXPENSE", "支出"),
    ]

    amount = models.DecimalField("金额", max_digits=12, decimal_places=2)
    type = models.CharField("类型", max_length=10, choices=TYPE_CHOICES, db_index=True)
    category = models.ForeignKey(
        Category, on_delete=models.PROTECT,
        verbose_name="分类", db_index=True,
    )
    note = models.CharField("备注", max_length=200, blank=True)
    date = models.DateField("日期", db_index=True)
    is_deleted = models.BooleanField("是否删除", default=False)
    created_at = models.DateTimeField("创建时间", auto_now_add=True)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        verbose_name = "流水"
        verbose_name_plural = "流水"
        ordering = ["-date", "-created_at"]

    def __str__(self):
        return f"{self.get_type_display()} {self.amount}元 - {self.category.name}"
