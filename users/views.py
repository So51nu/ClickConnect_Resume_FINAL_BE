# # # from rest_framework.views import APIView
# # # from rest_framework.response import Response
# # # from rest_framework.permissions import AllowAny, IsAdminUser
# # # from rest_framework import status
# # # from rest_framework_simplejwt.tokens import RefreshToken
# # # from django.contrib.auth import authenticate

# # # from .models import User, OTP
# # # from .serializers import UserSerializer
# # # import random


# # # # ================== SEND OTP ==================

# # # class SendOTPView(APIView):
# # #     permission_classes = [AllowAny]

# # #     def post(self, request):
# # #         phone = request.data.get("phone")

# # #         if not phone:
# # #             return Response({"message": "Phone required"}, status=400)

# # #         otp_code = str(random.randint(100000, 999999))
# # #         OTP.objects.create(phone=phone, code=otp_code)

# # #         print("OTP (DEV):", otp_code)

# # #         return Response({
# # #             "is_registered": User.objects.filter(phone=phone).exists()
# # #         })


# # # # ================== VERIFY OTP ==================
# # # from django.utils import timezone
# # # from rest_framework.views import APIView
# # # from rest_framework.response import Response
# # # from rest_framework.permissions import AllowAny
# # # from rest_framework_simplejwt.tokens import RefreshToken
# # # from .models import User, OTP

# # # from .models import User, OTP
# # # from .serializers import UserSerializer
# # # import random


# # # # ================== SEND OTP ==================
# # # class VerifyOTPView(APIView):
# # #     permission_classes = [AllowAny]

# # #     def post(self, request):
# # #         phone = request.data.get("phone")
# # #         otp = request.data.get("otp")

# # #         if not phone or not otp:
# # #             return Response({"message": "Phone and OTP are required"}, status=400)

# # #         otp_obj = OTP.objects.filter(phone=phone, code=otp).last()
# # #         if not otp_obj or not otp_obj.is_valid():
# # #             return Response({"message": "Invalid OTP"}, status=400)

# # #         user = User.objects.filter(phone=phone).first()

# # #         # 🔹 AUTO DECIDE: REGISTER or LOGIN
# # #         if not user:
# # #             user = User.objects.create(
# # #                 phone=phone,
# # #                 name=request.data.get("name", ""),
# # #                 email=request.data.get("email", ""),
# # #                 pincode=request.data.get("pincode", ""),
# # #             )
# # #             action = "registered"
# # #         else:
# # #             action = "logged_in"

# # #         otp_obj.delete()

# # #         refresh = RefreshToken.for_user(user)

# # #         return Response({
# # #             "action": action,
# # #             "access": str(refresh.access_token),
# # #             "refresh": str(refresh),
# # #             "user": {
# # #                 "phone": user.phone,
# # #                 "name": user.name,
# # #                 "email": user.email,
# # #                 "pincode": user.pincode,
# # #             }
# # #         })

# # # # ================== ADMIN LOGIN ==================

# # # class AdminLoginView(APIView):
# # #     permission_classes = [AllowAny]

# # #     def post(self, request):
# # #         phone = request.data.get("phone")
# # #         password = request.data.get("password")

# # #         user = authenticate(phone=phone, password=password)

# # #         if not user or not user.is_staff:
# # #             return Response(
# # #                 {"error": "Invalid admin credentials"},
# # #                 status=status.HTTP_401_UNAUTHORIZED
# # #             )

# # #         refresh = RefreshToken.for_user(user)

# # #         return Response({
# # #             "access": str(refresh.access_token),
# # #             "refresh": str(refresh),
# # #             "user": {
# # #                 "id": user.id,
# # #                 "phone": user.phone,
# # #                 "name": user.name,
# # #                 "role": "admin",
# # #             }
# # #         })


# # # # ================== ADMIN USER LIST ==================

# # # class AdminUserListView(APIView):
# # #     permission_classes = [IsAdminUser]

# # #     def get(self, request):
# # #         users = User.objects.filter(is_staff=False).order_by("-date_joined")
# # #         serializer = UserSerializer(users, many=True)
# # #         return Response(serializer.data)


# # # # ================== ADMIN USER DETAIL ==================

# # # class AdminUserDetailView(APIView):
# # #     permission_classes = [IsAdminUser]

# # #     def delete(self, request, pk):
# # #         try:
# # #             user = User.objects.get(pk=pk, is_staff=False)
# # #             user.delete()
# # #             return Response({"message": "User deleted"})
# # #         except User.DoesNotExist:
# # #             return Response({"error": "User not found"}, status=404)
# # # views.py
# # import random
# # from django.contrib.auth import authenticate
# # from rest_framework import status
# # from rest_framework.permissions import AllowAny, IsAdminUser
# # from rest_framework.response import Response
# # from rest_framework.views import APIView
# # from rest_framework_simplejwt.tokens import RefreshToken

# # from .models import User, OTP
# # from .serializers import UserSerializer


# # # ================== SEND OTP ==================
# # class SendOTPView(APIView):
# #     permission_classes = [AllowAny]

# #     def post(self, request):
# #         phone = request.data.get("phone")
# #         if not phone:
# #             return Response({"message": "Phone required"}, status=400)

# #         otp_code = str(random.randint(100000, 999999))
# #         OTP.objects.create(phone=phone, code=otp_code)

# #         # DEV only
# #         print("OTP (DEV):", otp_code)

# #         return Response({"is_registered": User.objects.filter(phone=phone).exists()})


# # # ================== VERIFY OTP ==================
# # class VerifyOTPView(APIView):
# #     permission_classes = [AllowAny]

# #     def post(self, request):
# #         phone = request.data.get("phone")
# #         # support both "otp" and "code" from frontend
# #         otp_value = request.data.get("otp") or request.data.get("code")

# #         if not phone or not otp_value:
# #             return Response({"message": "Phone and OTP are required"}, status=400)

# #         otp_obj = OTP.objects.filter(phone=phone, code=otp_value).last()
# #         if not otp_obj or not otp_obj.is_valid():
# #             return Response({"message": "Invalid OTP"}, status=400)

# #         user = User.objects.filter(phone=phone).first()

# #         if not user:
# #             user = User.objects.create(
# #                 phone=phone,
# #                 name=request.data.get("name", ""),
# #                 email=request.data.get("email", ""),
# #                 pincode=request.data.get("pincode", ""),
# #                 is_staff=False,
# #             )
# #             user.set_unusable_password()
# #             user.save()
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
# #                 "id": user.id,
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
# #             return Response({"error": "Invalid admin credentials"}, status=status.HTTP_401_UNAUTHORIZED)

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


# # # ================== ADMIN USER LIST (GET + POST) ==================
# # class AdminUserListView(APIView):
# #     permission_classes = [IsAdminUser]

# #     def get(self, request):
# #         users = User.objects.filter(is_staff=False).order_by("-date_joined")
# #         serializer = UserSerializer(users, many=True)
# #         return Response(serializer.data)

# #     def post(self, request):
# #         # create student/user
# #         serializer = UserSerializer(data=request.data)
# #         if serializer.is_valid():
# #             user = serializer.save(is_staff=False)
# #             return Response(UserSerializer(user).data, status=201)
# #         return Response(serializer.errors, status=400)


# # # ================== ADMIN USER DETAIL (GET + PATCH/PUT + DELETE) ==================
# # class AdminUserDetailView(APIView):
# #     permission_classes = [IsAdminUser]

# #     def get(self, request, pk):
# #         try:
# #             user = User.objects.get(pk=pk, is_staff=False)
# #             return Response(UserSerializer(user).data)
# #         except User.DoesNotExist:
# #             return Response({"error": "User not found"}, status=404)

# #     def patch(self, request, pk):
# #         try:
# #             user = User.objects.get(pk=pk, is_staff=False)
# #             serializer = UserSerializer(user, data=request.data, partial=True)
# #             if serializer.is_valid():
# #                 serializer.save()
# #                 return Response(serializer.data)
# #             return Response(serializer.errors, status=400)
# #         except User.DoesNotExist:
# #             return Response({"error": "User not found"}, status=404)

# #     def put(self, request, pk):
# #         # full update
# #         try:
# #             user = User.objects.get(pk=pk, is_staff=False)
# #             serializer = UserSerializer(user, data=request.data, partial=False)
# #             if serializer.is_valid():
# #                 serializer.save()
# #                 return Response(serializer.data)
# #             return Response(serializer.errors, status=400)
# #         except User.DoesNotExist:
# #             return Response({"error": "User not found"}, status=404)

# #     def delete(self, request, pk):
# #         try:
# #             user = User.objects.get(pk=pk, is_staff=False)
# #             user.delete()
# #             return Response({"message": "User deleted"})
# #         except User.DoesNotExist:
# #             return Response({"error": "User not found"}, status=404)

# import random
# from django.contrib.auth import authenticate
# from rest_framework import status
# from rest_framework.permissions import AllowAny, IsAdminUser
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework import generics

# from .models import User, OTP, ResumeTemplate, TemplatePricing
# from .serializers import (
#     UserSerializer,
#     ResumeTemplateSerializer,
#     TemplatePricingSerializer,
# )


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
#         return Response(
#             {
#                 "action": action,
#                 "access": str(refresh.access_token),
#                 "refresh": str(refresh),
#                 "user": {
#                     "id": user.id,
#                     "phone": user.phone,
#                     "name": user.name,
#                     "email": user.email,
#                     "pincode": user.pincode,
#                 },
#             }
#         )


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
# #                 status=status.HTTP_401_UNAUTHORIZED,
# #             )

