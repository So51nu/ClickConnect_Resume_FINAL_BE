# # from rest_framework.views import APIView
# # from rest_framework.response import Response
# # from rest_framework.permissions import AllowAny, IsAdminUser
# # from rest_framework import status
# # from rest_framework_simplejwt.tokens import RefreshToken
# # from django.contrib.auth import authenticate

# # from .models import User, OTP
# # from .serializers import UserSerializer
# # import random


# # # ================== SEND OTP ==================

# # class SendOTPView(APIView):
# #     permission_classes = [AllowAny]

# #     def post(self, request):
# #         phone = request.data.get("phone")

# #         if not phone:
# #             return Response({"message": "Phone required"}, status=400)

# #         otp_code = str(random.randint(100000, 999999))
# #         OTP.objects.create(phone=phone, code=otp_code)

# #         print("OTP (DEV):", otp_code)

# #         return Response({
# #             "is_registered": User.objects.filter(phone=phone).exists()
# #         })


# # # ================== VERIFY OTP ==================
# # from django.utils import timezone
# # from rest_framework.views import APIView
# # from rest_framework.response import Response
# # from rest_framework.permissions import AllowAny
# # from rest_framework_simplejwt.tokens import RefreshToken
# # from .models import User, OTP

# # from .models import User, OTP
# # from .serializers import UserSerializer
# # import random


# # # ================== SEND OTP ==================
# # class VerifyOTPView(APIView):
# #     permission_classes = [AllowAny]

# #     def post(self, request):
# #         phone = request.data.get("phone")
# #         otp = request.data.get("otp")

# #         if not phone or not otp:
# #             return Response({"message": "Phone and OTP are required"}, status=400)

# #         otp_obj = OTP.objects.filter(phone=phone, code=otp).last()
# #         if not otp_obj or not otp_obj.is_valid():
# #             return Response({"message": "Invalid OTP"}, status=400)

# #         user = User.objects.filter(phone=phone).first()

# #         # 🔹 AUTO DECIDE: REGISTER or LOGIN
# #         if not user:
# #             user = User.objects.create(
# #                 phone=phone,
# #                 name=request.data.get("name", ""),
# #                 email=request.data.get("email", ""),
# #                 pincode=request.data.get("pincode", ""),
# #             )
# #             action = "registered"
# #         else:
# #             action = "logged_in"

# #         otp_obj.delete()

# #         refresh = RefreshToken.for_user(user)

# #         return Response({
# #             "action": action,
# #             "access": str(refresh.access_token),
# #             "refresh": str(refresh),
# #             "user": {
# #                 "phone": user.phone,
# #                 "name": user.name,
# #                 "email": user.email,
# #                 "pincode": user.pincode,
# #             }
# #         })

# # # ================== ADMIN LOGIN ==================

# # class AdminLoginView(APIView):
# #     permission_classes = [AllowAny]

# #     def post(self, request):
# #         phone = request.data.get("phone")
# #         password = request.data.get("password")

# #         user = authenticate(phone=phone, password=password)

# #         if not user or not user.is_staff:
# #             return Response(
# #                 {"error": "Invalid admin credentials"},
# #                 status=status.HTTP_401_UNAUTHORIZED
# #             )

# #         refresh = RefreshToken.for_user(user)

# #         return Response({
# #             "access": str(refresh.access_token),
# #             "refresh": str(refresh),
# #             "user": {
# #                 "id": user.id,
# #                 "phone": user.phone,
# #                 "name": user.name,
# #                 "role": "admin",
# #             }
# #         })


# # # ================== ADMIN USER LIST ==================

# # class AdminUserListView(APIView):
# #     permission_classes = [IsAdminUser]

# #     def get(self, request):
# #         users = User.objects.filter(is_staff=False).order_by("-date_joined")
# #         serializer = UserSerializer(users, many=True)
# #         return Response(serializer.data)


# # # ================== ADMIN USER DETAIL ==================

# # class AdminUserDetailView(APIView):
# #     permission_classes = [IsAdminUser]

