import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "website_backend.settings")
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

EMAIL = os.environ.get("DJANGO_SUPERUSER_EMAIL", "admin@example.com")
PASSWORD = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "Admin@123")
PHONE = os.environ.get("DJANGO_SUPERUSER_PHONE", "9999999999")

# 👇 REQUIRED FIELD (VERY IMPORTANT)
USERNAME = os.environ.get("DJANGO_SUPERUSER_USERNAME", "admin")

if not User.objects.filter(email=EMAIL).exists():
    User.objects.create_superuser(
        username=USERNAME,   # ✅ FIX HERE
        email=EMAIL,
        password=PASSWORD,
        phone=PHONE,
        name="Admin"
    )
    print("✅ Superuser created successfully")
else:
    print("ℹ️ Superuser already exists")