# #         refresh = RefreshToken.for_user(user)
# #         return Response(
# #             {
# #                 "access": str(refresh.access_token),
# #                 "refresh": str(refresh),
# #                 "user": {"id": user.id, "phone": user.phone, "name": user.name, "role": "admin"},
# #             }
# #         )
# # views.py
# from django.contrib.auth import authenticate
# from rest_framework.permissions import AllowAny
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework import status
# from rest_framework_simplejwt.tokens import RefreshToken


# class AdminLoginView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         phone = request.data.get("phone")
#         password = request.data.get("password")

#         if not phone or not password:
#             return Response(
#                 {"detail": "Phone and password are required"},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         user = authenticate(phone=phone, password=password)
#         if not user or not user.is_staff:
#             return Response(
#                 {"detail": "Invalid admin credentials"},
#                 status=status.HTTP_401_UNAUTHORIZED,
#             )

#         refresh = RefreshToken.for_user(user)

#         # ✅ return admin_* keys (frontend will store in admin_access/admin_refresh/admin)
#         return Response(
#             {
#                 "action": "logged_in",
#                 "admin_access": str(refresh.access_token),
#                 "admin_refresh": str(refresh),
#                 "admin": {
#                     "id": user.id,
#                     "phone": user.phone,
#                     "name": user.name,
#                     "email": user.email or "",
#                     "role": "admin",
#                 },
#             }
#         )


# # ================== ADMIN USERS (CRUD) ==================
# class AdminUserListView(APIView):
#     permission_classes = [IsAdminUser]

#     def get(self, request):
#         users = User.objects.filter(is_staff=False).order_by("-date_joined")
#         return Response(UserSerializer(users, many=True).data)

#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save(is_staff=False)
#             return Response(UserSerializer(user).data, status=201)
#         return Response(serializer.errors, status=400)


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


# # =========================
# # ✅ NEW: Admin Templates APIs
# # =========================

# class AdminTemplateListCreateView(generics.ListCreateAPIView):
#     permission_classes = [IsAdminUser]
#     queryset = ResumeTemplate.objects.all().order_by("-updated_at")
#     serializer_class = ResumeTemplateSerializer


# class AdminTemplateDetailView(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [IsAdminUser]
#     queryset = ResumeTemplate.objects.all()
#     serializer_class = ResumeTemplateSerializer


# # =========================
# # ✅ NEW: Admin Template Pricing APIs
# # =========================

# class AdminTemplatePricingListCreateView(generics.ListCreateAPIView):
#     permission_classes = [IsAdminUser]
#     queryset = TemplatePricing.objects.select_related("template").all().order_by("-updated_at")
#     serializer_class = TemplatePricingSerializer


# class AdminTemplatePricingDetailView(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [IsAdminUser]
#     queryset = TemplatePricing.objects.select_related("template").all()
#     serializer_class = TemplatePricingSerializer

# # views.py (subscription section ko replace/add karo)
# from django.db.models import Sum, Q
# from rest_framework.permissions import IsAdminUser
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework import status

# from .models import Subscription
# from .serializers import SubscriptionSerializer


# class AdminSubscriptionListView(APIView):
#     permission_classes = [IsAdminUser]

#     def get(self, request):
#         qs = Subscription.objects.select_related("user").order_by("-created_at")

#         plan = request.GET.get("plan")
#         st = request.GET.get("status")
#         search = request.GET.get("search")

#         if plan:
#             qs = qs.filter(plan=plan)
#         if st:
#             qs = qs.filter(status=st)

#         if search:
#             search = search.strip()
#             qs = qs.filter(
#                 Q(user__name__icontains=search)
#                 | Q(user__email__icontains=search)
#                 | Q(user__phone__icontains=search)
#             )

#         serializer = SubscriptionSerializer(qs, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = SubscriptionSerializer(data=request.data)
#         if serializer.is_valid():
#             sub = serializer.save()
#             return Response(SubscriptionSerializer(sub).data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class AdminSubscriptionDetailView(APIView):
#     permission_classes = [IsAdminUser]

#     def get_object(self, pk):
#         return Subscription.objects.select_related("user").get(pk=pk)

#     def get(self, request, pk):
#         try:
#             sub = self.get_object(pk)
#             return Response(SubscriptionSerializer(sub).data)
#         except Subscription.DoesNotExist:
#             return Response({"error": "Subscription not found"}, status=404)

#     def patch(self, request, pk):
#         try:
#             sub = self.get_object(pk)
#             serializer = SubscriptionSerializer(sub, data=request.data, partial=True)
#             if serializer.is_valid():
#                 sub = serializer.save()
#                 return Response(SubscriptionSerializer(sub).data)
#             return Response(serializer.errors, status=400)
#         except Subscription.DoesNotExist:
#             return Response({"error": "Subscription not found"}, status=404)

#     def put(self, request, pk):
#         try:
#             sub = self.get_object(pk)
#             serializer = SubscriptionSerializer(sub, data=request.data, partial=False)
#             if serializer.is_valid():
#                 sub = serializer.save()
#                 return Response(SubscriptionSerializer(sub).data)
#             return Response(serializer.errors, status=400)
#         except Subscription.DoesNotExist:
#             return Response({"error": "Subscription not found"}, status=404)

#     def delete(self, request, pk):
#         try:
#             sub = self.get_object(pk)
#             sub.delete()
#             return Response({"message": "Subscription deleted"})
#         except Subscription.DoesNotExist:
#             return Response({"error": "Subscription not found"}, status=404)


# class AdminSubscriptionStatsView(APIView):
#     permission_classes = [IsAdminUser]

#     def get(self, request):
#         total = Subscription.objects.count()
#         active = Subscription.objects.filter(status="Active").count()

#         revenue = Subscription.objects.filter(status="Active").aggregate(total=Sum("amount"))["total"] or 0

#         churn = 0
#         if total:
#             churn = round((Subscription.objects.filter(status="Cancelled").count() / total) * 100, 2)

#         return Response({
#             "total": total,
#             "active": active,
#             "revenue": revenue,
#             "churn": churn,
#         })

# # views.py (add below your existing template views)
# from rest_framework import generics, status
# from rest_framework.permissions import IsAdminUser
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from django.utils.text import slugify
# from django.core.files.base import ContentFile

# import json
# import requests

# from .models import ResumeTemplate
# from .serializers import ResumeTemplateSerializer
# # ------------------------------
# # ✅ Schema Normalizer (BACKEND)
# # ------------------------------

# def normalize_template_schema(schema: dict) -> dict:
#     """
#     ✅ Backward compatible normalizer:
#     - old schemas (no type) => auto add type/dataKey
#     - new schemas (already type based) => keep as is
#     """
#     if not isinstance(schema, dict):
#         return {}

#     s = dict(schema)  # shallow copy
#     s.setdefault("version", 1)
#     s.setdefault("layout", "Single Column")
#     s.setdefault("theme", {})
#     s.setdefault("order", [])
#     s.setdefault("columns", {"left": [], "right": []})
#     s.setdefault("sections", {})

#     sections = s.get("sections") or {}
#     if not isinstance(sections, dict):
#         sections = {}
#     # helper to set defaults
#     def ensure_section(id_, default_type, default_key=None):
#         cfg = sections.get(id_) or {}
#         if not isinstance(cfg, dict):
#             cfg = {}
#         cfg.setdefault("enabled", True)

#         # if already type is present => don't override
#         if "type" not in cfg:
#             cfg["type"] = default_type
#         if default_key and "dataKey" not in cfg:
#             cfg["dataKey"] = default_key
#         sections[id_] = cfg

#     # ✅ default mapping (old templates auto work)
#     ensure_section("header", "header", "header")
#     ensure_section("summary", "text", "summary")
#     ensure_section("experience", "timeline", "experience")
#     ensure_section("education", "timeline", "education")
#     ensure_section("projects", "timeline", "projects")
#     ensure_section("skills", "skills", "skills")
#     ensure_section("certifications", "list", "certifications")

#     # languages: if schema says display=dots then frontend will show dots
#     ensure_section("languages", "languages", "languages")

#     # optional sections (if exists in schema, set types)
#     if "courses" in sections:
#         ensure_section("courses", "list", "courses")
#     if "achievements" in sections:
#         ensure_section("achievements", "grid", "achievements")
#     if "strengths" in sections:
#         ensure_section("strengths", "grid", "strengths")
#     if "contacts" in sections:
#         ensure_section("contacts", "contacts", "header")  # contacts reads header
#     if "interests" in sections:
#         ensure_section("interests", "list", "interests")
#     if "sidebarProfile" in sections:
#         ensure_section("sidebarProfile", "avatar", "header")

#     # ✅ also, if new templates add random sections without type
#     # we auto guess:
#     for sec_id, cfg in list(sections.items()):
#         if not isinstance(cfg, dict):
#             continue
#         if "type" in cfg:
#             continue
#         # guess by name
#         if sec_id in ("experience", "education", "projects"):
#             cfg["type"] = "timeline"
#             cfg.setdefault("dataKey", sec_id)
#         elif sec_id in ("summary", "objective"):
#             cfg["type"] = "text"
#             cfg.setdefault("dataKey", sec_id)
#         elif sec_id in ("languages",):
#             cfg["type"] = "languages"
#             cfg.setdefault("dataKey", sec_id)
#         else:
#             # fallback
#             cfg["type"] = "list"
#             cfg.setdefault("dataKey", sec_id)
#         sections[sec_id] = cfg

