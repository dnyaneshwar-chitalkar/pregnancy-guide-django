
from django.urls import path
from . import views


urlpatterns = [

    # Home
    path(
        "",
        views.home,
        name="home"
    ),

    # Login
    path(
        "login/",
        views.login_view,
        name="login"
    ),

    # Register
    path(
        "register/",
        views.register_view,
        name="register"
    ),

    # Logout
    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),

    # Admin Dashboard
    path(
        "admin-dashboard/",
        views.admin_dashboard,
        name="admin_dashboard"
    ),
# Users Page
path(
    "admin-dashboard/users/",
    views.users_page,
    name="users_page"
),
# Create User
path(
    "admin-dashboard/users/create/",
    views.create_user,
    name="create_user"
),
# View User
path(
    "admin-dashboard/users/<int:user_id>/",
    views.view_user,
    name="view_user"
),

# Delete User
path(
    "admin-dashboard/users/<int:user_id>/delete/",
    views.delete_user,
    name="delete_user"
),
]

