# # from rest_framework import serializers
# # from .models import User, OTP


# # class UserSerializer(serializers.ModelSerializer):
# #     class Meta:
# #         model = User
# #         fields = [
# #             "id",
# #             "phone",
# #             "name",
# #             "email",
# #             "pincode",
# #             "-created_at",
# #         ]


# # class OTPSendSerializer(serializers.Serializer):
# #     phone = serializers.CharField(max_length=10)


# # class OTPVerifySerializer(serializers.Serializer):
# #     phone = serializers.CharField(max_length=10)
# #     code = serializers.CharField(max_length=6)

# # serializers.py
# from rest_framework import serializers
# from .models import User, OTP


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = [
#             "id",
#             "phone",
#             "name",
#             "email",
#             "pincode",
#             "date_joined",
#         ]
#         read_only_fields = ["id", "date_joined"]

#     def create(self, validated_data):
#         # For OTP-based users: no password needed
#         user = User.objects.create(**validated_data)
#         user.set_unusable_password()
#         user.save()
#         return user


# class OTPSendSerializer(serializers.Serializer):
#     phone = serializers.CharField(max_length=10)


# class OTPVerifySerializer(serializers.Serializer):
#     phone = serializers.CharField(max_length=10)
#     code = serializers.CharField(max_length=6)

from rest_framework import serializers
from .models import User, OTP, ResumeTemplate, TemplatePricing


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "phone", "name", "email", "pincode", "date_joined"]
        read_only_fields = ["id", "date_joined"]

    def create(self, validated_data):
        # OTP-based users: password not needed
        user = User.objects.create(**validated_data)
        user.set_unusable_password()
        user.save()
        return user


class OTPSendSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=10)


class OTPVerifySerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=10)
    code = serializers.CharField(max_length=6)


# =========================
# ✅ NEW: Templates + Pricing serializers
# =========================

# class ResumeTemplateSerializer(serializers.ModelSerializer):
#     updated = serializers.SerializerMethodField()

#     class Meta:
#         model = ResumeTemplate
#         fields = [
#             "id",
#             "name",
#             "category",
#             "layout",
#             "status",
#             "downloads",
#             "rating",
#             "color",
#             "updated",
#             "updated_at",
#             "created_at",
#         ]
#         read_only_fields = ["id", "updated", "updated_at", "created_at"]

#     def get_updated(self, obj):
#         # frontend wants dd/mm/yyyy
#         return obj.updated_at.strftime("%d/%m/%Y")


# class TemplatePricingSerializer(serializers.ModelSerializer):
#     templateName = serializers.CharField(source="template.name", read_only=True)
#     template_id = serializers.PrimaryKeyRelatedField(
#         source="template", queryset=ResumeTemplate.objects.all(), write_only=True
#     )
#     updated = serializers.SerializerMethodField()

#     class Meta:
#         model = TemplatePricing
#         fields = [
#             "id",
#             "template_id",
#             "templateName",
#             "billing_type",
#             "currency",
#             "price",
#             "discount_percent",
#             "final_price",
#             "status",
#             "updated",
#             "updated_at",
#             "created_at",
#         ]
#         read_only_fields = ["id", "templateName", "final_price", "updated", "updated_at", "created_at"]

#     def get_updated(self, obj):
#         return obj.updated_at.strftime("%d/%m/%Y")

# serializers.py
from rest_framework import serializers
from .models import ResumeTemplate, TemplatePricing

# class ResumeTemplateSerializer(serializers.ModelSerializer):
#     updated = serializers.SerializerMethodField()

#     class Meta:
#         model = ResumeTemplate
#         fields = [
#             "id",
#             "name",
#             "category",
#             "layout",
#             "status",
#             "downloads",
#             "rating",
#             "color",

#             # ✅ NEW
#             "source",
#             "description",
#             "schema",
#             "preview_image",
#             "version",

#             "updated",
#             "updated_at",
#             "created_at",
#         ]
#         read_only_fields = ["id", "updated", "updated_at", "created_at", "version"]

#     def get_updated(self, obj):
#         return obj.updated_at.strftime("%d/%m/%Y")


# class TemplatePricingSerializer(serializers.ModelSerializer):
#     templateName = serializers.CharField(source="template.name", read_only=True)

#     # ✅ write-only (already)
#     template_id = serializers.PrimaryKeyRelatedField(
#         source="template", queryset=ResumeTemplate.objects.all(), write_only=True
#     )

#     # ✅ read-only - frontend edit ke liye
#     template_pk = serializers.IntegerField(source="template.id", read_only=True)

#     updated = serializers.SerializerMethodField()

#     class Meta:
#         model = TemplatePricing
#         fields = [
#             "id",
#             "template_id",
#             "template_pk",
#             "templateName",
#             "billing_type",
#             "currency",
#             "price",
#             "discount_percent",
#             "final_price",
#             "status",
#             "updated",
#             "updated_at",
#             "created_at",
#         ]
#         read_only_fields = ["id", "templateName", "template_pk", "final_price", "updated", "updated_at", "created_at"]

#     def get_updated(self, obj):
#         return obj.updated_at.strftime("%d/%m/%Y")