#     s["sections"] = sections
#     return s


# def normalize_marketplace_template(tpl: dict) -> dict:
#     """
#     normalize single template dict in MARKETPLACE_TEMPLATES
#     """
#     if not isinstance(tpl, dict):
#         return {}
#     out = dict(tpl)
#     out["schema"] = normalize_template_schema(out.get("schema") or {})
#     return out


# def normalized_marketplace_templates(raw_list: list) -> list:
#     if not isinstance(raw_list, list):
#         return []
#     return [normalize_marketplace_template(x) for x in raw_list]

# # ✅ Marketplace templates (FREE) - yahan aap easily add/remove kar sakte ho
# MARKETPLACE_TEMPLATES = [
#     {
#         "key": "simple-01",
#         "name": "Simple 01",
#         "category": "Classic",
#         "layout": "Single Column",
#         "color": "#111827",
#         "price_type": "free",
#         "price": 0,
#         "preview_image_url": "",  # optionally put CDN/static url
#         "schema": {
#             "version": 1,
#             "layout": "Single Column",
#             "theme": {
#                 "primary": "#111827",
#                 "fontFamily": "Georgia, 'Times New Roman', Times, serif",
#                 "headingUppercase": True,
#                 "titleSize": 12,
#                 "bodySize": 10,
#                 "lineHeight": 1.4,
#             },
#             "order": ["header", "summary", "experience", "education", "skills", "projects"],
#             "columns": {"left": [], "right": []},
#             "sections": {
#                 "header": {"enabled": True},
#                 "summary": {"enabled": True},
#                 "experience": {"enabled": True},
#                 "education": {"enabled": True},
#                 "skills": {"enabled": True},
#                 "projects": {"enabled": True},
#                 "certifications": {"enabled": False},
#                 "languages": {"enabled": False},
#             },
#         },
#     },
#     {
#         "key": "modern-02",
#         "name": "Modern 02",
#         "category": "Modern",
#         "layout": "Two Column",
#         "color": "#2563eb",
#         "price_type": "free",
#         "price": 0,
#         "preview_image_url": "",
#         "schema": {
#             "version": 1,
#             "layout": "Two Column",
#             "theme": {
#                 "primary": "#2563eb",
#                 "fontFamily": "system-ui, -apple-system, Segoe UI, Roboto, sans-serif",
#                 "headingUppercase": True,
#                 "titleSize": 12,
#                 "bodySize": 10,
#                 "lineHeight": 1.35,
#             },
#             "columns": {"left": ["summary", "skills", "education"], "right": ["header", "experience", "projects"]},
#             "order": [],
#             "sections": {
#                 "header": {"enabled": True},
#                 "summary": {"enabled": True},
#                 "experience": {"enabled": True},
#                 "education": {"enabled": True},
#                 "skills": {"enabled": True},
#                 "projects": {"enabled": True},
#                 "certifications": {"enabled": False},
#                 "languages": {"enabled": False},
#             },
#         },
#     },
#     {
#         "key": "nexus-03",
#         "name": "Nexus 03",
#         "category": "Modern",
#         "layout": "Sidebar Left",
#         "color": "#0b4a6f",
#         "price_type": "free",
#         "price": 0,
#         "preview_image_url": "",
#         "schema": {
#             "version": 1,
#             "layout": "Sidebar Left",
#             "theme": {
#                 "primary": "#0b4a6f",
#                 "fontFamily": "system-ui, -apple-system, Segoe UI, Roboto, sans-serif",
#                 "headingUppercase": True,
#                 "titleSize": 12,
#                 "bodySize": 10,
#                 "lineHeight": 1.35,
#             },
#             "columns": {"left": ["skills", "education", "languages"], "right": ["header", "summary", "experience", "projects"]},
#             "order": [],
#             "sections": {
#                 "header": {"enabled": True},
#                 "summary": {"enabled": True},
#                 "experience": {"enabled": True},
#                 "education": {"enabled": True},
#                 "skills": {"enabled": True},
#                 "projects": {"enabled": True},
#                 "certifications": {"enabled": False},
#                 "languages": {"enabled": True},
#             },
#         },
#     },
   



# ]


# class AdminMarketplaceTemplatesView(APIView):
#     permission_classes = [IsAdminUser]

#     def get(self, request):
#         return Response({"results": normalized_marketplace_templates(MARKETPLACE_TEMPLATES)})


# class AdminTemplateImportView(APIView):
#     """
#     ✅ CLONE & FREEZE
#     - marketplace_key OR direct payload
#     - preview_image_url download karke OUR storage me save
#     - schema ko OUR DB me save
#     """
#     permission_classes = [IsAdminUser]

#     def post(self, request):
#         key = request.data.get("marketplace_key")

#         if key:
#             tpl = next((x for x in MARKETPLACE_TEMPLATES if x["key"] == key), None)
#             if not tpl:
#                 return Response({"detail": "Invalid marketplace_key"}, status=400)

#             name = tpl["name"]
#             category = tpl["category"]
#             layout = tpl["layout"]
#             color = tpl.get("color", "#2563eb")
#             schema = tpl.get("schema", {})
            
#             schema = normalize_template_schema(schema)
#             preview_url = tpl.get("preview_image_url", "")
#         else:
#             # direct import support
#             name = request.data.get("name")
#             category = request.data.get("category", "Modern")
#             layout = request.data.get("layout", "Two Column")
#             color = request.data.get("color", "#2563eb")
#             schema = request.data.get("schema", {})
            
#             schema = normalize_template_schema(schema)
#             preview_url = request.data.get("preview_image_url", "")

#             if not name:
#                 return Response({"detail": "name is required"}, status=400)

#         # unique naming fallback
#         base_name = name
#         i = 1
#         while ResumeTemplate.objects.filter(name=name).exists():
#             i += 1
#             name = f"{base_name} ({i})"

#         obj = ResumeTemplate.objects.create(
#             name=name,
#             category=category,
#             layout=layout,
#             status="draft",
#             color=color,
#             source="imported",
#             schema=schema,
#         )

#         # download preview -> save locally (freeze)
#         if preview_url:
#             try:
#                 r = requests.get(preview_url, timeout=10)
#                 r.raise_for_status()
#                 fname = f"{slugify(obj.name)}.png"
#                 obj.preview_image.save(fname, ContentFile(r.content), save=True)
#             except Exception:
#                 # preview fail should NOT break import
#                 pass

#         return Response(ResumeTemplateSerializer(obj).data, status=status.HTTP_201_CREATED)


# class AdminTemplateDuplicateView(APIView):
#     permission_classes = [IsAdminUser]

#     def post(self, request, pk: int):
#         src = ResumeTemplate.objects.filter(pk=pk).first()
#         if not src:
#             return Response({"detail": "Template not found"}, status=404)

#         new_name = request.data.get("name") or f"{src.name} Copy"
#         base_name = new_name
#         i = 1
#         while ResumeTemplate.objects.filter(name=new_name).exists():
#             i += 1
#             new_name = f"{base_name} ({i})"

#         dup = ResumeTemplate.objects.create(
#             name=new_name,
#             category=src.category,
#             layout=src.layout,
#             status="draft",
#             color=src.color,
#             source="duplicated",
#             description=src.description,
#             schema=src.schema,
#         )

#         # copy preview file as OUR asset
#         if src.preview_image:
#             try:
#                 src.preview_image.open("rb")
#                 content = src.preview_image.read()
#                 dup.preview_image.save(f"{slugify(dup.name)}.png", ContentFile(content), save=True)
#             except Exception:
#                 pass

#         return Response(ResumeTemplateSerializer(dup).data, status=201)


# # views.py mein yeh imports add karo
# from rest_framework.permissions import IsAuthenticated
# from rest_framework import generics
# from django.db.models import Q
# from .models import Resume
# from .serializers import ResumeSerializer

# # Student APIs for templates and resumes

# # # ✅ Student Templates List (only active templates)
# # class StudentTemplateListView(generics.ListAPIView):
# #     permission_classes = [IsAuthenticated]
# #     serializer_class = ResumeTemplateSerializer
    
# #     def get_queryset(self):
# #         return ResumeTemplate.objects.filter(status="active").order_by('name')

# # # ✅ Student Resumes List/Create
# # class StudentResumeListCreateView(generics.ListCreateAPIView):
# #     permission_classes = [IsAuthenticated]
# #     serializer_class = ResumeSerializer
    
# #     def get_queryset(self):
# #         return Resume.objects.filter(user=self.request.user).order_by('-updated_at')
    
# #     def perform_create(self, serializer):
# #         template = serializer.validated_data.get('template')
# #         # Create default empty resume data
# #         default_data = {
# #             "header": {
# #                 "fullName": "",
# #                 "jobTitle": "",
# #                 "email": "",
# #                 "phone": "",
# #                 "location": "",
# #                 "linkedin": "",
# #                 "website": ""
# #             },
# #             "summary": "",
# #             "experience": [{"title": "", "company": "", "location": "", "from": "", "to": "", "bullets": [""]}],
# #             "education": [{"school": "", "degree": "", "from": "", "to": ""}],
# #             "skills": {"programming": [], "frameworks": [], "tools": []},
# #             "projects": [{"name": "", "desc": ""}]
# #         }
        
