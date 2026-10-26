import os
import logging
import firebase_admin
from firebase_admin import credentials
from django.conf import settings

logger = logging.getLogger(__name__)


def get_firebase_app():
    """
    Returns the initialized firebase_admin App instance,
    or initializes it using FIREBASE_CREDENTIALS_PATH from settings if not already initialized.
    """
    if firebase_admin._apps:
        return firebase_admin.get_app()

    cred_path = getattr(settings, 'FIREBASE_CREDENTIALS_PATH', None)
    if not cred_path or not os.path.exists(str(cred_path)):
        logger.warning(f"Firebase credentials file not found at: {cred_path}")
        return None

    try:
        cred = credentials.Certificate(str(cred_path))
        return firebase_admin.initialize_app(cred)
    except Exception as e:
        logger.error(f"Failed to initialize Firebase Admin SDK: {e}")
        return None

