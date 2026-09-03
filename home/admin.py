from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, PregnancyWeek


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):

    fieldsets = UserAdmin.fieldsets + (
        ("Additional Information", {
            "fields": ("phone_number",)
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional Information", {
            "fields": ("email", "phone_number")
        }),
    )


@admin.register(PregnancyWeek)
class PregnancyWeekAdmin(admin.ModelAdmin):
    list_display = ("week_number", "title")