# #         resume = serializer.save(
# #             user=self.request.user,
# #             data=default_data,
# #             status="draft"
# #         )
# #         return resume

# # # ✅ Student Resume Detail/Update/Delete
# # class StudentResumeDetailView(generics.RetrieveUpdateDestroyAPIView):
# #     permission_classes = [IsAuthenticated]
# #     serializer_class = ResumeSerializer
    
# #     def get_queryset(self):
# #         return Resume.objects.filter(user=self.request.user)



# # views.py mein yeh APIs add karo
# # Student Template Detail View
# # class StudentTemplateDetailView(APIView):
# #     permission_classes = [IsAuthenticated]
    
# #     def get(self, request, pk):
# #         try:
# #             template = ResumeTemplate.objects.get(id=pk, status="active")
# #             serializer = ResumeTemplateSerializer(template)
# #             return Response(serializer.data)
# #         except ResumeTemplate.DoesNotExist:
# #             return Response({"detail": "Template not found or not active"}, status=404)

# # Student Resume Update View
# class StudentResumeUpdateView(generics.UpdateAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = ResumeSerializer
    
#     def get_queryset(self):
#         return Resume.objects.filter(user=self.request.user)
    
#     def perform_update(self, serializer):
#         serializer.save()

# # views.py (replace your current StudentResumeDetailView with this)

# from rest_framework import generics
# from rest_framework.permissions import IsAuthenticated
# from .models import Resume
# from .serializers import ResumeSerializer

# # class StudentResumeDetailView(generics.RetrieveUpdateDestroyAPIView):
# #     permission_classes = [IsAuthenticated]
# #     serializer_class = ResumeSerializer

# #     def get_queryset(self):
# #         # ✅ user can only access own resumes
# #         return Resume.objects.filter(user=self.request.user)


# # # ✅ Student Dashboard Stats
# # class StudentDashboardStatsView(APIView):
# #     permission_classes = [IsAuthenticated]
    
# #     def get(self, request):
# #         user = request.user
# #         resumes = Resume.objects.filter(user=user)
        
# #         stats = {
# #             "totalResumes": resumes.count(),
# #             "completed": resumes.filter(status="completed").count(),
# #             "inProgress": resumes.filter(status__in=["draft", "in_progress"]).count(),
# #             "downloads": resumes.aggregate(total=Sum('download_count'))['total'] or 0
# #         }
        
# #         return Response(stats)

# # # ✅ Student Resume Download Tracking
# # from django.utils import timezone
# # from django.db.models import Sum
# # from django.utils import timezone

# # class StudentResumeDownloadView(APIView):
# #     permission_classes = [IsAuthenticated]
    
# #     def post(self, request, resume_id):
# #         try:
# #             resume = Resume.objects.get(id=resume_id, user=request.user)
# #             resume.download_count += 1
# #             resume.last_downloaded = timezone.now()
# #             resume.save()
            
# #             # Increment template downloads count too
# #             if resume.template:
# #                 resume.template.downloads += 1
# #                 resume.template.save()
            
# #             return Response({
# #                 "message": "Download tracked successfully",
# #                 "download_count": resume.download_count
# #             })
# #         except Resume.DoesNotExist:
# #             return Response({"error": "Resume not found"}, status=404)

# # views.py (important resume views)

# from django.db.models import Sum
# from django.utils import timezone
# from rest_framework import generics, status
# from rest_framework.permissions import IsAuthenticated, IsAdminUser
# from rest_framework.response import Response
# from rest_framework.views import APIView

# from .models import Resume, ResumeTemplate
# from .serializers import ResumeSerializer, ResumeTemplateSerializer


# # ✅ STUDENT: Templates list
# class StudentTemplateListView(generics.ListAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = ResumeTemplateSerializer

#     def get_queryset(self):
#         return ResumeTemplate.objects.filter(status="active").order_by("name")


# # ✅ STUDENT: Template detail
# class StudentTemplateDetailView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, pk):
#         try:
#             template = ResumeTemplate.objects.get(id=pk, status="active")
#             serializer = ResumeTemplateSerializer(template, context={"request": request})
#             return Response(serializer.data)
#         except ResumeTemplate.DoesNotExist:
#             return Response({"detail": "Template not found or not active"}, status=404)


# # ✅ STUDENT: Resume list + create
# class StudentResumeListCreateView(generics.ListCreateAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = ResumeSerializer

#     def get_queryset(self):
#         return Resume.objects.filter(user=self.request.user).order_by("-updated_at")

#     def perform_create(self, serializer):
#         default_data = {
#             "header": {"fullName": "", "jobTitle": "", "email": "", "phone": "", "location": "", "linkedin": "", "website": ""},
#             "summary": "",
#             "experience": [{"title": "", "company": "", "location": "", "from": "", "to": "", "bullets": [""]}],
#             "education": [{"school": "", "degree": "", "from": "", "to": ""}],
#             "skills": {"programming": [], "frameworks": [], "tools": []},
#             "projects": [{"name": "", "desc": ""}],
#         }
#         serializer.save(user=self.request.user, data=serializer.validated_data.get("data") or default_data, status="draft")


# # ✅ STUDENT: Resume detail/update/delete  (FIXED)
# class StudentResumeDetailView(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [IsAuthenticated]
#     serializer_class = ResumeSerializer

#     def get_queryset(self):
#         return Resume.objects.filter(user=self.request.user)


# # ✅ STUDENT: Dashboard stats
# class StudentDashboardStatsView(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         resumes = Resume.objects.filter(user=request.user)
#         return Response({
#             "totalResumes": resumes.count(),
#             "completed": resumes.filter(status="completed").count(),
#             "inProgress": resumes.filter(status__in=["draft", "in_progress"]).count(),
#             "downloads": resumes.aggregate(total=Sum("download_count"))["total"] or 0,
#         })


# # ✅ STUDENT: Download tracking
# class StudentResumeDownloadView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, resume_id):
#         try:
#             resume = Resume.objects.get(id=resume_id, user=request.user)
#             resume.download_count = (resume.download_count or 0) + 1
#             resume.last_downloaded = timezone.now()
#             resume.save()

#             if resume.template:
#                 resume.template.downloads = (resume.template.downloads or 0) + 1
#                 resume.template.save()

#             return Response({"message": "Download tracked", "download_count": resume.download_count})
#         except Resume.DoesNotExist:
#             return Response({"error": "Resume not found"}, status=404)


# # ✅ ADMIN: Resume list/create (NEW - fixes 404)
# class AdminResumeListCreateView(generics.ListCreateAPIView):
#     permission_classes = [IsAdminUser]
#     serializer_class = ResumeSerializer

#     def get_queryset(self):
#         return Resume.objects.all().order_by("-updated_at")

#     def perform_create(self, serializer):
#         # admin resume saved under admin user account (for testing templates)
#         serializer.save(user=self.request.user, status=serializer.validated_data.get("status") or "draft")


# # ✅ ADMIN: Resume detail/update/delete (NEW)
# class AdminResumeDetailView(generics.RetrieveUpdateDestroyAPIView):
#     permission_classes = [IsAdminUser]
#     serializer_class = ResumeSerializer
#     queryset = Resume.objects.all()
# # views.py
# from rest_framework.permissions import AllowAny
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework import status
# from rest_framework_simplejwt.tokens import RefreshToken

# from .serializers import StudentRegisterSerializer, StudentLoginSerializer
# from .models import User


# class StudentRegisterView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         serializer = StudentRegisterSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         user = serializer.save()

#         refresh = RefreshToken.for_user(user)
#         return Response(
#             {
#                 "action": "registered",
#                 "access": str(refresh.access_token),
#                 "refresh": str(refresh),
#                 "user": {
#                     "id": user.id,
#                     "phone": user.phone,
#                     "name": user.name,
#                     "email": user.email or "",
#                     "pincode": user.pincode,
#                 },
#             },
#             status=status.HTTP_201_CREATED,
#         )


# class StudentLoginView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         serializer = StudentLoginSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         user = serializer.validated_data["user"]

#         refresh = RefreshToken.for_user(user)
#         return Response(
#             {
#                 "action": "logged_in",
#                 "access": str(refresh.access_token),
#                 "refresh": str(refresh),
#                 "user": {
#                     "id": user.id,
#                     "phone": user.phone,
#                     "name": user.name,
#                     "email": user.email or "",
#                     "pincode": user.pincode,
#                 },
#             }
#         )


# # users/views.py
# from django.conf import settings
# from django.core.mail import EmailMultiAlternatives
# from django.contrib.auth.tokens import default_token_generator
# from django.utils.http import urlsafe_base64_encode
# from django.utils.encoding import force_bytes

# from rest_framework.permissions import AllowAny
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework import status

# from .models import User
# from .serializers import ForgotPasswordSerializer, ResetPasswordSerializer


# class ForgotPasswordView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         serializer = ForgotPasswordSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         email = serializer.validated_data["email"]

#         # ✅ Do not reveal whether email exists (security)
#         user = User.objects.filter(email__iexact=email, is_staff=False, is_active=True).first()

