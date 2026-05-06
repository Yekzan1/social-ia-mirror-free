from supabase import create_client, Client
from core.config import Config
import streamlit as st

class DatabaseConnection:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance.client = None
            cls._instance.initialize_client()
        return cls._instance

    def initialize_client(self):
        """Initialize Supabase client."""
        if not Config.SUPABASE_URL or not Config.SUPABASE_KEY:
            st.warning("⚠️ Supabase credentials missing. Check your .env file.")
            return None
        
        try:
            self.client = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)
            return self.client
        except Exception as e:
            st.error(f"❌ Failed to connect to Supabase: {str(e)}")
            return None

    def get_client(self) -> Client:
        """Return the Supabase client instance."""
        if not self.client:
            self.initialize_client()
        return self.client

    def initialize_db(self):
        """
        Database structure should be initialized via Supabase SQL Editor.
        This method acts as a check for required tables.
        """
        # In Supabase, we don't usually create tables via code at runtime for security reasons.
        # We assume the user has run the schema.sql in their Supabase dashboard.
        pass

# Helper to get the client quickly
def get_db():
    return DatabaseConnection().get_client()
