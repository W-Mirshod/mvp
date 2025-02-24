from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.faq.serializers import FAQSerializer
from .models import FAQ


@method_decorator(csrf_exempt, name='dispatch')
class FAQListView(RetrieveUpdateDestroyAPIView):
    serializer_class = FAQSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]

    
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
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create new FAQ",
        request_body=FAQSerializer,
        responses={
            201: FAQSerializer,
            400: "Bad Request"
        }
    )
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=201)

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
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

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
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

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
        instance = self.get_object()
        instance.delete()
        return Response(status=204)