#         if user:
#             uid = urlsafe_base64_encode(force_bytes(user.pk))
#             token = default_token_generator.make_token(user)

#             frontend = getattr(settings, "FRONTEND_URL", "http://localhost:5173").rstrip("/")
#             reset_link = f"{frontend}/reset-password?uid={uid}&token={token}"

#             subject = "Reset your password"
#             text_body = (
#                 f"Hi {user.name or 'User'},\n\n"
#                 f"You requested a password reset.\n"
#                 f"Open this link to set a new password:\n{reset_link}\n\n"
#                 f"If you did not request this, you can ignore this email.\n"
#             )

#             msg = EmailMultiAlternatives(
#                 subject=subject,
#                 body=text_body,
#                 from_email=getattr(settings, "DEFAULT_FROM_EMAIL", None),
#                 to=[user.email],
#             )
#             msg.send(fail_silently=False)

#         return Response(
#             {"message": "If this email is registered, a reset link has been sent."},
#             status=status.HTTP_200_OK,
#         )


# class ResetPasswordView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         serializer = ResetPasswordSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         user = serializer.validated_data["user"]
#         password = serializer.validated_data["password"]

#         user.set_password(password)
#         user.save()

#         return Response({"message": "Password reset successful. Please login now."}, status=200)


# # users/views.py
# from django.conf import settings
# from django.core.mail import EmailMultiAlternatives
# from django.contrib.auth.tokens import default_token_generator
# from django.utils.http import urlsafe_base64_encode
# from django.utils.encoding import force_bytes

# from rest_framework.permissions import AllowAny
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework import status

# from .models import User
# from .serializers import AdminForgotPasswordSerializer, AdminResetPasswordSerializer


# class AdminForgotPasswordView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         serializer = AdminForgotPasswordSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         email = serializer.validated_data["email"]

#         # ✅ only admin users
#         user = User.objects.filter(email__iexact=email, is_staff=True, is_active=True).first()

#         if user and user.email:
#             uid = urlsafe_base64_encode(force_bytes(user.pk))
#             token = default_token_generator.make_token(user)

#             frontend = getattr(settings, "FRONTEND_URL", "http://localhost:5173").rstrip("/")
#             reset_link = f"{frontend}/admin/reset-password?uid={uid}&token={token}"

#             subject = "Admin password reset"
#             text_body = (
#                 f"Hi {user.name or 'Admin'},\n\n"
#                 f"You requested an admin password reset.\n"
#                 f"Open this link to set a new password:\n{reset_link}\n\n"
#                 f"If you did not request this, ignore this email.\n"
#             )

#             # ✅ IMPORTANT: avoid empty from_email
#             from_email = getattr(settings, "DEFAULT_FROM_EMAIL", None) or None

#             msg = EmailMultiAlternatives(
#                 subject=subject,
#                 body=text_body,
#                 from_email=from_email,
#                 to=[user.email],
#             )
#             msg.send(fail_silently=False)

#         # ✅ same response always (security)
#         return Response(
#             {"message": "If this email is registered, a reset link has been sent."},
#             status=status.HTTP_200_OK,
#         )


# class AdminResetPasswordView(APIView):
#     permission_classes = [AllowAny]

#     def post(self, request):
#         serializer = AdminResetPasswordSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         user = serializer.validated_data["user"]
#         password = serializer.validated_data["password"]

#         user.set_password(password)
#         user.save()

#         return Response({"message": "Admin password reset successful. Please login now."}, status=200)


# # users/views.py
# from rest_framework import generics
# from rest_framework.permissions import IsAdminUser
# from .models import User
# from .serializers import AdminUserSerializer
# from django.templatetags.static import static
# from .marketplace_templates import MARKETPLACE_TEMPLATES, normalized_marketplace_templates


# # users/views.py
# from rest_framework import generics
# from rest_framework.permissions import IsAdminUser
# from .models import User
# from .serializers import AdminUserSerializer


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


# """users/views_marketplace_patch.py

# ✅ Copy/paste the classes + helper functions below into your existing users/views.py.

# What it fixes:
# 1) Marketplace templates are now 31 different designs.
# 2) preview images are served from Django static and import/duplicate freezes them into DB.
# 3) Import works even without external URLs (no requests.get needed).

# Requires:
# - users/marketplace_templates.py (from backend_marketplace_templates.py)
# - static/marketplace/tpl-01.png ... tpl-31.png

# """

# from django.contrib.staticfiles import finders
# from django.templatetags.static import static
# from django.utils.text import slugify
# from django.core.files.base import ContentFile
# from rest_framework.permissions import IsAdminUser
# from rest_framework.response import Response
# from rest_framework.views import APIView
# from rest_framework import status

# from .models import ResumeTemplate
# from .serializers import ResumeTemplateSerializer
# from .marketplace_templates import MARKETPLACE_TEMPLATES

# # --- keep your existing normalize_template_schema(...) exactly as-is ---
# # from .views import normalize_template_schema


# def _marketplace_with_preview_urls(request):
#     """Attach absolute preview_image_url at runtime."""
#     out = []
#     for tpl in MARKETPLACE_TEMPLATES:
#         t = dict(tpl)
#         sp = t.get("preview_static_path") or ""
#         if sp:
#             # static() returns relative URL, build_absolute_uri => absolute
#             t["preview_image_url"] = request.build_absolute_uri(static(sp))
#         else:
#             t["preview_image_url"] = ""
#         out.append(t)
#     return out


# class AdminMarketplaceTemplatesView(APIView):
#     permission_classes = [IsAdminUser]

#     def get(self, request):
#         # If you already have normalized_marketplace_templates(), you can call it too.
#         # But our marketplace file already contains schema shapes compatible with your normalizer.
#         return Response({"results": _marketplace_with_preview_urls(request)})


# class AdminTemplateImportView(APIView):
#     """CLONE & FREEZE

#     - marketplace_key OR direct payload
#     - If marketplace template has preview_static_path, we read it from staticfiles (NO internet).
#     - schema stored in DB, preview stored in template.preview_image.
#     """

#     permission_classes = [IsAdminUser]

#     def post(self, request):
#         key = request.data.get("marketplace_key")

#         if key:
#             tpl = next((x for x in MARKETPLACE_TEMPLATES if x.get("key") == key), None)
#             if not tpl:
#                 return Response({"detail": "Invalid marketplace_key"}, status=400)

#             name = tpl.get("name")
#             category = tpl.get("category", "Modern")
#             layout = tpl.get("layout", "Two Column")
#             color = tpl.get("color", "#2563eb")
#             schema = tpl.get("schema", {})
#             preview_static_path = tpl.get("preview_static_path")
#             preview_url = request.build_absolute_uri(static(preview_static_path)) if preview_static_path else ""

#         else:
#             # direct import support
#             name = request.data.get("name")
#             category = request.data.get("category", "Modern")
#             layout = request.data.get("layout", "Two Column")
#             color = request.data.get("color", "#2563eb")
#             schema = request.data.get("schema", {})
#             preview_url = request.data.get("preview_image_url", "")
#             preview_static_path = None

#             if not name:
#                 return Response({"detail": "name is required"}, status=400)

#         # ✅ normalize schema (use your existing helper)
#         from .views import normalize_template_schema  # local import to avoid circular
#         schema = normalize_template_schema(schema)

#         # unique naming fallback
#         base_name = name
#         i = 1
#         while ResumeTemplate.objects.filter(name=name).exists():
#             i += 1
#             name = f"{base_name} ({i})"

#         obj = ResumeTemplate.objects.create(
#             name=name,
#             category=category,
#             layout=layout,
#             status="draft",
#             color=color,
#             source="imported",
#             schema=schema,
#         )

#         # ✅ Freeze preview
#         content = None
#         if preview_static_path:
#             abs_path = finders.find(preview_static_path)
#             if abs_path:
#                 try:
#                     with open(abs_path, "rb") as f:
#                         content = f.read()
#                 except Exception:
#                     content = None
#         elif preview_url:
#             # external URL fallback (optional)
#             try:
#                 import requests

#                 r = requests.get(preview_url, timeout=10)
#                 r.raise_for_status()
#                 content = r.content
#             except Exception:
#                 content = None

#         if content:
#             fname = f"{slugify(obj.name)}.png"
#             try:
#                 obj.preview_image.save(fname, ContentFile(content), save=True)
#             except Exception:
#                 pass

#         # serializer absolute preview_image url (if context request)
#         return Response(ResumeTemplateSerializer(obj, context={"request": request}).data, status=status.HTTP_201_CREATED)

# users/views.py

import random

from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.contrib.staticfiles import finders
from django.core.files.base import ContentFile
from django.core.mail import EmailMultiAlternatives
from django.templatetags.static import static
from django.utils import timezone
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.text import slugify
from django.db.models import Sum, Q

from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import (
    User,
    OTP,
    ResumeTemplate,
    TemplatePricing,
    Subscription,
    Resume,
    TemplatePayment, TemplateAccess,
)
from .serializers import (
    UserSerializer,
    ResumeTemplateSerializer,
    TemplatePricingSerializer,
    SubscriptionSerializer,
    ResumeSerializer,
    StudentRegisterSerializer,
    StudentLoginSerializer,
    ForgotPasswordSerializer,
    ResetPasswordSerializer,
    AdminForgotPasswordSerializer,
    AdminResetPasswordSerializer,
    AdminUserSerializer,
    StudentTemplateSerializer,
    TemplatePaymentAdminSerializer,
)
import time
import hmac
import hashlib
import requests
from .access import has_template_access, has_active_subscription
from rest_framework.exceptions import ValidationError

