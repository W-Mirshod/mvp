import logging
from typing import Dict
from apps.backend_mailer.constants import BackendConstants

logger = logging.getLogger(__name__)


class EmailBackendManager:
    @staticmethod
    def get_backend_fields(backend_type: int, config: Dict) -> Dict:
        """Get email backend"""
        backend_class = BackendConstants.EMAIL_BACKENDS_CHOICES_DICT.get(backend_type)

        if backend_class:
            required_fields = BackendConstants.BACKEND_FIELDS.get(backend_class, [])
            return {field: config.get(field) for field in required_fields}

        return {}
