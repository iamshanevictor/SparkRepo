"""Supabase client initialization and utilities."""
import os
from typing import Optional
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

class SupabaseClient:
    _instance: Optional[Client] = None
    
    @classmethod
    def get_client(cls) -> Client:
        """Get or create the Supabase client instance."""
        if cls._instance is None:
            url = os.environ.get("SUPABASE_URL")
            key = os.environ.get("SUPABASE_KEY")
            if not url or not key:
                raise ValueError("Missing Supabase URL or key in environment variables")
            cls._instance = create_client(url, key)
        return cls._instance
    
    @classmethod
    def get_admin_client(cls) -> Client:
        """Get or create the Supabase admin client instance (uses service role key)."""
        url = os.environ.get("SUPABASE_URL")
        key = os.environ.get("SUPABASE_SERVICE_KEY")
        if not url or not key:
            raise ValueError("Missing Supabase URL or service key in environment variables")
        return create_client(url, key)

# Export the client functions
get_supabase = SupabaseClient.get_client
get_supabase_admin = SupabaseClient.get_admin_client
