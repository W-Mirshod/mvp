from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import action
from django.core.exceptions import ValidationError
from .services import IMAPService
from .models import EmailAccount

class EmailViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = EmailAccount.objects.all()

    def _get_service(self):
        """Helper to create service instance"""
        account = EmailAccount.objects.filter(is_active=True).first()
        return IMAPService(account)

    @action(detail=False)
    def check(self, request):
        try:
            service = self._get_service()
            folder = request.query_params.get('folder', 'INBOX')
            return Response(service.check_folder(folder))
        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

    @action(detail=False)
    def latest(self, request):
        """Get latest emails from specified folder"""
        try:
            service = self._get_service()
            folder = request.query_params.get('folder', 'INBOX')
            limit = min(int(request.query_params.get('limit', 5)), 50)  # Max 50 emails
            
            return Response({
                'folder': folder,
                'emails': service.get_latest_emails(folder, limit)
            })
        except ValidationError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
        except ValueError:
            return Response(
                {'error': 'Invalid limit parameter'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=False)
    def stats(self, request):
        """Get statistics for important folders"""
        try:
            service = self._get_service()
            stats = service.get_folder_stats()
            return Response(stats)
        except ValidationError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )
