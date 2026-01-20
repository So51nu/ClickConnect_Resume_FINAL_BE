from django.utils import timezone
from .models import TemplateAccess, Subscription, TemplatePricing, ResumeTemplate

def has_active_subscription(user) -> bool:
    today = timezone.localdate()
    return Subscription.objects.filter(
        user=user,
        status="Active",
        start_date__lte=today,
        end_date__gte=today,
    ).exists()

def has_template_access(user, template: ResumeTemplate) -> bool:
    # No template => allow (safe)
    if not template:
        return True

    pricing: TemplatePricing | None = getattr(template, "pricing", None)

    # pricing missing => allow (or you can block, but safe to allow)
    if not pricing:
        return True

    # inactive pricing => block
    if pricing.status != "active":
        return False

    if pricing.billing_type == "free":
        return True

    if pricing.billing_type == "subscription":
        return has_active_subscription(user)

    # one_time
    return TemplateAccess.objects.filter(user=user, template=template).exists()