# #     def delete(self, request, pk):
# #         try:
# #             user = User.objects.get(pk=pk, is_staff=False)
# #             user.delete()
# #             return Response({"message": "User deleted"})
# #         except User.DoesNotExist:
# #             return Response({"error": "User not found"}, status=404)
# # views.py
# import random
# from django.contrib.auth import authenticate
# from rest_framework import status
# from rest_framework.permissions import AllowAny, IsAdminUser
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework_simplejwt.tokens import RefreshToken

# from .models import User, OTP
# from .serializers import UserSerializer


# # ================== SEND OTP ==================
# class SendOTPView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         phone = request.data.get("phone")
#         if not phone:
#             return Response({"message": "Phone required"}, status=400)

#         otp_code = str(random.randint(100000, 999999))
#         OTP.objects.create(phone=phone, code=otp_code)

#         # DEV only
#         print("OTP (DEV):", otp_code)

#         return Response({"is_registered": User.objects.filter(phone=phone).exists()})


# # ================== VERIFY OTP ==================
# class VerifyOTPView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         phone = request.data.get("phone")
#         # support both "otp" and "code" from frontend
#         otp_value = request.data.get("otp") or request.data.get("code")

#         if not phone or not otp_value:
#             return Response({"message": "Phone and OTP are required"}, status=400)

#         otp_obj = OTP.objects.filter(phone=phone, code=otp_value).last()
#         if not otp_obj or not otp_obj.is_valid():
#             return Response({"message": "Invalid OTP"}, status=400)

#         user = User.objects.filter(phone=phone).first()

#         if not user:
#             user = User.objects.create(
#                 phone=phone,
#                 name=request.data.get("name", ""),
#                 email=request.data.get("email", ""),
#                 pincode=request.data.get("pincode", ""),
#                 is_staff=False,
#             )
#             user.set_unusable_password()
#             user.save()
#             action = "registered"
#         else:
#             action = "logged_in"

#         otp_obj.delete()
#         refresh = RefreshToken.for_user(user)

#         return Response({
#             "action": action,
#             "access": str(refresh.access_token),
#             "refresh": str(refresh),
#             "user": {
#                 "id": user.id,
#                 "phone": user.phone,
#                 "name": user.name,
#                 "email": user.email,
#                 "pincode": user.pincode,
#             }
#         })


# # ================== ADMIN LOGIN ==================
# class AdminLoginView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         phone = request.data.get("phone")
#         password = request.data.get("password")

#         user = authenticate(phone=phone, password=password)
#         if not user or not user.is_staff:
#             return Response({"error": "Invalid admin credentials"}, status=status.HTTP_401_UNAUTHORIZED)

#         refresh = RefreshToken.for_user(user)

#         return Response({
#             "access": str(refresh.access_token),
#             "refresh": str(refresh),
#             "user": {
#                 "id": user.id,
#                 "phone": user.phone,
#                 "name": user.name,
#                 "role": "admin",
#             }
#         })


# # ================== ADMIN USER LIST (GET + POST) ==================
# class AdminUserListView(APIView):
#     permission_classes = [IsAdminUser]

#     def get(self, request):
#         users = User.objects.filter(is_staff=False).order_by("-date_joined")
#         serializer = UserSerializer(users, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         # create student/user
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save(is_staff=False)
#             return Response(UserSerializer(user).data, status=201)
#         return Response(serializer.errors, status=400)


# # ================== ADMIN USER DETAIL (GET + PATCH/PUT + DELETE) ==================
# class AdminUserDetailView(APIView):
#     permission_classes = [IsAdminUser]

#     def get(self, request, pk):
#         try:
#             user = User.objects.get(pk=pk, is_staff=False)
#             return Response(UserSerializer(user).data)
#         except User.DoesNotExist:
#             return Response({"error": "User not found"}, status=404)

#     def patch(self, request, pk):
#         try:
#             user = User.objects.get(pk=pk, is_staff=False)
#             serializer = UserSerializer(user, data=request.data, partial=True)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data)
#             return Response(serializer.errors, status=400)
#         except User.DoesNotExist:
#             return Response({"error": "User not found"}, status=404)

#     def put(self, request, pk):
#         # full update
#         try:
#             user = User.objects.get(pk=pk, is_staff=False)
#             serializer = UserSerializer(user, data=request.data, partial=False)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response(serializer.data)
#             return Response(serializer.errors, status=400)
#         except User.DoesNotExist:
#             return Response({"error": "User not found"}, status=404)

