from django.urls import path
from . import views

urlpatterns = [
    # Auth
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register_view, name="register"),
    # Admin
    path("admin/dashboard/", views.admin_dashboard, name="admin_dashboard"),
    path("admin/users/", views.admin_user_list, name="admin_user_list"),
    path("admin/users/create/", views.admin_user_create, name="admin_user_create"),
    path("admin/users/<int:pk>/edit/", views.admin_user_edit, name="admin_user_edit"),
]
