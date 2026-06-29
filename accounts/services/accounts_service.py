import logging

from django.contrib.auth import get_user_model
from django.db import transaction

logger = logging.getLogger("business")

User = get_user_model()


class AccountsService:

    def register_user(self, username, password, email=None):
        with transaction.atomic():
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email or "",
            )
            logger.info("用户注册", extra={"user_id": user.id, "username": username})
            return user

    def create_user(self, username, password, email=None, is_staff=False, is_active=True):
        with transaction.atomic():
            user = User.objects.create_user(
                username=username,
                password=password,
                email=email or "",
                is_staff=is_staff,
            )
            if not is_active:
                user.is_active = False
                user.save(update_fields=["is_active"])
            logger.info("管理员创建用户", extra={
                "user_id": user.id, "username": username,
                "is_staff": is_staff, "is_active": is_active,
            })
            return user

    def list_users(self):
        return User.objects.all().order_by("-date_joined")

    def get_user(self, user_id):
        return User.objects.get(id=user_id)

    def update_user(self, user_id, data):
        with transaction.atomic():
            user = self.get_user(user_id)
            for key in ["username", "email", "is_staff", "is_active"]:
                if key in data:
                    setattr(user, key, data[key])
            password = data.get("password")
            if password:
                user.set_password(password)
            user.save()
            logger.info("管理员更新用户", extra={"user_id": user.id})
            return user