# ✅ NEW: 31 marketplace templates file (zip wala)
from .marketplace_templates import MARKETPLACE_TEMPLATES


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
                email=request.data.get("email", "") or None,
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


# ================== ADMIN LOGIN ==================
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
# ✅ Admin Templates APIs
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
# ✅ Admin Template Pricing APIs
# =========================
class AdminTemplatePricingListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = TemplatePricing.objects.select_related("template").all().order_by("-updated_at")
    serializer_class = TemplatePricingSerializer


class AdminTemplatePricingDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = TemplatePricing.objects.select_related("template").all()
    serializer_class = TemplatePricingSerializer


# =========================
# ✅ Subscription (Admin)
# =========================
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


# ------------------------------
# ✅ Schema Normalizer (BACKEND)
# ------------------------------
def normalize_template_schema(schema: dict) -> dict:
    """
    Backward compatible schema normalizer:
    - old schemas => auto add type/dataKey
    - new schemas (already typed) => keep
    """
    if not isinstance(schema, dict):
        return {}

    s = dict(schema)
    s.setdefault("version", 1)
    s.setdefault("layout", "Single Column")
    s.setdefault("theme", {})
    s.setdefault("order", [])
    s.setdefault("columns", {"left": [], "right": []})
    s.setdefault("sections", {})

    sections = s.get("sections") or {}
    if not isinstance(sections, dict):
        sections = {}

    def ensure_section(id_, default_type, default_key=None):
        cfg = sections.get(id_) or {}
        if not isinstance(cfg, dict):
            cfg = {}
        cfg.setdefault("enabled", True)
        if "type" not in cfg:
            cfg["type"] = default_type
        if default_key and "dataKey" not in cfg:
            cfg["dataKey"] = default_key
        sections[id_] = cfg

    ensure_section("header", "header", "header")
    ensure_section("summary", "text", "summary")
    ensure_section("experience", "timeline", "experience")
    ensure_section("education", "timeline", "education")
    ensure_section("projects", "timeline", "projects")
    ensure_section("skills", "skills", "skills")
    ensure_section("certifications", "list", "certifications")
    ensure_section("languages", "languages", "languages")

    # optional
    if "courses" in sections:
        ensure_section("courses", "list", "courses")
    if "achievements" in sections:
        ensure_section("achievements", "grid", "achievements")
    if "strengths" in sections:
        ensure_section("strengths", "grid", "strengths")
    if "contacts" in sections:
        ensure_section("contacts", "contacts", "header")
    if "interests" in sections:
        ensure_section("interests", "list", "interests")
    if "sidebarProfile" in sections:
        ensure_section("sidebarProfile", "avatar", "header")

    for sec_id, cfg in list(sections.items()):
        if not isinstance(cfg, dict):
            continue
        if "type" in cfg:
            continue
        if sec_id in ("experience", "education", "projects"):
            cfg["type"] = "timeline"
            cfg.setdefault("dataKey", sec_id)
        elif sec_id in ("summary", "objective"):
            cfg["type"] = "text"
            cfg.setdefault("dataKey", sec_id)
        elif sec_id in ("languages",):
            cfg["type"] = "languages"
            cfg.setdefault("dataKey", sec_id)
        else:
            cfg["type"] = "list"
            cfg.setdefault("dataKey", sec_id)
        sections[sec_id] = cfg

    s["sections"] = sections
    return s


# =========================
# ✅ Marketplace (31 templates) + Import (Freeze Preview)
# =========================
def _marketplace_with_preview_urls(request):
    out = []
    for tpl in MARKETPLACE_TEMPLATES:
        t = dict(tpl)
        sp = t.get("preview_static_path") or ""
        if sp:
            t["preview_image_url"] = request.build_absolute_uri(static(sp))
        else:
            t["preview_image_url"] = ""
        out.append(t)
    return out


class AdminMarketplaceTemplatesView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        return Response({"results": _marketplace_with_preview_urls(request)})


class AdminTemplateImportView(APIView):
    """
    CLONE & FREEZE:
    - marketplace_key
    - preview image is read from STATIC (no internet)
    - schema normalized and stored in DB
    """
    permission_classes = [IsAdminUser]

    def post(self, request):
        key = request.data.get("marketplace_key")

        if not key:
            return Response({"detail": "marketplace_key is required"}, status=400)

        tpl = next((x for x in MARKETPLACE_TEMPLATES if x.get("key") == key), None)
        if not tpl:
            return Response({"detail": "Invalid marketplace_key"}, status=400)

        name = tpl.get("name") or key
        category = tpl.get("category", "Modern")
        layout = tpl.get("layout", "Two Column")
        color = tpl.get("color", "#2563eb")
        schema = tpl.get("schema", {})
        preview_static_path = tpl.get("preview_static_path")  # marketplace/tpl-01.png

        schema = normalize_template_schema(schema)

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

        content = None
        if preview_static_path:
            abs_path = finders.find(preview_static_path)
            if abs_path:
                try:
                    with open(abs_path, "rb") as f:
                        content = f.read()
                except Exception:
                    content = None

        if content:
            fname = f"{slugify(obj.name)}.png"
            try:
                obj.preview_image.save(fname, ContentFile(content), save=True)
            except Exception:
                pass

        return Response(
            ResumeTemplateSerializer(obj, context={"request": request}).data,
            status=status.HTTP_201_CREATED,
        )


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

        if src.preview_image:
            try:
                src.preview_image.open("rb")
                content = src.preview_image.read()
                dup.preview_image.save(f"{slugify(dup.name)}.png", ContentFile(content), save=True)
            except Exception:
                pass

        return Response(ResumeTemplateSerializer(dup, context={"request": request}).data, status=201)

class StudentTemplateListView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = StudentTemplateSerializer

    def get_queryset(self):
        return ResumeTemplate.objects.filter(status="active").order_by("name")

    def get_serializer_context(self):
        ctx = super().get_serializer_context()
        ctx["request"] = self.request
        return ctx


class StudentTemplateDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        template = ResumeTemplate.objects.filter(id=pk, status="active").first()
        if not template:
            return Response({"detail": "Template not found or not active"}, status=404)
        return Response(StudentTemplateSerializer(template, context={"request": request}).data)

class StudentResumeListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ResumeSerializer

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user).order_by("-updated_at")

    def perform_create(self, serializer):
        template = serializer.validated_data.get("template")  # template_id -> template
        if template and not has_template_access(self.request.user, template):
            raise ValidationError({"template_id": "This template is paid/locked. Please purchase or subscribe."})

        default_data = {
            "header": {"fullName": "", "jobTitle": "", "email": "", "phone": "", "location": "", "linkedin": "", "website": ""},
            "summary": "",
            "experience": [{"title": "", "company": "", "location": "", "from": "", "to": "", "bullets": [""]}],
            "education": [{"school": "", "degree": "", "from": "", "to": ""}],
            "skills": {"programming": [], "frameworks": [], "tools": []},
            "projects": [{"name": "", "desc": ""}],
        }

        serializer.save(
            user=self.request.user,
            data=serializer.validated_data.get("data") or default_data,
            status="draft",
        )
class StudentResumeDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ResumeSerializer

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)

    def perform_update(self, serializer):
        new_template = serializer.validated_data.get("template")  # may be None if not sent
        if new_template and not has_template_access(self.request.user, new_template):
            raise ValidationError({"template_id": "This template is paid/locked. Please purchase or subscribe."})
        serializer.save()






class StudentTemplateOrderCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        template_id = request.data.get("template_id")
        if not template_id:
            return Response({"detail": "template_id is required"}, status=400)

        template = ResumeTemplate.objects.filter(id=template_id, status="active").first()
        if not template:
            return Response({"detail": "Template not found"}, status=404)

        pricing = getattr(template, "pricing", None)
        if not pricing or pricing.status != "active":
            return Response({"detail": "Pricing not active for this template"}, status=403)

        # Already unlocked?
        if has_template_access(request.user, template):
            return Response({"has_access": True, "detail": "Already has access"}, status=200)

        # Free
        if pricing.billing_type == "free":
            return Response({"has_access": True, "detail": "Template is free"}, status=200)

        # Subscription required
        if pricing.billing_type == "subscription":
            if has_active_subscription(request.user):
                return Response({"has_access": True, "detail": "Subscription active"}, status=200)
            return Response(
                {"has_access": False, "detail": "Subscription required to access this template"},
                status=402,
            )

        # One-time purchase via Razorpay
        if pricing.currency != "INR":
            return Response({"detail": "Only INR supported for Razorpay right now"}, status=400)

        key_id = getattr(settings, "RAZORPAY_KEY_ID", "")
        key_secret = getattr(settings, "RAZORPAY_KEY_SECRET", "")
        if not key_id or not key_secret:
            return Response({"detail": "Razorpay keys not configured in backend"}, status=500)

        amount_paise = int(round(float(pricing.final_price or 0) * 100))
        if amount_paise <= 0:
            return Response({"detail": "Invalid pricing amount"}, status=400)

        receipt = f"tpl_{template.id}_u{request.user.id}_{int(time.time())}"

        r = requests.post(
            "https://api.razorpay.com/v1/orders",
            auth=(key_id, key_secret),
            json={
                "amount": amount_paise,
                "currency": "INR",
                "receipt": receipt,
                "notes": {"template_id": str(template.id), "user_id": str(request.user.id)},
            },
            timeout=20,
        )

        if r.status_code >= 400:
            return Response({"detail": "Razorpay order create failed", "raw": r.text}, status=502)

        order = r.json()
        order_id = order.get("id")
        if not order_id:
            return Response({"detail": "Razorpay order_id missing"}, status=502)

        TemplatePayment.objects.create(
            user=request.user,
            template=template,
            provider="razorpay",
            status="created",
            order_id=order_id,
            currency="INR",
            amount=amount_paise,
            amount_display=float(pricing.final_price or 0),
            pricing_snapshot={
                "billing_type": pricing.billing_type,
                "currency": pricing.currency,
                "price": pricing.price,
                "discount_percent": pricing.discount_percent,
                "final_price": pricing.final_price,
                "template_name": template.name,
            },
        )

        return Response(
            {
                "provider": "razorpay",
                "key": key_id,
                "order_id": order_id,
                "amount": amount_paise,
                "currency": "INR",
                "template_id": template.id,
                "template_name": template.name,
            },
            status=200,
        )


