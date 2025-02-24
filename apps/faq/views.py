from rest_framework.generics import RetrieveUpdateDestroyAPIView
from apps.faq.serializers import FAQSerializer
from .models import FAQ
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


class FAQListView(RetrieveUpdateDestroyAPIView):
    serializer_class = FAQSerializer
    lookup_field = 'id'
    
    def get_queryset(self):
        return FAQ.objects.filter(is_active=True)

    @swagger_auto_schema(
        operation_description="Get FAQ by ID",
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description="FAQ ID",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="FAQ details",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'question': openapi.Schema(type=openapi.TYPE_STRING),
                        'answer': openapi.Schema(type=openapi.TYPE_STRING),
                    }
                )
            ),
            404: "FAQ not found"
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Update FAQ",
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description="FAQ ID",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        request_body=FAQSerializer,
        responses={
            200: FAQSerializer,
            400: "Bad Request",
            404: "FAQ not found"
        }
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Partially update FAQ",
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description="FAQ ID",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        request_body=FAQSerializer,
        responses={
            200: FAQSerializer,
            400: "Bad Request",
            404: "FAQ not found"
        }
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_description="Delete FAQ",
        manual_parameters=[
            openapi.Parameter(
                'id',
                openapi.IN_PATH,
                description="FAQ ID",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            204: "FAQ deleted successfully",
            404: "FAQ not found"
        }
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)