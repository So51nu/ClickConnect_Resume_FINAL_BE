# # from django.urls import path
# # from .views import (
# #     SendOTPView,
# #     VerifyOTPView,
# #     AdminLoginView,
# #     AdminUserListView,
# #     AdminUserDetailView,
# # )

# # urlpatterns = [
# #     path("send-otp/", SendOTPView.as_view()),
# #     path("verify-otp/", VerifyOTPView.as_view()),
# #     path("admin/login/", AdminLoginView.as_view()),
# #     path("admin/users/", AdminUserListView.as_view()),
# #     path("admin/users/<int:pk>/", AdminUserDetailView.as_view()),
# # ]

# from django.urls import path
# from .views import (
#     SendOTPView,
#     VerifyOTPView,
#     AdminLoginView,
#     AdminUserListView,
#     AdminUserDetailView,
#     AdminTemplateListCreateView,
#     AdminTemplateDetailView,
#     AdminTemplatePricingListCreateView,
#     AdminTemplatePricingDetailView,
#     AdminSubscriptionListView,
#     AdminSubscriptionStatsView,
#     AdminSubscriptionDetailView,
#     AdminMarketplaceTemplatesView,
#     AdminTemplateImportView,
#     AdminTemplateDuplicateView,
#     StudentTemplateListView,
#     StudentResumeListCreateView,
#     StudentResumeDetailView,
#     StudentDashboardStatsView,
#     StudentResumeDownloadView,
#     StudentResumeUpdateView,
#     StudentTemplateDetailView
# )

# urlpatterns = [
#     path("send-otp/", SendOTPView.as_view()),
#     path("verify-otp/", VerifyOTPView.as_view()),

#     path("admin/login/", AdminLoginView.as_view()),
#     path("admin/users/", AdminUserListView.as_view()),
#     path("admin/users/<int:pk>/", AdminUserDetailView.as_view()),

#     # ✅ NEW
#     path("admin/templates/", AdminTemplateListCreateView.as_view()),
#     path("admin/templates/<int:pk>/", AdminTemplateDetailView.as_view()),

#     path("admin/template-marketplace/", AdminMarketplaceTemplatesView.as_view()),
#     path("admin/templates/import/", AdminTemplateImportView.as_view()),
#     path("admin/templates/<int:pk>/duplicate/", AdminTemplateDuplicateView.as_view()),

#     path("admin/template-pricing/", AdminTemplatePricingListCreateView.as_view()),
#     path("admin/template-pricing/<int:pk>/", AdminTemplatePricingDetailView.as_view()),
#     # urls.py

#     path("admin/subscriptions/", AdminSubscriptionListView.as_view()),
#     path("admin/subscriptions/stats/", AdminSubscriptionStatsView.as_view()),
#     path("admin/subscriptions/<int:pk>/", AdminSubscriptionDetailView.as_view()),
#     path("student/templates/", StudentTemplateListView.as_view(), name="student-templates"),
#     path("student/templates/<int:pk>/", StudentTemplateDetailView.as_view(), name="student-template-detail"),
#     path("student/resumes/", StudentResumeListCreateView.as_view(), name="student-resumes"),
#     path("student/resumes/<int:pk>/", StudentResumeDetailView.as_view(), name="student-resume-detail"),
#     path("student/resumes/<int:pk>/update/", StudentResumeUpdateView.as_view(), name="student-resume-update"),
#     path("student/dashboard/stats/", StudentDashboardStatsView.as_view(), name="student-dashboard-stats"),
#     path("student/resumes/<int:resume_id>/download/", StudentResumeDownloadView.as_view(), name="student-resume-download"),

# ]

from django.urls import path
from .views import (
    SendOTPView,
    VerifyOTPView,
    AdminLoginView,
    AdminUserListView,
    AdminUserDetailView,
    AdminTemplateListCreateView,
    AdminTemplateDetailView,
    AdminTemplatePricingListCreateView,
    AdminTemplatePricingDetailView,
    AdminSubscriptionListView,
    AdminSubscriptionStatsView,
    AdminSubscriptionDetailView,
    AdminMarketplaceTemplatesView,
    AdminTemplateImportView,
    AdminTemplateDuplicateView,

    StudentTemplateListView,
    StudentTemplateDetailView,
    StudentResumeListCreateView,
    StudentResumeDetailView,
    StudentDashboardStatsView,
    StudentResumeDownloadView,

    # ✅ NEW admin resume endpoints
    AdminResumeListCreateView,
    AdminResumeDetailView,
    StudentRegisterView,   # ✅ add
    StudentLoginView,
    ForgotPasswordView,
    ResetPasswordView,
)

urlpatterns = [
    path("send-otp/", SendOTPView.as_view()),
    path("verify-otp/", VerifyOTPView.as_view()),
    path("register/", StudentRegisterView.as_view()),
    path("login/", StudentLoginView.as_view()),
    path("password/forgot/", ForgotPasswordView.as_view()),
    path("password/reset/", ResetPasswordView.as_view()),
    path("admin/login/", AdminLoginView.as_view()),
    path("admin/users/", AdminUserListView.as_view()),
    path("admin/users/<int:pk>/", AdminUserDetailView.as_view()),

    path("admin/templates/", AdminTemplateListCreateView.as_view()),
    path("admin/templates/<int:pk>/", AdminTemplateDetailView.as_view()),

    path("admin/template-marketplace/", AdminMarketplaceTemplatesView.as_view()),
    path("admin/templates/import/", AdminTemplateImportView.as_view()),
    path("admin/templates/<int:pk>/duplicate/", AdminTemplateDuplicateView.as_view()),

    path("admin/template-pricing/", AdminTemplatePricingListCreateView.as_view()),
    path("admin/template-pricing/<int:pk>/", AdminTemplatePricingDetailView.as_view()),

    path("admin/subscriptions/", AdminSubscriptionListView.as_view()),
    path("admin/subscriptions/stats/", AdminSubscriptionStatsView.as_view()),
    path("admin/subscriptions/<int:pk>/", AdminSubscriptionDetailView.as_view()),

    # ✅ ADMIN resumes (fix 404)
    path("admin/resumes/", AdminResumeListCreateView.as_view(), name="admin-resumes"),
    path("admin/resumes/<int:pk>/", AdminResumeDetailView.as_view(), name="admin-resume-detail"),

    # ✅ STUDENT
    path("student/templates/", StudentTemplateListView.as_view(), name="student-templates"),
    path("student/templates/<int:pk>/", StudentTemplateDetailView.as_view(), name="student-template-detail"),

    path("student/resumes/", StudentResumeListCreateView.as_view(), name="student-resumes"),
    path("student/resumes/<int:pk>/", StudentResumeDetailView.as_view(), name="student-resume-detail"),
    path("student/dashboard/stats/", StudentDashboardStatsView.as_view(), name="student-dashboard-stats"),
    path("student/resumes/<int:resume_id>/download/", StudentResumeDownloadView.as_view(), name="student-resume-download"),
]