#     def delete(self, request, pk):
#         try:
#             user = User.objects.get(pk=pk, is_staff=False)
#             user.delete()
#             return Response({"message": "User deleted"})
#         except User.DoesNotExist:
#             return Response({"error": "User not found"}, status=404)

import random
from django.contrib.auth import authenticate
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import generics

from .models import User, OTP, ResumeTemplate, TemplatePricing
from .serializers import (
    UserSerializer,
    ResumeTemplateSerializer,
    TemplatePricingSerializer,
)


# ================== SEND OTP ==================
class SendOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone = request.data.get("phone")
        if not phone:
            return Response({"message": "Phone required"}, status=400)

        otp_code = str(random.randint(100000, 999999))
        OTP.objects.create(phone=phone, code=otp_code)

        # DEV only
        print("OTP (DEV):", otp_code)

        return Response({"is_registered": User.objects.filter(phone=phone).exists()})


# ================== VERIFY OTP ==================
class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone = request.data.get("phone")
        otp_value = request.data.get("otp") or request.data.get("code")

        if not phone or not otp_value:
            return Response({"message": "Phone and OTP are required"}, status=400)

        otp_obj = OTP.objects.filter(phone=phone, code=otp_value).last()
        if not otp_obj or not otp_obj.is_valid():
            return Response({"message": "Invalid OTP"}, status=400)

        user = User.objects.filter(phone=phone).first()

        if not user:
            user = User.objects.create(
                phone=phone,
                name=request.data.get("name", ""),
                email=request.data.get("email", ""),
                pincode=request.data.get("pincode", ""),
                is_staff=False,
            )
            user.set_unusable_password()
            user.save()
            action = "registered"
        else:
            action = "logged_in"

        otp_obj.delete()

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "action": action,
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "id": user.id,
                    "phone": user.phone,
                    "name": user.name,
                    "email": user.email,
                    "pincode": user.pincode,
                },
            }
        )


# # ================== ADMIN LOGIN ==================
# class AdminLoginView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         phone = request.data.get("phone")
#         password = request.data.get("password")

#         user = authenticate(phone=phone, password=password)
#         if not user or not user.is_staff:
#             return Response(
#                 {"error": "Invalid admin credentials"},
#                 status=status.HTTP_401_UNAUTHORIZED,
#             )

#         refresh = RefreshToken.for_user(user)
#         return Response(
#             {
#                 "access": str(refresh.access_token),
#                 "refresh": str(refresh),
#                 "user": {"id": user.id, "phone": user.phone, "name": user.name, "role": "admin"},
#             }
#         )
# views.py
from django.contrib.auth import authenticate
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken


class AdminLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        phone = request.data.get("phone")
        password = request.data.get("password")

        if not phone or not password:
            return Response(
                {"detail": "Phone and password are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user = authenticate(phone=phone, password=password)
        if not user or not user.is_staff:
            return Response(
                {"detail": "Invalid admin credentials"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        refresh = RefreshToken.for_user(user)

        # ✅ return admin_* keys (frontend will store in admin_access/admin_refresh/admin)
        return Response(
            {
                "action": "logged_in",
                "admin_access": str(refresh.access_token),
                "admin_refresh": str(refresh),
                "admin": {
                    "id": user.id,
                    "phone": user.phone,
                    "name": user.name,
                    "email": user.email or "",
                    "role": "admin",
                },
            }
        )


# ================== ADMIN USERS (CRUD) ==================
class AdminUserListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        users = User.objects.filter(is_staff=False).order_by("-date_joined")
        return Response(UserSerializer(users, many=True).data)

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save(is_staff=False)
            return Response(UserSerializer(user).data, status=201)
        return Response(serializer.errors, status=400)


class AdminUserDetailView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, pk):
        try:
            user = User.objects.get(pk=pk, is_staff=False)
            return Response(UserSerializer(user).data)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

    def patch(self, request, pk):
        try:
            user = User.objects.get(pk=pk, is_staff=False)
            serializer = UserSerializer(user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

    def put(self, request, pk):
        try:
            user = User.objects.get(pk=pk, is_staff=False)
            serializer = UserSerializer(user, data=request.data, partial=False)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=400)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

    def delete(self, request, pk):
        try:
            user = User.objects.get(pk=pk, is_staff=False)
            user.delete()
            return Response({"message": "User deleted"})
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)


# =========================
# ✅ NEW: Admin Templates APIs
# =========================

class AdminTemplateListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = ResumeTemplate.objects.all().order_by("-updated_at")
    serializer_class = ResumeTemplateSerializer


class AdminTemplateDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = ResumeTemplate.objects.all()
    serializer_class = ResumeTemplateSerializer


# =========================
# ✅ NEW: Admin Template Pricing APIs
# =========================

class AdminTemplatePricingListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = TemplatePricing.objects.select_related("template").all().order_by("-updated_at")
    serializer_class = TemplatePricingSerializer


class AdminTemplatePricingDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = TemplatePricing.objects.select_related("template").all()
    serializer_class = TemplatePricingSerializer

# views.py (subscription section ko replace/add karo)
from django.db.models import Sum, Q
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import Subscription
from .serializers import SubscriptionSerializer


class AdminSubscriptionListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        qs = Subscription.objects.select_related("user").order_by("-created_at")

        plan = request.GET.get("plan")
        st = request.GET.get("status")
        search = request.GET.get("search")

        if plan:
            qs = qs.filter(plan=plan)
        if st:
            qs = qs.filter(status=st)

        if search:
            search = search.strip()
            qs = qs.filter(
                Q(user__name__icontains=search)
                | Q(user__email__icontains=search)
                | Q(user__phone__icontains=search)
            )

        serializer = SubscriptionSerializer(qs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SubscriptionSerializer(data=request.data)
        if serializer.is_valid():
            sub = serializer.save()
            return Response(SubscriptionSerializer(sub).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class AdminSubscriptionDetailView(APIView):
    permission_classes = [IsAdminUser]

    def get_object(self, pk):
        return Subscription.objects.select_related("user").get(pk=pk)

    def get(self, request, pk):
        try:
            sub = self.get_object(pk)
            return Response(SubscriptionSerializer(sub).data)
        except Subscription.DoesNotExist:
            return Response({"error": "Subscription not found"}, status=404)

    def patch(self, request, pk):
        try:
            sub = self.get_object(pk)
            serializer = SubscriptionSerializer(sub, data=request.data, partial=True)
            if serializer.is_valid():
                sub = serializer.save()
                return Response(SubscriptionSerializer(sub).data)
            return Response(serializer.errors, status=400)
        except Subscription.DoesNotExist:
            return Response({"error": "Subscription not found"}, status=404)

    def put(self, request, pk):
        try:
            sub = self.get_object(pk)
            serializer = SubscriptionSerializer(sub, data=request.data, partial=False)
            if serializer.is_valid():
                sub = serializer.save()
                return Response(SubscriptionSerializer(sub).data)
            return Response(serializer.errors, status=400)
        except Subscription.DoesNotExist:
            return Response({"error": "Subscription not found"}, status=404)

    def delete(self, request, pk):
        try:
            sub = self.get_object(pk)
            sub.delete()
            return Response({"message": "Subscription deleted"})
        except Subscription.DoesNotExist:
            return Response({"error": "Subscription not found"}, status=404)


class AdminSubscriptionStatsView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        total = Subscription.objects.count()
        active = Subscription.objects.filter(status="Active").count()

        revenue = Subscription.objects.filter(status="Active").aggregate(total=Sum("amount"))["total"] or 0

        churn = 0
        if total:
            churn = round((Subscription.objects.filter(status="Cancelled").count() / total) * 100, 2)

        return Response({
            "total": total,
            "active": active,
            "revenue": revenue,
            "churn": churn,
        })

# views.py (add below your existing template views)
from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils.text import slugify
from django.core.files.base import ContentFile

import json
import requests

from .models import ResumeTemplate
from .serializers import ResumeTemplateSerializer

# ✅ Marketplace templates (FREE) - yahan aap easily add/remove kar sakte ho
MARKETPLACE_TEMPLATES = [
    {
        "key": "simple-01",
        "name": "Simple 01",
        "category": "Classic",
        "layout": "Single Column",
        "color": "#111827",
        "price_type": "free",
        "price": 0,
        "preview_image_url": "",  # optionally put CDN/static url
        "schema": {
            "version": 1,
            "layout": "Single Column",
            "theme": {
                "primary": "#111827",
                "fontFamily": "Georgia, 'Times New Roman', Times, serif",
                "headingUppercase": True,
                "titleSize": 12,
                "bodySize": 10,
                "lineHeight": 1.4,
            },
            "order": ["header", "summary", "experience", "education", "skills", "projects"],
            "columns": {"left": [], "right": []},
            "sections": {
                "header": {"enabled": True},
                "summary": {"enabled": True},
                "experience": {"enabled": True},
                "education": {"enabled": True},
                "skills": {"enabled": True},
                "projects": {"enabled": True},
                "certifications": {"enabled": False},
                "languages": {"enabled": False},
            },
        },
    },
    {
        "key": "modern-02",
        "name": "Modern 02",
        "category": "Modern",
        "layout": "Two Column",
        "color": "#2563eb",
        "price_type": "free",
        "price": 0,
        "preview_image_url": "",
        "schema": {
            "version": 1,
            "layout": "Two Column",
            "theme": {
                "primary": "#2563eb",
                "fontFamily": "system-ui, -apple-system, Segoe UI, Roboto, sans-serif",
                "headingUppercase": True,
                "titleSize": 12,
                "bodySize": 10,
                "lineHeight": 1.35,
            },
            "columns": {"left": ["summary", "skills", "education"], "right": ["header", "experience", "projects"]},
            "order": [],
            "sections": {
                "header": {"enabled": True},
                "summary": {"enabled": True},
                "experience": {"enabled": True},
                "education": {"enabled": True},
                "skills": {"enabled": True},
                "projects": {"enabled": True},
                "certifications": {"enabled": False},
                "languages": {"enabled": False},
            },
        },
    },
    {
        "key": "nexus-03",
        "name": "Nexus 03",
        "category": "Modern",
        "layout": "Sidebar Left",
        "color": "#0b4a6f",
        "price_type": "free",
        "price": 0,
        "preview_image_url": "",
        "schema": {
            "version": 1,
            "layout": "Sidebar Left",
            "theme": {
                "primary": "#0b4a6f",
                "fontFamily": "system-ui, -apple-system, Segoe UI, Roboto, sans-serif",
                "headingUppercase": True,
                "titleSize": 12,
                "bodySize": 10,
                "lineHeight": 1.35,
            },
            "columns": {"left": ["skills", "education", "languages"], "right": ["header", "summary", "experience", "projects"]},
            "order": [],
            "sections": {
                "header": {"enabled": True},
                "summary": {"enabled": True},
                "experience": {"enabled": True},
                "education": {"enabled": True},
                "skills": {"enabled": True},
                "projects": {"enabled": True},
                "certifications": {"enabled": False},
                "languages": {"enabled": True},
            },
        },
    },
]


class AdminMarketplaceTemplatesView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        return Response({"results": MARKETPLACE_TEMPLATES})


class AdminTemplateImportView(APIView):
    """
    ✅ CLONE & FREEZE
    - marketplace_key OR direct payload
    - preview_image_url download karke OUR storage me save
    - schema ko OUR DB me save
    """
    permission_classes = [IsAdminUser]

    def post(self, request):
        key = request.data.get("marketplace_key")

        if key:
            tpl = next((x for x in MARKETPLACE_TEMPLATES if x["key"] == key), None)
            if not tpl:
                return Response({"detail": "Invalid marketplace_key"}, status=400)

            name = tpl["name"]
            category = tpl["category"]
            layout = tpl["layout"]
            color = tpl.get("color", "#2563eb")
            schema = tpl.get("schema", {})
            preview_url = tpl.get("preview_image_url", "")
        else:
            # direct import support
            name = request.data.get("name")
            category = request.data.get("category", "Modern")
            layout = request.data.get("layout", "Two Column")
            color = request.data.get("color", "#2563eb")
            schema = request.data.get("schema", {})
            preview_url = request.data.get("preview_image_url", "")

            if not name:
                return Response({"detail": "name is required"}, status=400)

        # unique naming fallback
        base_name = name
        i = 1
        while ResumeTemplate.objects.filter(name=name).exists():
            i += 1
            name = f"{base_name} ({i})"

        obj = ResumeTemplate.objects.create(
            name=name,
            category=category,
            layout=layout,
            status="draft",
            color=color,
            source="imported",
            schema=schema,
        )

        # download preview -> save locally (freeze)
        if preview_url:
            try:
                r = requests.get(preview_url, timeout=10)
                r.raise_for_status()
                fname = f"{slugify(obj.name)}.png"
                obj.preview_image.save(fname, ContentFile(r.content), save=True)
            except Exception:
                # preview fail should NOT break import
                pass

        return Response(ResumeTemplateSerializer(obj).data, status=status.HTTP_201_CREATED)


class AdminTemplateDuplicateView(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, pk: int):
        src = ResumeTemplate.objects.filter(pk=pk).first()
        if not src:
            return Response({"detail": "Template not found"}, status=404)

        new_name = request.data.get("name") or f"{src.name} Copy"
        base_name = new_name
        i = 1
        while ResumeTemplate.objects.filter(name=new_name).exists():
            i += 1
            new_name = f"{base_name} ({i})"

        dup = ResumeTemplate.objects.create(
            name=new_name,
            category=src.category,
            layout=src.layout,
            status="draft",
            color=src.color,
            source="duplicated",
            description=src.description,
            schema=src.schema,
        )

        # copy preview file as OUR asset
        if src.preview_image:
            try:
                src.preview_image.open("rb")
                content = src.preview_image.read()
                dup.preview_image.save(f"{slugify(dup.name)}.png", ContentFile(content), save=True)
            except Exception:
                pass

        return Response(ResumeTemplateSerializer(dup).data, status=201)


# views.py mein yeh imports add karo
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from django.db.models import Q
from .models import Resume
from .serializers import ResumeSerializer

# Student APIs for templates and resumes

# # ✅ Student Templates List (only active templates)
# class StudentTemplateListView(generics.ListAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = ResumeTemplateSerializer
    
#     def get_queryset(self):
#         return ResumeTemplate.objects.filter(status="active").order_by('name')

# # ✅ Student Resumes List/Create
# class StudentResumeListCreateView(generics.ListCreateAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = ResumeSerializer
    
#     def get_queryset(self):
#         return Resume.objects.filter(user=self.request.user).order_by('-updated_at')
    
#     def perform_create(self, serializer):
#         template = serializer.validated_data.get('template')
#         # Create default empty resume data
#         default_data = {
#             "header": {
#                 "fullName": "",
#                 "jobTitle": "",
#                 "email": "",
#                 "phone": "",
#                 "location": "",
#                 "linkedin": "",
#                 "website": ""
#             },
#             "summary": "",
#             "experience": [{"title": "", "company": "", "location": "", "from": "", "to": "", "bullets": [""]}],
#             "education": [{"school": "", "degree": "", "from": "", "to": ""}],
#             "skills": {"programming": [], "frameworks": [], "tools": []},
#             "projects": [{"name": "", "desc": ""}]
#         }
        
#         resume = serializer.save(
#             user=self.request.user,
#             data=default_data,
#             status="draft"
#         )
#         return resume

# # ✅ Student Resume Detail/Update/Delete
# class StudentResumeDetailView(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = ResumeSerializer
    
#     def get_queryset(self):
#         return Resume.objects.filter(user=self.request.user)



# views.py mein yeh APIs add karo
# Student Template Detail View
# class StudentTemplateDetailView(APIView):
#     permission_classes = [IsAuthenticated]
    
#     def get(self, request, pk):
#         try:
#             template = ResumeTemplate.objects.get(id=pk, status="active")
#             serializer = ResumeTemplateSerializer(template)
#             return Response(serializer.data)
#         except ResumeTemplate.DoesNotExist:
#             return Response({"detail": "Template not found or not active"}, status=404)

# Student Resume Update View
class StudentResumeUpdateView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ResumeSerializer
    
    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)
    
    def perform_update(self, serializer):
        serializer.save()

# views.py (replace your current StudentResumeDetailView with this)

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from .models import Resume
from .serializers import ResumeSerializer

# class StudentResumeDetailView(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = ResumeSerializer

#     def get_queryset(self):
#         # ✅ user can only access own resumes
#         return Resume.objects.filter(user=self.request.user)


# # ✅ Student Dashboard Stats
# class StudentDashboardStatsView(APIView):
#     permission_classes = [IsAuthenticated]
    
#     def get(self, request):
#         user = request.user
#         resumes = Resume.objects.filter(user=user)
        
#         stats = {
#             "totalResumes": resumes.count(),
#             "completed": resumes.filter(status="completed").count(),
#             "inProgress": resumes.filter(status__in=["draft", "in_progress"]).count(),
#             "downloads": resumes.aggregate(total=Sum('download_count'))['total'] or 0
#         }
        
#         return Response(stats)

# # ✅ Student Resume Download Tracking
# from django.utils import timezone
# from django.db.models import Sum
# from django.utils import timezone

# class StudentResumeDownloadView(APIView):
#     permission_classes = [IsAuthenticated]
    
#     def post(self, request, resume_id):
#         try:
#             resume = Resume.objects.get(id=resume_id, user=request.user)
#             resume.download_count += 1
#             resume.last_downloaded = timezone.now()
#             resume.save()
            
#             # Increment template downloads count too
#             if resume.template:
#                 resume.template.downloads += 1
#                 resume.template.save()
            
#             return Response({
#                 "message": "Download tracked successfully",
#                 "download_count": resume.download_count
#             })
#         except Resume.DoesNotExist:
#             return Response({"error": "Resume not found"}, status=404)

# views.py (important resume views)

from django.db.models import Sum
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Resume, ResumeTemplate
from .serializers import ResumeSerializer, ResumeTemplateSerializer


# ✅ STUDENT: Templates list
class StudentTemplateListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ResumeTemplateSerializer

    def get_queryset(self):
        return ResumeTemplate.objects.filter(status="active").order_by("name")


# ✅ STUDENT: Template detail
class StudentTemplateDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            template = ResumeTemplate.objects.get(id=pk, status="active")
            serializer = ResumeTemplateSerializer(template, context={"request": request})
            return Response(serializer.data)
        except ResumeTemplate.DoesNotExist:
            return Response({"detail": "Template not found or not active"}, status=404)


# ✅ STUDENT: Resume list + create
class StudentResumeListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ResumeSerializer

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user).order_by("-updated_at")

    def perform_create(self, serializer):
        default_data = {
            "header": {"fullName": "", "jobTitle": "", "email": "", "phone": "", "location": "", "linkedin": "", "website": ""},
            "summary": "",
            "experience": [{"title": "", "company": "", "location": "", "from": "", "to": "", "bullets": [""]}],
            "education": [{"school": "", "degree": "", "from": "", "to": ""}],
            "skills": {"programming": [], "frameworks": [], "tools": []},
            "projects": [{"name": "", "desc": ""}],
        }
        serializer.save(user=self.request.user, data=serializer.validated_data.get("data") or default_data, status="draft")


# ✅ STUDENT: Resume detail/update/delete  (FIXED)
class StudentResumeDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ResumeSerializer

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)


# ✅ STUDENT: Dashboard stats
class StudentDashboardStatsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        resumes = Resume.objects.filter(user=request.user)
        return Response({
            "totalResumes": resumes.count(),
            "completed": resumes.filter(status="completed").count(),
            "inProgress": resumes.filter(status__in=["draft", "in_progress"]).count(),
            "downloads": resumes.aggregate(total=Sum("download_count"))["total"] or 0,
        })


# ✅ STUDENT: Download tracking
class StudentResumeDownloadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, resume_id):
        try:
            resume = Resume.objects.get(id=resume_id, user=request.user)
            resume.download_count = (resume.download_count or 0) + 1
            resume.last_downloaded = timezone.now()
            resume.save()

            if resume.template:
                resume.template.downloads = (resume.template.downloads or 0) + 1
                resume.template.save()

            return Response({"message": "Download tracked", "download_count": resume.download_count})
        except Resume.DoesNotExist:
            return Response({"error": "Resume not found"}, status=404)


