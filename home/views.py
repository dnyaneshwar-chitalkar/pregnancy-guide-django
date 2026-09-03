from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from .models import CustomUser


# =====================================================
# HOME
# =====================================================

def home(request):

    open_login = request.session.pop("open_login", False)

    return render(
        request,
        "home/index.html",
        {
            "open_login": open_login
        }
    )


# =====================================================
# ADMIN DASHBOARD
# =====================================================

def is_staff_user(user):
    return user.is_authenticated and user.is_staff


@login_required
@user_passes_test(is_staff_user, login_url="home")
def admin_dashboard(request):

    return render(
        request,
        "admin_panel/dashboard.html"
    )
    # =====================================================
    # USERS PAGE
    # =====================================================


@login_required
@user_passes_test(is_staff_user, login_url="home")
def users_page(request):
    search_query = request.GET.get("search", "").strip()

    users = CustomUser.objects.all().order_by("-date_joined")

    if search_query:
        users = users.filter(
            Q(first_name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(last_name__icontains=search_query) |
            Q(username__icontains=search_query)
        )

    return render(
        request,
        "admin_panel/users.html",
        {
            "users": users,
            "search_query": search_query
        }
    )


# =====================================================
# CREATE USER - ADMIN
# =====================================================

@login_required
@user_passes_test(is_staff_user, login_url="home")
def create_user(request):
    if request.method == "POST":

        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        email = request.POST.get("email", "").strip().lower()
        phone_number = request.POST.get("phone_number", "").strip()
        password = request.POST.get("password", "")

        # Check required fields
        if not first_name or not email or not password:
            messages.error(
                request,
                "Please fill all required fields."
            )
            return redirect("users_page")

        # Check duplicate email
        if CustomUser.objects.filter(email=email).exists():
            messages.error(
                request,
                "Email already registered."
            )
            return redirect("users_page")

        # Create user
        user = CustomUser.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )

        # Save phone number
        if phone_number:
            user.phone_number = phone_number
            user.save()

        messages.success(
            request,
            "User created successfully!"
        )

        return redirect("users_page")

    return redirect("users_page")

# =====================================================
# VIEW USER
# =====================================================

@login_required
@user_passes_test(is_staff_user, login_url="home")
def view_user(request, user_id):

    try:
        user = CustomUser.objects.get(id=user_id)
    except CustomUser.DoesNotExist:
        messages.error(request, "User not found.")
        return redirect("users_page")

    return render(
        request,
        "admin_panel/user_detail.html",
        {
            "user": user
        }
    )


# =====================================================
# DELETE USER
# =====================================================

@login_required
@user_passes_test(is_staff_user, login_url="home")
def delete_user(request, user_id):

    if request.method == "POST":

        try:
            user = CustomUser.objects.get(id=user_id)

            # Prevent admin from deleting himself
            if user.id == request.user.id:
                messages.error(
                    request,
                    "You cannot delete your own account."
                )
                return redirect("users_page")

            user.delete()

            messages.success(
                request,
                "User deleted successfully."
            )

        except CustomUser.DoesNotExist:

            messages.error(
                request,
                "User not found."
            )

    return redirect("users_page")
# =====================================================
# REGISTER
# =====================================================


def register_view(request):
    if request.method == "POST":

        name = request.POST.get("name", "").strip()
        email = request.POST.get("email", "").strip().lower()
        password = request.POST.get("password", "")
        confirm_password = request.POST.get("confirm_password", "")

        print("REGISTER DATA:", name, email)

        if not name or not email or not password or not confirm_password:
            messages.error(request, "Please fill all fields.")
            return redirect("home")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("home")

        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return redirect("home")

        user = CustomUser.objects.create_user(
            username=email,
            email=email,
            password=password,
            first_name=name
        )

        print("NEW USER CREATED:", user.email, user.first_name)

        request.session["open_login"] = True

        messages.success(
            request,
            "Registration successful! Please login."
        )

        return redirect("home")

    return redirect("home")

# =====================================================
# LOGIN
# EMAIL OR PHONE + PASSWORD
# =====================================================

def login_view(request):

    if request.method != "POST":
        return redirect("home")

    login_input = request.POST.get(
        "login_input",
        ""
    ).strip()

    password = request.POST.get(
        "password",
        ""
    )

    if not login_input or not password:

        messages.error(
            request,
            "Please enter email/phone and password."
        )

        return redirect("home")

    user_obj = None

    # -------------------------------------------------
    # FIND USER BY EMAIL
    # -------------------------------------------------

    if "@" in login_input:

        try:

            user_obj = CustomUser.objects.get(
                email=login_input.lower()
            )

        except CustomUser.DoesNotExist:

            user_obj = None

    # -------------------------------------------------
    # FIND USER BY PHONE
    # -------------------------------------------------

    else:

        try:

            user_obj = CustomUser.objects.get(
                phone_number=login_input
            )

        except CustomUser.DoesNotExist:

            user_obj = None

    # -------------------------------------------------
    # AUTHENTICATE
    # -------------------------------------------------

    if user_obj:

        user = authenticate(
            request,
            username=user_obj.email,
            password=password
        )

        if user is not None:

            # Create Django login session
            login(
                request,
                user,
                backend="django.contrib.auth.backends.ModelBackend"
            )

            messages.success(
                request,
                f"Welcome back, {user.first_name or user.email}!"
            )

            return redirect("home")

    # -------------------------------------------------
    # LOGIN FAILED
    # -------------------------------------------------

    messages.error(
        request,
        "Invalid email/phone or password."
    )

    return redirect("home")


# =====================================================
# LOGOUT
# =====================================================

def logout_view(request):

    logout(request)

    messages.success(
        request,
        "You have been logged out."
    )

    return redirect("home")