# # serializers.py

# from .models import Subscription,Resume
# class SubscriptionSerializer(serializers.ModelSerializer):
#     # display fields for table
#     user_name = serializers.CharField(source="user.name", read_only=True)
#     user_email = serializers.CharField(source="user.email", read_only=True)
#     user_phone = serializers.CharField(source="user.phone", read_only=True)

#     # write field for create/update
#     user_id = serializers.PrimaryKeyRelatedField(
#         source="user",
#         queryset=User.objects.filter(is_staff=False),
#         write_only=True,
#         required=True,
#     )

#     class Meta:
#         model = Subscription
#         fields = [
#             "id",
#             "user_id",
#             "user_name",
#             "user_email",
#             "user_phone",
#             "plan",
#             "amount",
#             "status",
#             "start_date",
#             "end_date",
#             "auto_renew",
#             "created_at",
#         ]
#         read_only_fields = ["id", "user_name", "user_email", "user_phone", "created_at"]
        


# # # serializers.py mein yeh add karo
# # class ResumeSerializer(serializers.ModelSerializer):
# #     template_name = serializers.CharField(source="template.name", read_only=True, allow_null=True)
# #     user_name = serializers.CharField(source="user.name", read_only=True)
    
# #     # For student creation
# #     template_id = serializers.PrimaryKeyRelatedField(
# #         source="template",
# #         queryset=ResumeTemplate.objects.filter(status="active"),
# #         write_only=True,
# #         required=True
# #     )
    
# #     class Meta:
# #         model = Resume
# #         fields = [
# #             "id",
# #             "title",
# #             "data",
# #             "status",
# #             "template_id",
# #             "template_name",
# #             "user_name",
# #             "download_count",
# #             "last_downloaded",
# #             "created_at",
# #             "updated_at"
# #         ]
# #         read_only_fields = ["id", "template_name", "user_name", "download_count", "last_downloaded", "created_at", "updated_at"]

# class ResumeSerializer(serializers.ModelSerializer):
#     template_name = serializers.CharField(source="template.name", read_only=True, allow_null=True)
#     template_pk = serializers.IntegerField(source="template.id", read_only=True)  # ✅ ADD THIS
#     user_name = serializers.CharField(source="user.name", read_only=True)

#     # For student creation (request body field)
#     template_id = serializers.PrimaryKeyRelatedField(
#         source="template",
#         queryset=ResumeTemplate.objects.filter(status="active"),
#         write_only=True,
#         required=True
#     )

#     class Meta:
#         model = Resume
#         fields = [
#             "id",
#             "title",
#             "data",
#             "status",
#             "template_id",      # ✅ input
#             "template_pk",      # ✅ output (important)
#             "template_name",
#             "user_name",
#             "download_count",
#             "last_downloaded",
#             "created_at",
#             "updated_at"
#         ]
#         read_only_fields = ["id", "template_pk", "template_name", "user_name", "download_count", "last_downloaded", "created_at", "updated_at"]

# serializers.py
from rest_framework import serializers
from .models import User, ResumeTemplate, TemplatePricing, Subscription, Resume


class ResumeTemplateSerializer(serializers.ModelSerializer):
    updated = serializers.SerializerMethodField()
    preview_image = serializers.SerializerMethodField()  # absolute URL

    class Meta:
        model = ResumeTemplate
        fields = [
            "id",
            "name",
            "category",
            "layout",
            "status",
            "downloads",
            "rating",
            "color",
            "source",
            "description",
            "schema",
            "preview_image",
            "version",
            "updated",
            "updated_at",
            "created_at",
        ]
        read_only_fields = ["id", "updated", "updated_at", "created_at", "version"]

    def get_updated(self, obj):
        return obj.updated_at.strftime("%d/%m/%Y") if obj.updated_at else ""

    def get_preview_image(self, obj):
        if not obj.preview_image:
            return ""
        request = self.context.get("request")
        try:
            url = obj.preview_image.url
        except Exception:
            return ""
        return request.build_absolute_uri(url) if request else url


class TemplatePricingSerializer(serializers.ModelSerializer):
    templateName = serializers.CharField(source="template.name", read_only=True)

    template_id = serializers.PrimaryKeyRelatedField(
        source="template", queryset=ResumeTemplate.objects.all(), write_only=True
    )
    template_pk = serializers.IntegerField(source="template.id", read_only=True)

    updated = serializers.SerializerMethodField()

    class Meta:
        model = TemplatePricing
        fields = [
            "id",
            "template_id",
            "template_pk",
            "templateName",
            "billing_type",
            "currency",
            "price",
            "discount_percent",
            "final_price",
            "status",
            "updated",
            "updated_at",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "templateName",
            "template_pk",
            "final_price",
            "updated",
            "updated_at",
            "created_at",
        ]

    def get_updated(self, obj):
        return obj.updated_at.strftime("%d/%m/%Y") if obj.updated_at else ""


class SubscriptionSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.name", read_only=True)
    user_email = serializers.CharField(source="user.email", read_only=True)
    user_phone = serializers.CharField(source="user.phone", read_only=True)

    user_id = serializers.PrimaryKeyRelatedField(
        source="user",
        queryset=User.objects.filter(is_staff=False),
        write_only=True,
        required=True,
    )

    class Meta:
        model = Subscription
        fields = [
            "id",
            "user_id",
            "user_name",
            "user_email",
            "user_phone",
            "plan",
            "amount",
            "status",
            "start_date",
            "end_date",
            "auto_renew",
            "created_at",
        ]
        read_only_fields = ["id", "user_name", "user_email", "user_phone", "created_at"]


class ResumeSerializer(serializers.ModelSerializer):
    template_name = serializers.CharField(source="template.name", read_only=True, allow_null=True)
    template_pk = serializers.IntegerField(source="template.id", read_only=True)  # ✅ for editor to load template
    user_name = serializers.CharField(source="user.name", read_only=True)

    # ✅ IMPORTANT FIX:
    # required=False so PUT/PATCH doesn't force template_id again
    template_id = serializers.PrimaryKeyRelatedField(
        source="template",
        queryset=ResumeTemplate.objects.filter(status="active"),
        write_only=True,
        required=False,
        allow_null=True,
    )

    class Meta:
        model = Resume
        fields = [
            "id",
            "title",
            "data",
            "status",
            "template_id",     # request input (optional on update)
            "template_pk",     # response output
            "template_name",
            "user_name",
            "download_count",
            "last_downloaded",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["id", "template_pk", "template_name", "user_name", "download_count", "last_downloaded", "created_at", "updated_at"]

    def update(self, instance, validated_data):
        # ✅ keep old template if not provided
        if "template" not in validated_data:
            validated_data["template"] = instance.template
        return super().update(instance, validated_data)

# serializers.py
from rest_framework import serializers
from django.db.models import Q
from .models import User


class StudentRegisterSerializer(serializers.Serializer):
    phone = serializers.CharField(max_length=10)
    name = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    pincode = serializers.CharField(max_length=6)
    password = serializers.CharField(min_length=6, write_only=True)

    def validate_phone(self, value):
        value = "".join([c for c in value if c.isdigit()])
        if len(value) != 10:
            raise serializers.ValidationError("Mobile number must be 10 digits")
        return value

    def validate_pincode(self, value):
        value = "".join([c for c in value if c.isdigit()])
        if len(value) != 6:
            raise serializers.ValidationError("Pincode must be 6 digits")
        return value

    def validate_email(self, value):
        return value.strip().lower()

    def validate(self, attrs):
        phone = attrs["phone"]
        email = attrs["email"]

        # ✅ email kisi aur user ke paas hai?
        email_owner = User.objects.filter(email__iexact=email).first()
        phone_owner = User.objects.filter(phone=phone).first()

        if email_owner and phone_owner and email_owner.id != phone_owner.id:
            raise serializers.ValidationError({"email": "This email is already in use."})

        if email_owner and not phone_owner:
            raise serializers.ValidationError({"email": "This email is already registered."})

        return attrs

    def create(self, validated_data):
        phone = validated_data["phone"]
        email = validated_data["email"]
        password = validated_data["password"]

        name = validated_data.get("name", "")
        pincode = validated_data.get("pincode", "")

        user = User.objects.filter(phone=phone).first()

        # ✅ If phone user exists (OTP user), allow converting to email/password account
        if user:
            user.name = name or user.name
            user.pincode = pincode or user.pincode
            user.email = email
            user.is_staff = False
            user.set_password(password)
            user.save()
            return user

        # ✅ New create
        user = User.objects.create(
            phone=phone,
            name=name,
            email=email,
            pincode=pincode,
            is_staff=False,
        )
        user.set_password(password)
        user.save()
        return user


class StudentLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate_email(self, value):
        return value.strip().lower()

    def validate(self, attrs):
        email = attrs["email"]
        password = attrs["password"]

        user = User.objects.filter(email__iexact=email).first()
        if not user:
            raise serializers.ValidationError({"detail": "Invalid email or password"})

        if user.is_staff:
            raise serializers.ValidationError({"detail": "Please use Admin Login for admin account"})

        if not user.is_active:
            raise serializers.ValidationError({"detail": "Account is disabled"})

        if not user.check_password(password):
            raise serializers.ValidationError({"detail": "Invalid email or password"})

        attrs["user"] = user
        return attrs


# users/serializers.py
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str

from .models import User


class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, value):
        return value.strip().lower()


class ResetPasswordSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    password = serializers.CharField(write_only=True, min_length=6)

    def validate_password(self, value):
        # ✅ Django password validators apply (min length, common password etc.)
        validate_password(value)
        return value

    def validate(self, attrs):
        uid = attrs.get("uid")
        token = attrs.get("token")

        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)
        except Exception:
            raise serializers.ValidationError({"detail": "Invalid reset link"})

        # ✅ only student accounts (optional restriction)
        if user.is_staff:
            raise serializers.ValidationError({"detail": "Invalid reset link"})

        if not default_token_generator.check_token(user, token):
            raise serializers.ValidationError({"detail": "Reset link expired or invalid"})

        attrs["user"] = user
        return attrs
