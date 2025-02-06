from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from django.utils.decorators import method_decorator

from apps.backend_mailer.serializers.email_template_serializer import (
    RetrieveEmailTemplateSerializer,
    CreateEmailTemplateSerializer,
)
from apps.backend_mailer.view_logic.email_template_qs import EmailTemplateQueryset
from utils.permissions import IsTokenValid
from utils.views import MultiSerializerViewSet

@method_decorator(name='list', decorator=swagger_auto_schema(operation_description="List email templates"))
@method_decorator(name='create', decorator=swagger_auto_schema(operation_description="Create an email template"))
@method_decorator(name='retrieve', decorator=swagger_auto_schema(operation_description="Retrieve an email template"))


class EmailTemplateView(MultiSerializerViewSet):
    queryset = None  # see get_queryset
    permission_classes = (
        IsAuthenticated,
        # IsTokenValid,
    )
    serializers = {
        "list": RetrieveEmailTemplateSerializer,
        "create": CreateEmailTemplateSerializer,
        "retrieve": RetrieveEmailTemplateSerializer,
    }

    def get_queryset(self):
        return EmailTemplateQueryset.email_template_queryset(
            user_obj=self.request.user,
            action=self.action,
            kwargs=self.kwargs,
        )
