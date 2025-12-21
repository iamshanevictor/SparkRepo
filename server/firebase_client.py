"""Firebase client initialization for SparkRepo."""
import firebase_admin
from firebase_admin import credentials, firestore, auth
import os
import json
import logging

logger = logging.getLogger(__name__)

# Global Firestore client
db = None

def initialize_firebase():
    """Initialize Firebase Admin SDK."""
    global db
    
    try:
        # Check if already initialized
        if firebase_admin._apps:
            logger.info("Firebase already initialized")
            db = firestore.client()
            return db
        
        # Get service account from environment variable
        service_account_json = os.getenv('FIREBASE_SERVICE_ACCOUNT_KEY')
        
        if service_account_json:
            # Parse JSON string to dict
            service_account = json.loads(service_account_json)
            cred = credentials.Certificate(service_account)
        else:
            # Try to load from file (for local development)
            service_account_path = os.getenv('FIREBASE_SERVICE_ACCOUNT_PATH', 'serviceAccountKey.json')
            if os.path.exists(service_account_path):
                cred = credentials.Certificate(service_account_path)
            else:
                raise ValueError(
                    "Firebase credentials not found. Set FIREBASE_SERVICE_ACCOUNT_KEY environment variable "
                    "or place serviceAccountKey.json in the server directory."
                )
        
        # Initialize Firebase
        firebase_admin.initialize_app(cred)
        db = firestore.client()
        
        logger.info("Firebase initialized successfully")
        return db
        
    except Exception as e:
        logger.error(f"Failed to initialize Firebase: {e}")
        raise


def get_firestore_client():
    """Get Firestore client instance."""
    global db
    if db is None:
        db = initialize_firebase()
    return db