# ✅ ADMIN: Resume list/create (NEW - fixes 404)
class AdminResumeListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = ResumeSerializer

    def get_queryset(self):
        return Resume.objects.all().order_by("-updated_at")

    def perform_create(self, serializer):
        # admin resume saved under admin user account (for testing templates)
        serializer.save(user=self.request.user, status=serializer.validated_data.get("status") or "draft")


# ✅ ADMIN: Resume detail/update/delete (NEW)
class AdminResumeDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = ResumeSerializer
    queryset = Resume.objects.all()
# views.py
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import StudentRegisterSerializer, StudentLoginSerializer
from .models import User


class StudentRegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = StudentRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "action": "registered",
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "id": user.id,
                    "phone": user.phone,
                    "name": user.name,
                    "email": user.email or "",
                    "pincode": user.pincode,
                },
            },
            status=status.HTTP_201_CREATED,
        )


class StudentLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = StudentLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)
        return Response(
            {
                "action": "logged_in",
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "id": user.id,
                    "phone": user.phone,
                    "name": user.name,
                    "email": user.email or "",
                    "pincode": user.pincode,
                },
            }
        )


# users/views.py
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import User
from .serializers import ForgotPasswordSerializer, ResetPasswordSerializer


class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]

        # ✅ Do not reveal whether email exists (security)
        user = User.objects.filter(email__iexact=email, is_staff=False, is_active=True).first()

        if user:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            frontend = getattr(settings, "FRONTEND_URL", "http://localhost:5173").rstrip("/")
            reset_link = f"{frontend}/reset-password?uid={uid}&token={token}"

            subject = "Reset your password"
            text_body = (
                f"Hi {user.name or 'User'},\n\n"
                f"You requested a password reset.\n"
                f"Open this link to set a new password:\n{reset_link}\n\n"
                f"If you did not request this, you can ignore this email.\n"
            )

            msg = EmailMultiAlternatives(
                subject=subject,
                body=text_body,
                from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
                to=[user.email],
            )
            msg.send(fail_silently=False)

        return Response(
            {"message": "If this email is registered, a reset link has been sent."},
            status=status.HTTP_200_OK,
        )


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        password = serializer.validated_data["password"]

        user.set_password(password)
        user.save()

        return Response({"message": "Password reset successful. Please login now."}, status=200)