class StudentTemplatePaymentVerifyView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        razorpay_order_id = request.data.get("razorpay_order_id")
        razorpay_payment_id = request.data.get("razorpay_payment_id")
        razorpay_signature = request.data.get("razorpay_signature")

        if not (razorpay_order_id and razorpay_payment_id and razorpay_signature):
            return Response({"detail": "Missing razorpay fields"}, status=400)

        pay = TemplatePayment.objects.filter(
            user=request.user,
            order_id=razorpay_order_id,
        ).select_related("template").first()

        if not pay:
            return Response({"detail": "Order not found"}, status=404)

        key_secret = getattr(settings, "RAZORPAY_KEY_SECRET", "")
        if not key_secret:
            return Response({"detail": "Razorpay secret not configured"}, status=500)

        message = f"{razorpay_order_id}|{razorpay_payment_id}".encode("utf-8")
        expected = hmac.new(key_secret.encode("utf-8"), message, hashlib.sha256).hexdigest()

        if expected != razorpay_signature:
            pay.status = "failed"
            pay.payment_id = razorpay_payment_id
            pay.signature = razorpay_signature
            pay.save(update_fields=["status", "payment_id", "signature"])
            return Response({"detail": "Invalid signature"}, status=400)

        # Mark paid
        pay.status = "paid"
        pay.payment_id = razorpay_payment_id
        pay.signature = razorpay_signature
        pay.paid_at = timezone.now()
        pay.save(update_fields=["status", "payment_id", "signature", "paid_at"])

        # Grant access
        TemplateAccess.objects.get_or_create(
            user=request.user,
            template=pay.template,
            defaults={"access_type": "one_time", "payment": pay, "valid_until": None},
        )

        return Response({"detail": "Payment verified. Template unlocked.", "has_access": True}, status=200)


class AdminPaymentsListView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        qs = TemplatePayment.objects.select_related("user", "template").all().order_by("-created_at")

        status_q = request.GET.get("status")
        provider_q = request.GET.get("provider")
        search = (request.GET.get("search") or "").strip()

        if status_q:
            qs = qs.filter(status=status_q)
        if provider_q:
            qs = qs.filter(provider=provider_q)
        if search:
            qs = qs.filter(
                Q(order_id__icontains=search)
                | Q(payment_id__icontains=search)
                | Q(user__phone__icontains=search)
                | Q(user__name__icontains=search)
                | Q(template__name__icontains=search)
            )

        data = TemplatePaymentAdminSerializer(qs, many=True).data
        return Response({"results": data, "count": qs.count()})



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

            from .models import AIUsageEvent

            is_ai = isinstance(resume.data, dict) and ("__ai" in resume.data or "__schema" in resume.data)
            if is_ai:
                job = (resume.data.get("header") or {}).get("jobTitle", "")
                domain = (job or "").strip()[:80]
                applied = resume.data.get("__schema") or {}
                tpl_key = ""
                layout = ""
                if isinstance(applied, dict):
                    tpl_key = str(applied.get("key") or applied.get("template_key") or "")
                    layout = str(applied.get("layout") or "")

                AIUsageEvent.objects.create(
                    user=request.user,
                    resume=resume,
                    event_type="download",
                    domain=domain,
                    template_key=tpl_key,
                    template_layout=layout,
                    prompt_excerpt="",
                )


            return Response({"message": "Download tracked", "download_count": resume.download_count})
        except Resume.DoesNotExist:
            return Response({"error": "Resume not found"}, status=404)


from django.utils import timezone
from django.db.models import Count
from django.db.models.functions import TruncDay, TruncWeek, TruncMonth
from rest_framework.permissions import IsAdminUser
from .models import AIUsageEvent

def _parse_date(s: str):
    # expects YYYY-MM-DD
    try:
        return timezone.datetime.fromisoformat(s).date()
    except Exception:
        return None

class AdminAIUsageView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        preset = (request.GET.get("preset") or "").lower().strip()
        group = (request.GET.get("group") or "day").lower().strip()  # day|week|month
        from_s = (request.GET.get("from") or "").strip()
        to_s = (request.GET.get("to") or "").strip()

        today = timezone.localdate()

        # defaults
        date_from = _parse_date(from_s) or (today - timezone.timedelta(days=30))
        date_to = _parse_date(to_s) or today

        if preset:
            if preset in ("today", "1d"):
                date_from = today
                date_to = today
            elif preset in ("7d", "week"):
                date_from = today - timezone.timedelta(days=6)
                date_to = today
            elif preset in ("30d", "month"):
                date_from = today - timezone.timedelta(days=29)
                date_to = today
            elif preset in ("90d",):
                date_from = today - timezone.timedelta(days=89)
                date_to = today
            elif preset in ("1y", "year"):
                date_from = today - timezone.timedelta(days=364)
                date_to = today

        dt_from = timezone.make_aware(timezone.datetime.combine(date_from, timezone.datetime.min.time()))
        dt_to = timezone.make_aware(timezone.datetime.combine(date_to, timezone.datetime.max.time()))

        qs = AIUsageEvent.objects.filter(created_at__range=(dt_from, dt_to))

        gen_qs = qs.filter(event_type="generate")
        dl_qs = qs.filter(event_type="download")

        # KPIs
        ai_resumes = gen_qs.count()
        ai_downloads = dl_qs.count()
        unique_users = gen_qs.values("user_id").distinct().count()
        avg_per_user = round(ai_resumes / unique_users, 2) if unique_users else 0.0

        # group function
        if group == "week":
            trunc = TruncWeek("created_at")
        elif group == "month":
            trunc = TruncMonth("created_at")
        else:
            trunc = TruncDay("created_at")

        gen_series = (
            gen_qs.annotate(bucket=trunc)
            .values("bucket")
            .annotate(count=Count("id"))
            .order_by("bucket")
        )
        dl_series = (
            dl_qs.annotate(bucket=trunc)
            .values("bucket")
            .annotate(count=Count("id"))
            .order_by("bucket")
        )

        # merge into time_series
        dl_map = {str(x["bucket"].date()): x["count"] for x in dl_series if x["bucket"]}
        time_series = []
        for x in gen_series:
            if not x["bucket"]:
                continue
            key = str(x["bucket"].date())
            time_series.append({
                "label": key,
                "ai_resumes": x["count"],
                "downloads": dl_map.get(key, 0),
            })

        # Domains (top + low)
        domain_counts = (
            gen_qs.exclude(domain="")
            .values("domain")
            .annotate(count=Count("id"))
            .order_by("-count")
        )
        top_domains = [{"name": d["domain"], "count": d["count"]} for d in domain_counts[:8]]
        low_domains = [{"name": d["domain"], "count": d["count"]} for d in domain_counts.reverse()[:8]]

        # Templates
        tpl_counts = (
            gen_qs.exclude(template_key="")
            .values("template_key", "template_layout")
            .annotate(count=Count("id"))
            .order_by("-count")
        )
        templates = [
            {"key": x["template_key"], "layout": x["template_layout"], "count": x["count"]}
            for x in tpl_counts[:12]
        ]

        # Heatmap (day x hour) for generation peaks
        # day: 0=Mon..6=Sun
        heat = [[0 for _ in range(24)] for _ in range(7)]
        for ev in gen_qs.only("created_at"):
            dt = timezone.localtime(ev.created_at)
            heat[dt.weekday()][dt.hour] += 1

        return Response({
            "range": {"from": str(date_from), "to": str(date_to), "group": group},
            "kpis": {
                "ai_resumes": ai_resumes,
                "ai_downloads": ai_downloads,
                "unique_users": unique_users,
                "avg_per_user": avg_per_user,
            },
            "time_series": time_series,
            "top_domains": top_domains,
            "low_domains": low_domains,
            "templates": templates,
            "heatmap": {
                "days": ["Mon","Tue","Wed","Thu","Fri","Sat","Sun"],
                "hours": list(range(24)),
                "matrix": heat,
            },
        })

# =========================
# ✅ ADMIN: Resumes
# =========================
class AdminResumeListCreateView(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = ResumeSerializer

    def get_queryset(self):
        return Resume.objects.all().order_by("-updated_at")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, status=serializer.validated_data.get("status") or "draft")


class AdminResumeDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = ResumeSerializer
    queryset = Resume.objects.all()


# =========================
# ✅ Student Register/Login (email+password)
# =========================
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


# =========================
# ✅ Forgot/Reset Password (Student)
# =========================
class ForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
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

        return Response({"message": "If this email is registered, a reset link has been sent."}, status=200)


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


# =========================
# ✅ Forgot/Reset Password (Admin)
# =========================
class AdminForgotPasswordView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AdminForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
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

            from_email = getattr(settings, "DEFAULT_FROM_EMAIL", None) or None
            msg = EmailMultiAlternatives(subject=subject, body=text_body, from_email=from_email, to=[user.email])
            msg.send(fail_silently=False)

        return Response({"message": "If this email is registered, a reset link has been sent."}, status=200)


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


# =========================
# ✅ Admin Staff CRUD
# =========================
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
    
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .models import Resume, ResumeTemplate
from .ai_resume import call_openai_resume, build_dynamic_resume_schema

from django.templatetags.static import static
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Resume, ResumeTemplate
from .marketplace_templates import MARKETPLACE_TEMPLATES
from .ai_resume import call_openai_resume, build_dynamic_resume_schema


def _pick_default_template_schema() -> dict:
    # pick first marketplace template as default
    if MARKETPLACE_TEMPLATES and isinstance(MARKETPLACE_TEMPLATES[0], dict):
        return MARKETPLACE_TEMPLATES[0].get("schema") or {}
    return {
        "version": 1,
        "layout": "Single Column",
        "theme": {"primary": "#2563eb"},
        "order": ["header", "summary", "experience", "education", "skills", "projects"],
        "columns": {"left": [], "right": []},
        "sections": {
            "header": {"enabled": True, "type": "header", "dataKey": "header"},
            "summary": {"enabled": True, "type": "text", "dataKey": "summary"},
            "experience": {"enabled": True, "type": "timeline", "dataKey": "experience"},
            "education": {"enabled": True, "type": "timeline", "dataKey": "education"},
            "skills": {"enabled": True, "type": "skills", "dataKey": "skills"},
            "projects": {"enabled": True, "type": "timeline", "dataKey": "projects"},
        },
    }


class AITemplateSuggestionsView(APIView):
    """
    Return 5 templates (cards) for user to choose.
    Uses marketplace templates (no DB dependency).
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        out = []
        for tpl in (MARKETPLACE_TEMPLATES or [])[:5]:
            t = dict(tpl)
            sp = t.get("preview_static_path") or ""
            t["preview_image_url"] = request.build_absolute_uri(static(sp)) if sp else ""
            # keep only fields needed by UI
            out.append({
                "key": t.get("key"),
                "name": t.get("name"),
                "layout": t.get("layout"),
                "color": t.get("color"),
                "preview_image_url": t.get("preview_image_url"),
                "schema": t.get("schema"),
            })
        return Response({"results": out})


# class AIResumeGenerateView(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         prompt = (request.data.get("prompt") or "").strip()
#         template_id = request.data.get("template_id")
#         template_schema = request.data.get("template_schema")

#         if not prompt:
#             return Response({"detail": "prompt is required"}, status=status.HTTP_400_BAD_REQUEST)

#         # ✅ 1) Decide which template schema to apply
#         applied_schema = None
#         tpl_obj = None

#         if isinstance(template_schema, dict) and template_schema.get("sections"):
#             applied_schema = template_schema
#         elif template_id:
#             try:
#                 tpl_obj = ResumeTemplate.objects.get(pk=int(template_id))
#                 applied_schema = tpl_obj.schema or None
#             except Exception:
#                 tpl_obj = None
#                 applied_schema = None

#         # ✅ If user did not choose anything -> auto-pick default marketplace schema
#         if not applied_schema:
#             applied_schema = _pick_default_template_schema()

#         # ✅ 2) Extract extra text fields from schema
#         extra_text_fields = []
#         sections = applied_schema.get("sections") or {}
#         if isinstance(sections, dict):
#             for sec_id, cfg in sections.items():
#                 if not isinstance(cfg, dict):
#                     continue
#                 if cfg.get("enabled") is False:
#                     continue
#                 if cfg.get("type") == "text":
#                     dk = cfg.get("dataKey") or sec_id
#                     if dk and dk != "summary":
#                         extra_text_fields.append(dk)

#         extra_text_fields = list(dict.fromkeys(extra_text_fields))

#         # ✅ 3) Build dynamic schema for OpenAI output
#         response_schema = build_dynamic_resume_schema(extra_text_fields)

#         # ✅ 4) Tell AI what fields to fill
#         prompt_for_ai = (
#             f"{prompt}\n\n"
#             f"Template-driven text sections (must include): {extra_text_fields}\n"
#             f"Return meaningful content for each (or empty string).\n"
#             f"Always include array keys even if empty: certifications,languages,interests,strengths,achievements,courses.\n"
#         )

#         try:
#             gen = call_openai_resume(prompt_for_ai, response_schema)
#         except Exception as e:
#             return Response({"detail": str(e)}, status=status.HTTP_502_BAD_GATEWAY)

#         title = gen.get("title") or "AI Resume"
#         data = gen.get("data") or {}

#         # store schema in resume for later rendering
#         data["__schema"] = applied_schema

#         resume = Resume.objects.create(
#             user=request.user,
#             template=tpl_obj,   # could be None when using marketplace schema
#             title=title,
#             data=data,
#             status="draft",
#         )

#         return Response({
#             "resume_id": resume.pk,
#             "title": resume.title,
#             "data": resume.data,
#             "template_pk": tpl_obj.pk if tpl_obj else None,
#             "applied_schema": applied_schema,
#         }, status=status.HTTP_201_CREATED)
from .models import AIUsageEvent
from .ai_resume import call_openai_resume, build_dynamic_resume_schema
from .ai_templates import get_suggestions, pick_random_template
class AITemplateSuggestionsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # returns 5 different templates each time
        items = []
        for t in get_suggestions(5):
            items.append({
                "key": t["key"],
                "name": t["name"],
                "layout": t["layout"],
                "color": t["color"],
                "preview_svg": t["preview_svg"],
                "schema": t["schema"],
            })
        return Response({"results": items})
class AIResumeGenerateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        prompt = (request.data.get("prompt") or "").strip()
        template_schema = request.data.get("template_schema")  # optional

        if not prompt:
            return Response({"detail": "prompt is required"}, status=status.HTTP_400_BAD_REQUEST)

        # ✅ If user didn't provide schema -> pick random AI template EVERY time
        if not (isinstance(template_schema, dict) and template_schema.get("sections")):
            template_schema = pick_random_template()["schema"]

        # ✅ derive extra text fields from schema (enabled + type=text)
        extra_text_fields = []
        sections = template_schema.get("sections") or {}
        if isinstance(sections, dict):
            for sec_id, cfg in sections.items():
                if not isinstance(cfg, dict):
                    continue
                if cfg.get("enabled") is False:
                    continue
                if cfg.get("type") == "text":
                    dk = cfg.get("dataKey") or sec_id
                    if dk and dk != "summary":
                        extra_text_fields.append(dk)

        extra_text_fields = list(dict.fromkeys(extra_text_fields))

        # ✅ dynamic schema (strict)
        response_schema = build_dynamic_resume_schema(extra_text_fields)

        # ✅ domain-specific instruction (role inference happens inside model)
        prompt_for_ai = (
            f"{prompt}\n\n"
            f"IMPORTANT:\n"
            f"- Write resume ONLY for the role/domain in the prompt.\n"
            f"- If prompt says Full Stack Developer -> full stack skills/projects.\n"
            f"- If prompt says Sales -> sales KPIs, targets, CRM.\n"
            f"- If prompt says Banking -> compliance, financial products, risk.\n\n"
            f"Template-driven text fields you MUST fill: {extra_text_fields}\n"
            f"Always include optional arrays even if empty: certifications,languages,interests,strengths,achievements,courses.\n"
        )

        try:
            gen = call_openai_resume(prompt_for_ai, response_schema)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_502_BAD_GATEWAY)

        title = gen.get("title") or "AI Resume"
        data = gen.get("data") or {}

        # ✅ attach schema so frontend always renders same
        data["__schema"] = template_schema

        resume = Resume.objects.create(
            user=request.user,
            template=None,
            title=title,
            data=data,
            status="draft",
        )
                # infer domain from prompt / jobTitle
        job = (data.get("header") or {}).get("jobTitle", "")
        domain = (job or prompt).strip()[:80]

        # template meta (from schema)
        applied = data.get("__schema") or {}
        tpl_key = ""
        if isinstance(applied, dict):
            tpl_key = str(applied.get("key") or applied.get("template_key") or "")
        layout = str((applied.get("layout") if isinstance(applied, dict) else "") or "")

        AIUsageEvent.objects.create(
            user=request.user,
            resume=resume,
            event_type="generate",
            domain=domain,
            template_key=tpl_key,
            template_layout=layout,
            prompt_excerpt=(prompt[:500] if prompt else ""),
        )


        return Response({
            "resume_id": resume.pk,
            "title": resume.title,
            "data": resume.data,
            "applied_schema": template_schema,   # return schema as source of truth
        }, status=status.HTTP_201_CREATED)











