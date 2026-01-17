from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User,
    OTP,
    Subscription,
    ResumeTemplate,
    TemplatePricing,
    Resume,
)

# =====================================================
# USER ADMIN
# =====================================================
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    model = User

    ordering = ("-date_joined",)
    list_display = ("phone", "name", "is_staff", "is_active")
    list_filter = ("is_staff", "is_active")
    search_fields = ("phone", "name")

    fieldsets = (
        (None, {"fields": ("phone", "password")}),
        ("Personal Info", {"fields": ("name", "email", "pincode")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "phone",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )


# =====================================================
# OTP ADMIN
# =====================================================
@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ("phone", "code", "created_at")
    search_fields = ("phone",)
    readonly_fields = ("created_at",)
    ordering = ("-created_at",)


# =====================================================
# SUBSCRIPTION ADMIN
# =====================================================
@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "plan",
        "status",
        "amount",
        "start_date",
        "end_date",
        "auto_renew",
    )
    list_filter = ("plan", "status", "auto_renew")
    search_fields = ("user__phone",)
    ordering = ("-created_at",)


# =====================================================
# RESUME TEMPLATE ADMIN
# =====================================================
@admin.register(ResumeTemplate)
class ResumeTemplateAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "layout",
        "status",
        "version",
        "downloads",
        "updated_at",
    )
    list_filter = ("status", "category", "layout")
    search_fields = ("name",)
    readonly_fields = ("downloads", "rating", "created_at", "updated_at")
    ordering = ("-updated_at",)


# =====================================================
# TEMPLATE PRICING ADMIN
# =====================================================
@admin.register(TemplatePricing)
class TemplatePricingAdmin(admin.ModelAdmin):
    list_display = (
        "template",
        "billing_type",
        "currency",
        "price",
        "discount_percent",
        "final_price",
        "status",
    )
    list_filter = ("billing_type", "status", "currency")
    readonly_fields = ("final_price",)
    ordering = ("-updated_at",)


# =====================================================
# RESUME ADMIN
# =====================================================
@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "user",
        "status",
        "template_name",
        "download_count",
        "updated_at",
    )
    list_filter = ("status",)
    search_fields = ("title", "user__phone")
    ordering = ("-updated_at",)