# users/views.py
from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import User
from .serializers import AdminForgotPasswordSerializer, AdminResetPasswordSerializer


class AdminForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AdminForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]

        # ✅ only admin users
        user = User.objects.filter(email__iexact=email, is_staff=True, is_active=True).first()

        if user and user.email:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            frontend = getattr(settings, "FRONTEND_URL", "http://localhost:5173").rstrip("/")
            reset_link = f"{frontend}/admin/reset-password?uid={uid}&token={token}"

            subject = "Admin password reset"
            text_body = (
                f"Hi {user.name or 'Admin'},\n\n"
                f"You requested an admin password reset.\n"
                f"Open this link to set a new password:\n{reset_link}\n\n"
                f"If you did not request this, ignore this email.\n"
            )

            # ✅ IMPORTANT: avoid empty from_email
            from_email = getattr(settings, "DEFAULT_FROM_EMAIL", None) or None

            msg = EmailMultiAlternatives(
                subject=subject,
                body=text_body,
                from_email=from_email,
                to=[user.email],
            )
            msg.send(fail_silently=False)

        # ✅ same response always (security)
        return Response(
            {"message": "If this email is registered, a reset link has been sent."},
            status=status.HTTP_200_OK,
        )


class AdminResetPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AdminResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        password = serializer.validated_data["password"]

        user.set_password(password)
        user.save()

        return Response({"message": "Admin password reset successful. Please login now."}, status=200)


# users/views.py
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from .models import User
from .serializers import AdminUserSerializer

# class AdminStaffListCreateView(generics.ListCreateAPIView):
#     permission_classes = [IsAdminUser]
#     serializer_class = AdminUserSerializer

#     def get_queryset(self):
#         return User.objects.filter(is_staff=True).order_by("-date_joined")


# class AdminStaffDetailView(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [IsAdminUser]
#     serializer_class = AdminUserSerializer

#     def get_queryset(self):
#         return User.objects.filter(is_staff=True)

# users/views.py
from rest_framework import generics
from rest_framework.permissions import IsAdminUser
from .models import User
from .serializers import AdminUserSerializer


class AdminStaffListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = AdminUserSerializer

    def get_queryset(self):
        return User.objects.filter(is_staff=True).order_by("-date_joined")


class AdminStaffDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = AdminUserSerializer

    def get_queryset(self):
        return User.objects.filter(is_staff=True)
