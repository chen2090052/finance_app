import logging
from django.db import transaction

from ..models import Category, Transaction

logger = logging.getLogger("business")


class CategoryService:

    def list_categories(self, type_filter=None):
        qs = Category.objects.filter(is_deleted=False)
        if type_filter:
            qs = qs.filter(type=type_filter)
        return qs

    def create_category(self, data):
        with transaction.atomic():
            c = Category.objects.create(**data)
            logger.info("创建分类", extra={"category_id": c.id, "name": c.name})
            return c

    def update_category(self, category_id, data):
        with transaction.atomic():
            c = Category.objects.get(id=category_id, is_deleted=False)
            for key, value in data.items():
                setattr(c, key, value)
            c.save()
            logger.info("更新分类", extra={"category_id": c.id})
            return c

    def delete_category(self, category_id):
        with transaction.atomic():
            c = Category.objects.get(id=category_id, is_deleted=False)
            if Transaction.objects.filter(
                category=c, is_deleted=False
            ).exists():
                raise ValueError("该分类下还有流水记录，无法删除")
            c.is_deleted = True
            c.save()
            logger.info("删除分类", extra={"category_id": c.id})
