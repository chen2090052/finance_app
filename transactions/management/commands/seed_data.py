from django.core.management.base import BaseCommand
from transactions.models import Category


class Command(BaseCommand):
    help = "初始化默认分类数据"

    def handle(self, *args, **options):
        categories = [
            {"name": "工资", "type": "INCOME", "icon": "💰", "sort_order": 1},
            {"name": "奖金", "type": "INCOME", "icon": "🎁", "sort_order": 2},
            {"name": "兼职", "type": "INCOME", "icon": "💼", "sort_order": 3},
            {"name": "投资收益", "type": "INCOME", "icon": "📈", "sort_order": 4},
            {"name": "其他收入", "type": "INCOME", "icon": "📥", "sort_order": 5},
            {"name": "餐饮", "type": "EXPENSE", "icon": "🍜", "sort_order": 1},
            {"name": "交通", "type": "EXPENSE", "icon": "🚌", "sort_order": 2},
            {"name": "购物", "type": "EXPENSE", "icon": "🛒", "sort_order": 3},
            {"name": "住房", "type": "EXPENSE", "icon": "🏠", "sort_order": 4},
            {"name": "娱乐", "type": "EXPENSE", "icon": "🎮", "sort_order": 5},
            {"name": "医疗", "type": "EXPENSE", "icon": "💊", "sort_order": 6},
            {"name": "教育", "type": "EXPENSE", "icon": "📚", "sort_order": 7},
            {"name": "通讯", "type": "EXPENSE", "icon": "📱", "sort_order": 8},
            {"name": "其他支出", "type": "EXPENSE", "icon": "📤", "sort_order": 9},
        ]

        created = 0
        for cat in categories:
            _, is_new = Category.objects.get_or_create(
                name=cat["name"], type=cat["type"],
                defaults=cat,
            )
            if is_new:
                created += 1

        self.stdout.write(self.style.SUCCESS(f"初始化完成，新增 {created} 个分类"))
